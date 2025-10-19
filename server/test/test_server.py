import sys
import os
import io
import json
import importlib
from unittest.mock import MagicMock, patch

import pytest
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash
from itsdangerous import BadSignature
from sqlalchemy.exc import IntegrityError

# --- 1. 环境设置 ---
os.environ['SECRET_KEY'] = 'a-very-secret-key-for-testing'
os.environ['DB_HOST'], os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_NAME'] = 'mock','mock','mock','mock'
# 确保在导入 server 之前设置好环境变量
if 'server' in sys.modules:
    del sys.modules['server']
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
sys.modules['rmap_routes'] = MagicMock()

# --- 2. 导入应用 ---
from server import create_app

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
    # 确保 watermarking_method 存在，以使 WatermarkingMethod 被正确定义
    sys.modules['watermarking_method'] = MagicMock()
    
    app_instance = create_app()
    app_instance.config['TESTING'] = True
    app_instance.config['WTF_CSRF_ENABLED'] = False
    yield app_instance
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    del sys.modules['watermarking_method']

@pytest.fixture
def client(app, mocker):
    reset_mock_db()
    mocker.patch('server.HAS_SQLALCHEMY', True)
    
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_engine.begin.return_value.__enter__.return_value = mock_conn

    def mock_execute(sql_obj, params=None, **kwargs):
        sql = str(sql_obj).lower()
        final_params = (params or {}).copy()
        final_params.update(kwargs)

        # 使用 if/elif 结构避免错误的逻辑分支匹配
        if 'select 1' in sql:
            return MagicMock(fetchone=lambda: (1,))
        elif 'insert into users' in sql:
            if any(u['email'] == final_params.get('email') for u in db_data['users'].values()):
                raise IntegrityError("mock email exists", "params", "orig")
            user_id = next_ids['users']
            db_data['users'][user_id] = {'id': user_id, 'hpassword': 'hashed_pw', **final_params}
            next_ids['users'] += 1
            return MagicMock(lastrowid=user_id)
        elif 'select' in sql and 'from users where' in sql:
            user = None
            if 'email' in final_params:
                user = next((u for u in db_data['users'].values() if u['email'] == final_params['email']), None)
                if user: return MagicMock(first=lambda: create_mock_row(user))
            elif 'id' in final_params:
                user = db_data['users'].get(final_params['id'])
                if user: return MagicMock(one=lambda: create_mock_row(user))
            return MagicMock(first=lambda: None, one=lambda: None)
        elif 'insert into documents' in sql:
            doc_id = next_ids['documents']
            db_data['documents'][doc_id] = {'id': doc_id, **final_params}
            next_ids['documents'] += 1
            return MagicMock(lastrowid=doc_id, scalar=lambda: doc_id)
        elif 'select' in sql and 'from documents where' in sql:
            uid = final_params.get('uid', -1)
            if 'id' in final_params and uid != -1:
                doc = db_data['documents'].get(final_params.get('id'))
                if doc and doc.get('ownerid') == uid: return MagicMock(first=lambda: create_mock_row(doc))
                return MagicMock(first=lambda: None)
            elif uid != -1:
                doc_list = [d for d in db_data['documents'].values() if d.get('ownerid') == uid]
                return MagicMock(all=lambda: [create_mock_row(d) for d in doc_list])
        elif 'select' in sql and 'from versions' in sql:
            if 'link' in final_params:
                version = next((v for v in db_data['versions'].values() if v.get('link') == final_params['link']), None)
                if version: return MagicMock(first=lambda: create_mock_row(version))
            elif final_params.get('did'):
                ver_list = [v for v in db_data['versions'].values() if v.get('documentid') == final_params['did']]
                return MagicMock(all=lambda: [create_mock_row(v) for v in ver_list])
            return MagicMock(first=lambda: None, all=lambda: [])
        elif 'delete from' in sql:
            if 'from versions' in sql or 'versions' in str(sql_obj):
                db_data['versions'] = {k:v for k,v in db_data['versions'].items() if v.get('documentid') != final_params.get('did')}
            if 'from documents' in sql or 'documents' in str(sql_obj):
                db_data['documents'].pop(final_params.get('id'), None)
            return MagicMock()
        elif 'insert into versions' in sql:
            ver_id = next_ids['versions']
            db_data['versions'][ver_id] = {'id': ver_id, **final_params}
            next_ids['versions'] += 1
            return MagicMock(lastrowid=ver_id, scalar=lambda: ver_id)
        elif 'last_insert_id' in sql:
            return MagicMock(scalar=lambda: next_ids['documents'] - 1)
        
        return MagicMock()

    mock_conn.execute.side_effect = mock_execute
    mocker.patch('server.create_engine', return_value=mock_engine)
    mocker.patch('server.WMUtils.apply_watermark', return_value=b'%PDF-watermarked-content')
    mocker.patch('server.WMUtils.read_watermark', return_value='decoded-secret')
    mocker.patch('server.check_password_hash', side_effect=lambda h, p: p != 'wrong')
    
    with app.app_context():
        yield app.test_client()

