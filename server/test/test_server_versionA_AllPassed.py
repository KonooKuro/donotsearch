import sys
import os
import io
import json
from unittest.mock import MagicMock, patch

import pytest
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash

# --- 1. 环境设置 ---
os.environ['SECRET_KEY'] = 'a-very-secret-key-for-testing'
os.environ['DB_HOST'], os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_NAME'] = 'mock','mock','mock','mock'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
sys.modules['rmap_routes'] = MagicMock()

# --- 2. 导入应用 ---
from server import create_app, HAS_SQLALCHEMY

# --- 3. 全局测试辅助工具 ---
db_data, next_ids = {}, {}
def reset_mock_db():
    global db_data, next_ids
    db_data, next_ids = {"users":{},"documents":{},"versions":{}}, {"users":1,"documents":1,"versions":1}
def create_mock_row(data_dict):
    row = MagicMock()
    row.configure_mock(**data_dict)
    row.__getitem__.side_effect = lambda i: list(data_dict.values())[i]
    return row

# --- 4. Pytest Fixtures ---
@pytest.fixture(scope="module")
def app():
    temp_dir = os.path.join(os.path.dirname(__file__), 'test_storage_temp')
    os.environ['STORAGE_DIR'] = temp_dir
    app_instance = create_app()
    app_instance.config['TESTING'] = True
    yield app_instance
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

@pytest.fixture
def client(app, mocker):
    reset_mock_db()
    if not HAS_SQLALCHEMY:
        pytest.skip("此深度测试套件需要 SQLAlchemy 已安装")

    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_engine.begin.return_value.__enter__.return_value = mock_conn

    def mock_execute(sql_obj, params=None, **kwargs):
        sql = str(sql_obj).lower()
        final_params = (params or {}).copy()
        final_params.update(kwargs)

        if 'select 1' in sql: return MagicMock(fetchone=lambda: (1,))
        if 'insert into users' in sql:
            user_id = next_ids['users']
            db_data['users'][user_id] = {'id': user_id, **final_params}
            next_ids['users'] += 1
            return MagicMock(lastrowid=user_id)
        if 'from users where' in sql:
            user = None
            if 'email' in final_params:
                user = next((u for u in db_data['users'].values() if u['email'] == final_params['email']), None)
                if user: return MagicMock(first=lambda: create_mock_row(user))
            elif 'id' in final_params:
                user = db_data['users'].get(final_params['id'])
                if user: return MagicMock(one=lambda: create_mock_row(user))
            return MagicMock(first=lambda: None, one=lambda: None)
        if 'insert into documents' in sql:
            doc_id = next_ids['documents']
            db_data['documents'][doc_id] = {'id': doc_id, **final_params}
            next_ids['documents'] += 1
            return MagicMock(lastrowid=doc_id)
        if 'select' in sql and 'from documents where' in sql:
            uid = final_params.get('uid', -1)
            if 'id' in final_params and uid != -1:
                doc = db_data['documents'].get(final_params.get('id'))
                if doc and doc.get('ownerid') == uid: return MagicMock(first=lambda: create_mock_row(doc))
                return MagicMock(first=lambda: None)
            elif uid != -1:
                doc_list = [d for d in db_data['documents'].values() if d.get('ownerid') == uid]
                return MagicMock(all=lambda: [create_mock_row(d) for d in doc_list])
        
        # 关键修正：添加对 versions 表的查询模拟
        if 'from versions' in sql and 'select' in sql:
            # `read_watermark` 通过 link 查询
            if 'link' in final_params:
                version = next((v for v in db_data['versions'].values() if v.get('link') == final_params['link']), None)
                if version:
                    return MagicMock(first=lambda: create_mock_row(version))
            return MagicMock(first=lambda: None)

        if 'delete from' in sql:
            if 'from versions' in sql: db_data['versions'] = {k:v for k,v in db_data['versions'].items() if v.get('documentid') != final_params.get('did')}
            if 'from documents' in sql: db_data['documents'].pop(final_params.get('id'), None)
            return MagicMock()
        if 'insert into versions' in sql:
            ver_id = next_ids['versions']
            db_data['versions'][ver_id] = {'id': ver_id, **final_params}
            next_ids['versions'] += 1
            return MagicMock(lastrowid=ver_id)
            
        return MagicMock()

    mock_conn.execute.side_effect = mock_execute
    mocker.patch('server.create_engine', return_value=mock_engine)
    mocker.patch('server.WMUtils.apply_watermark', return_value=b'%PDF-watermarked-content')
    # 修正：确保模拟返回正确的字符串格式
    mocker.patch('server.WMUtils.read_watermark', return_value='decoded-secret')
    mock_check_pass = mocker.patch('server.check_password_hash')
    mock_check_pass.side_effect = lambda h, p: p != 'wrong'
    with app.app_context():
        yield app.test_client()