@pytest.fixture
def auth_headers(client):
    email, password = 'fixture-user@test.com', 'fixture-password'
    res = client.post('/api/create-user', json={'email': email, 'login': 'fixture_user', 'password': password})
    assert res.status_code == 201
    res = client.post('/api/login', json={'email': email, 'password': password})
    assert res.status_code == 200
    return {'Authorization': f"Bearer {res.json['token']}"}

@pytest.fixture
def admin_headers(mocker):
    mocker.patch('server.URLSafeTimedSerializer.loads', return_value={"uid": 999, "roles": ["admin"]})
    return {'Authorization': 'Bearer admin-token-string'}

@pytest.fixture
def uploaded_doc(client, auth_headers):
    pdf_content = b'%PDF-1.0\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n149\n%%EOF'
    pdf_file = FileStorage(stream=io.BytesIO(pdf_content), filename='test.pdf')
    res = client.post('/api/upload-document', headers=auth_headers, data={'file': pdf_file})
    assert res.status_code == 201
    return res.json['id']

# --- 5. 测试用例 ---

def test_public_pages(client):
    assert client.get('/').status_code == 200
    assert client.get('/login').status_code == 200
    assert client.get('/signup').status_code == 200

def test_healthz_with_mock_db(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json['db_connected'] is True
    response = client.get('/api/healthz')
    assert response.status_code == 200

class TestUserAuth:
    def test_signup_and_login_flow(self, client):
        res = client.post('/api/create-user', json={'email': 'test@test.com', 'login': 'testuser', 'password': 'password123'})
        assert res.status_code == 201
        res = client.post('/api/login', json={'email': 'test@test.com', 'password': 'wrong'})
        assert res.status_code == 401
        res = client.post('/api/login', json={'email': 'test@test.com', 'password': 'password123'})
        assert res.status_code == 200
        token = res.json['token']
        res = client.post('/auth/session', json={'token': token})
        assert res.status_code == 200

    def test_unauthorized_access(self, client):
        assert client.get('/api/list-documents').status_code == 401
        assert client.post('/api/upload-document').status_code == 401
    
    def test_logout(self, client):
        res = client.post('/logout')
        assert res.status_code == 200
        assert 'auth_token=;' in res.headers['Set-Cookie']

class TestFullWorkflow:
    def test_document_lifecycle(self, client, auth_headers):
        pdf_content = (b'%PDF-1.0\n'b'trailer<</Size 4/Root 1 0 R>>\nstartxref\n149\n%%EOF')
        pdf_file = FileStorage(stream=io.BytesIO(pdf_content), filename='test.pdf')
        res = client.post('/api/upload-document', headers=auth_headers, data={'file': pdf_file, 'name': 'My First PDF'})
        assert res.status_code == 201
        doc_id = res.json['id']
        res = client.get(f'/api/get-document/{doc_id}', headers=auth_headers)
        assert res.status_code == 200
        res = client.post(f'/api/create-watermark/{doc_id}', headers=auth_headers, json={'method': 'm', 'secret': 's'})
        assert res.status_code == 201
        version_link = res.json['link']
        res = client.post(f'/api/read-watermark/{doc_id}', headers=auth_headers, json={'method': 'm', 'link': version_link})
        assert res.status_code == 200
        res = client.delete(f'/api/delete-document/{doc_id}', headers=auth_headers)
        assert res.status_code == 200
        res = client.get(f'/api/get-document/{doc_id}', headers=auth_headers)
        assert res.status_code == 404

class TestAPIEdgeCases:
    def test_create_user_failures(self, client):
        res = client.post('/api/create-user', json={'email': 'a@b.com', 'login': 'user'})
        assert res.status_code == 400
        client.post('/api/create-user', json={'email': 'test@test.com', 'login': 'testuser', 'password': 'pw'})
        res = client.post('/api/create-user', json={'email': 'test@test.com', 'login': 'testuser2', 'password': 'pw'})
        assert res.status_code == 409

    def test_login_failures(self, client):
        res = client.post('/api/login', json={'email': 'user@example.com'})
        assert res.status_code == 400
        res = client.post('/api/login', json={'email': 'no-such-user@test.com', 'password': 'p'})
        assert res.status_code == 401

    def test_unauthorized_access_with_bad_token(self, client, mocker):
        mocker.patch('server.URLSafeTimedSerializer.loads', side_effect=BadSignature("mocked bad signature"))
        bad_headers = {'Authorization': 'Bearer a-bad-token'}
        res = client.get('/api/list-documents', headers=bad_headers)
        assert res.status_code == 401

    @pytest.mark.parametrize("file_data, content_type, error_msg, status_code", [
        ({}, None, 'no_file', 400),
        ({'file': (io.BytesIO(b''), '')}, 'multipart/form-data', 'filename_missing', 400),
        ({'file': (io.BytesIO(b"t"), 't.txt')}, 'multipart/form-data', 'unsupported_media_type', 415),
        ({'file': (io.BytesIO(b"%PDF-invalid"), 'b.pdf')}, 'multipart/form-data', 'invalid_pdf', 400),
        ({'file': (io.BytesIO(b"0" * (21*1024*1024)), 'l.pdf')}, 'multipart/form-data', 'payload_too_large', 413),
    ])
    def test_upload_document_failures(self, client, auth_headers, file_data, content_type, error_msg, status_code):
        res = client.post('/api/upload-document', headers=auth_headers, data=file_data, content_type=content_type)
        assert res.status_code == status_code
        assert res.json['error'] == error_msg
    
    def test_create_watermark_failures(self, client, auth_headers, uploaded_doc):
        res = client.post(f'/api/create-watermark/{uploaded_doc}', headers=auth_headers, json={'secret': 'abc'})
        assert res.status_code == 400
        res = client.post(f'/api/create-watermark/{uploaded_doc}', headers=auth_headers, json={'method': 'm'})
        assert res.status_code == 400
        res = client.post('/api/create-watermark/9999', headers=auth_headers, json={'method': 'm', 'secret': 's'})
        assert res.status_code == 404

    def test_read_watermark_failures(self, client, auth_headers, uploaded_doc):
        res = client.post(f'/api/read-watermark/{uploaded_doc}', headers=auth_headers, json={})
        assert res.status_code == 400
        res = client.post('/api/read-watermark/9999', headers=auth_headers, json={'method': 'm'})
        assert res.status_code == 404

    def test_delete_nonexistent_document(self, client, auth_headers):
        res = client.delete('/api/delete-document/9999', headers=auth_headers)
        assert res.status_code == 404

class TestAdminRoutes:
    def test_load_plugin_permission_denied(self, client, auth_headers):
        res = client.post('/api/load-plugin', headers=auth_headers, json={})
        assert res.status_code == 403

    def test_load_plugin_admin_access(self, client, admin_headers, app, mocker):
        from server import WatermarkingMethod
        res = client.post('/api/load-plugin', headers=admin_headers, json={})
        assert res.status_code == 400
        res = client.post('/api/load-plugin', headers=admin_headers, json={'filename': 'no-such-plugin.py'})
        assert res.status_code == 404
        
        plugin_dir = app.config["STORAGE_DIR"] / "files" / "plugins"
        plugin_dir.mkdir(parents=True, exist_ok=True)
        # 创建一个符合规范的插件
        dummy_plugin_code = """
from server import WatermarkingMethod
class Plugin(WatermarkingMethod):
    name = "dummy-plugin"
"""
        (plugin_dir / "dummy.py").write_text(dummy_plugin_code)
        
        res = client.post('/api/load-plugin', headers=admin_headers, json={'filename': 'dummy.py'})
        assert res.status_code == 201
        assert res.json['registered_as'] == 'dummy-plugin'

class TestPyMySQLEmulation:
    @pytest.fixture
    def pymysql_client(self, mocker):
        mocker.patch('server.HAS_SQLALCHEMY', False)
        # 注入一个 mock pymysql 模块
        mocker.patch.dict('sys.modules', {'pymysql': MagicMock()})
        
        # 重新加载 server 模块以使其导入 mock 的 pymysql
        import server
        importlib.reload(server)
        
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.lastrowid = 1
        
        def fetchone_side_effect(*args):
            sql = args[0] if args else ""
            if "SELECT id, email, login FROM Users" in sql: return (1, 'p@t.com', 'p_user')
            if "SELECT id, email, login, hpassword" in sql: return (1, 'p@t.com', 'p_user', generate_password_hash('pw'))
            return None
        mock_cursor.fetchone.side_effect = fetchone_side_effect
        
        # 现在可以 patch 'server.pymysql.connect'
        server.pymysql.connect.return_value.__enter__.return_value = mock_conn

        test_app = server.create_app()
        test_app.config['TESTING'] = True
        with test_app.app_context():
            yield test_app.test_client()

    def test_healthz_with_pymysql(self, pymysql_client):
        res = pymysql_client.get('/healthz')
        assert res.status_code == 200

    def test_create_user_with_pymysql(self, pymysql_client):
        res = pymysql_client.post('/api/create-user', json={'email': 'p@t.com', 'login': 'p_user', 'password': 'pw'})
        assert res.status_code == 201

    def test_login_with_pymysql(self, pymysql_client):
        res = pymysql_client.post('/api/login', json={'email': 'p@t.com', 'password': 'pw'})
        assert res.status_code == 200

class TestWebAuth:
    def test_documents_page_unauthorized(self, client):
        res = client.get('/documents', follow_redirects=False)
        assert res.status_code == 302
        assert '/login' in res.location

    def test_documents_page_with_bad_token(self, client):
        client.set_cookie('auth_token', 'invalid-token')
        res = client.get('/documents', follow_redirects=False)
        assert res.status_code == 302