@pytest.fixture
def auth_headers(client, app):
    email, password = 'fixture-user@test.com', 'fixture-password'
    res = client.post('/api/create-user', json={'email': email, 'login': 'fixture_user', 'password': password})
    assert res.status_code == 201, f"Fixture 'auth_headers' 创建用户失败: {res.json}"
    res = client.post('/api/login', json={'email': email, 'password': password})
    assert res.status_code == 200, f"Fixture 'auth_headers' 登录失败: {res.json}"
    return {'Authorization': f"Bearer {res.json['token']}"}

# --- 5. 测试用例 ---
def test_public_pages(client):
    assert client.get('/').status_code == 200
    assert client.get('/login').status_code == 200

def test_healthz_with_mock_db(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json['db_connected'] is True

class TestUserAuth:
    def test_signup_and_login_flow(self, client):
        res = client.post('/api/create-user', json={'email': 'test@test.com', 'login': 'testuser', 'password': 'password123'})
        assert res.status_code == 201
        res = client.post('/api/login', json={'email': 'test@test.com', 'password': 'wrong'})
        assert res.status_code == 401
        res = client.post('/api/login', json={'email': 'test@test.com', 'password': 'password123'})
        assert res.status_code == 200
        assert 'token' in res.json

    def test_unauthorized_access(self, client):
        assert client.get('/api/list-documents').status_code == 401
        assert client.post('/api/upload-document').status_code == 401

class TestFullWorkflow:
    def test_document_lifecycle(self, client, auth_headers):
        pdf_content = (
            b'%PDF-1.0\n'
            b'1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n'
            b'trailer<</Size 4/Root 1 0 R>>\nstartxref\n149\n%%EOF'
        )
        pdf_file = FileStorage(stream=io.BytesIO(pdf_content), filename='test.pdf', content_type='application/pdf')
        res = client.post(
            '/api/upload-document', headers=auth_headers,
            data={'file': pdf_file, 'name': 'My First PDF'}, content_type='multipart/form-data'
        )
        assert res.status_code == 201, f"文件上传失败: {res.json}"
        doc_data = res.json
        doc_id = doc_data['id']
        assert doc_data['name'] == 'My_First_PDF'
        res = client.get(f'/api/get-document/{doc_id}', headers=auth_headers)
        assert res.status_code == 200
        assert res.data == pdf_content
        res = client.post(f'/api/create-watermark/{doc_id}', headers=auth_headers, json={
            'method': 'wjj-watermark', 'secret': 'top-secret'
        })
        assert res.status_code == 201
        version_link = res.json['link']
        res = client.post(f'/api/read-watermark/{doc_id}', headers=auth_headers, json={
            'method': 'wjj-watermark', 'link': version_link
        })
        # 修正后的断言
        assert res.status_code == 200
        # 因为我们模拟返回的是 'decoded-secret'，所以这里检查 raw 字段
        assert res.json['raw'] == 'decoded-secret'
        res = client.delete(f'/api/delete-document/{doc_id}', headers=auth_headers)
        assert res.status_code == 200
        res = client.get(f'/api/get-document/{doc_id}', headers=auth_headers)
        assert res.status_code == 404
