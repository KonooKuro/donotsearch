import sys
import os
import io
import json
from unittest.mock import MagicMock, patch

import pytest
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash

# --- 1. 环境设置 ---
# 在导入任何应用代码之前完成

# 设置必要的环境变量
os.environ['SECRET_KEY'] = 'a-very-secret-key-for-testing'
os.environ['DB_HOST'] = 'mock-db'
os.environ['DB_USER'] = 'mock-user'
os.environ['DB_PASSWORD'] = 'mock-pass'
os.environ['DB_NAME'] = 'mock-db-name'

# 将 'src' 目录添加到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# 模拟掉非核心的、可能不存在的依赖
sys.modules['rmap_routes'] = MagicMock()

# --- 2. 导入应用 ---
from server import create_app, HAS_SQLALCHEMY

# --- 3. 全局测试辅助工具 ---

# 用 Python 字典模拟数据库
db_data = {}
next_ids = {}

def reset_mock_db():
    """重置内存数据库，确保测试隔离"""
    global db_data, next_ids
    db_data = {
        "users": {}, "documents": {}, "versions": {}
    }
    next_ids = {
        "users": 1, "documents": 1, "versions": 1
    }

def create_mock_row(data_dict):
    """辅助函数：创建一个行为类似 SQLAlchemy Row 的模拟对象"""
    row = MagicMock()
    # 使用 configure_mock 一次性设置所有属性，使其可以通过 `row.attribute` 访问
    row.configure_mock(**data_dict)
    # 允许通过索引访问，模拟元组行为 `row[0]`
    row.__getitem__.side_effect = lambda i: list(data_dict.values())[i]
    return row

# --- 4. Pytest Fixtures (测试的“积木块”) ---

@pytest.fixture(scope="module")
def app():
    """创建一个全局的 Flask app 实例 (在所有测试运行前只执行一次)"""
    # 使用临时目录作为文件存储，避免测试污染实际文件系统
    temp_dir = os.path.join(os.path.dirname(__file__), 'test_storage_temp')
    os.environ['STORAGE_DIR'] = temp_dir
    
    app_instance = create_app()
    app_instance.config['TESTING'] = True
    
    # 使用 yield 将 app_instance 提供给测试
    yield app_instance

    # 所有测试结束后，清理临时文件目录
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

@pytest.fixture
def client(app, mocker):
    """
    为每个测试函数创建一个新的 client，并 patch 数据库连接和外部依赖。
    这是最重要的 fixture，确保每个测试都在一个干净的环境中运行。
    """
    reset_mock_db()

    if not HAS_SQLALCHEMY:
        pytest.skip("此深度测试套件需要 SQLAlchemy 已安装")

    # --- 数据库模拟核心逻辑 ---
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    # 模拟 `with engine.connect() as conn:` 的行为
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_engine.begin.return_value.__enter__.return_value = mock_conn

    def mock_execute(sql_obj, params=None, **kwargs):
        """这个函数是模拟数据库的核心，它拦截SQL并返回伪造的数据"""
        sql = str(sql_obj).lower()
        params = params or kwargs

        # 模拟健康检查
        if 'select 1' in sql:
            return MagicMock(fetchone=lambda: (1,))
        
        # 模拟创建用户
        if 'insert into users' in sql:
            user_id = next_ids['users']
            db_data['users'][user_id] = {'id': user_id, **params}
            next_ids['users'] += 1
            return MagicMock(lastrowid=user_id)

        # 模拟查询用户
        if 'from users where' in sql:
            user = None
            if 'email' in params:
                user = next((u for u in db_data['users'].values() if u['email'] == params['email']), None)
            elif 'id' in params:
                user = db_data['users'].get(params['id'])
            
            if user:
                mock_row = create_mock_row(user)
                return MagicMock(first=lambda: mock_row, one=lambda: mock_row)
            return MagicMock(first=lambda: None, one=lambda: None)
            
        # 模拟上传文档
        if 'insert into documents' in sql:
            doc_id = next_ids['documents']
            db_data['documents'][doc_id] = {'id': doc_id, **params}
            next_ids['documents'] += 1
            return MagicMock(lastrowid=doc_id)

        # 模拟查询文档 (覆盖 list-documents 和 get-document)
        if 'from documents where' in sql:
            # get-document 的情况
            if 'id' in params and 'ownerid' in params.get('uid', -1): # 使用 .get 避免 KeyError
                doc = db_data['documents'].get(params.get('id'))
                if doc and doc.get('ownerid') == params.get('uid'):
                     return MagicMock(first=lambda: create_mock_row(doc))
                return MagicMock(first=lambda: None)
            
            # list-documents 的情况
            elif 'ownerid' in params:
                owner_id_key = 'ownerid' if 'ownerid' in params else 'uid'
                doc_list = [d for d in db_data['documents'].values() if d.get('ownerid') == params.get(owner_id_key)]
                mock_rows = [create_mock_row(d) for d in doc_list]
                return MagicMock(all=lambda: mock_rows)

        # 模拟删除
        if 'delete from' in sql:
            if 'from versions' in sql:
                db_data['versions'] = {k: v for k, v in db_data['versions'].items() if v.get('documentid') != params.get('did')}
            if 'from documents' in sql:
                db_data['documents'].pop(params.get('id'), None)
            return MagicMock()
            
        # 模拟创建水印版本
        if 'insert into versions' in sql:
            ver_id = next_ids['versions']
            db_data['versions'][ver_id] = {'id': ver_id, **params}
            next_ids['versions'] += 1
            return MagicMock(lastrowid=ver_id)

        return MagicMock()

    mock_conn.execute.side_effect = mock_execute
    
    # 关键修正：patch 'server.create_engine'，因为 server.py 导入了它
    mocker.patch('server.create_engine', return_value=mock_engine)
    
    # 模拟水印工具函数，让它们返回固定的、可预测的结果
    mocker.patch('server.WMUtils.apply_watermark', return_value=b'%PDF-watermarked-content')
    mocker.patch('server.WMUtils.read_watermark', return_value='{"secret": "decoded-secret"}')
    
    with app.app_context():
        yield app.test_client()

@pytest.fixture
def auth_headers(client, app):
    """Fixture 修正：在内存数据库中直接创建用户，然后通过 API 登录获取真实 token"""
    email = 'fixture-user@test.com'
    password = 'fixture-password'
    
    # 直接在内存数据库中创建用户记录，使用真实的哈希函数
    user_id = next_ids['users']
    db_data['users'][user_id] = {
        'id': user_id,
        'email': email,
        'login': 'fixture_user',
        'hpassword': generate_password_hash(password)
    }
    next_ids['users'] += 1

    # 通过 API 登录以获取一个由服务器签发的有效 token
    res = client.post('/api/login', json={'email': email, 'password': password})
    
    assert res.status_code == 200, f"Fixture 'auth_headers' 登录失败. 响应: {res.json}"
    assert 'token' in res.json
    
    token = res.json['token']
    return {'Authorization': f'Bearer {token}'}


# --- 5. 测试用例 ---

def test_public_pages(client):
    """测试无需登录即可访问的页面"""
    assert client.get('/').status_code == 200
    assert client.get('/login').status_code == 200

def test_healthz_with_mock_db(client):
    """测试 healthz 端点能反映模拟的数据库连接状态"""
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json['db_connected'] is True

class TestUserAuth:
    """用户认证流程的详细测试"""
    def test_signup_and_login_flow(self, client):
        """测试用户创建和登录的完整流程"""
        res = client.post('/api/create-user', json={'email': 'test@test.com'})
        assert res.status_code == 400

        res = client.post('/api/create-user', json={
            'email': 'test@test.com', 'login': 'testuser', 'password': 'password123'
        })
        assert res.status_code == 201
        
        res = client.post('/api/login', json={'email': 'test@test.com', 'password': 'wrong'})
        assert res.status_code == 401
        
        res = client.post('/api/login', json={'email': 'test@test.com', 'password': 'password123'})
        assert res.status_code == 200
        assert 'token' in res.json

    def test_unauthorized_access(self, client):
        """测试未认证时访问受保护的API"""
        assert client.get('/api/list-documents').status_code == 401
        assert client.post('/api/upload-document').status_code == 401

class TestFullWorkflow:
    """测试核心业务的完整工作流"""
    def test_document_lifecycle(self, client, auth_headers):
        """测试从上传到删除的完整文档生命周期"""
        
        # 1. 上传文档
        # 关键修正：使用一个结构上有效的最小化PDF内容，以通过服务器校验
        pdf_content = (
            b'%PDF-1.0\n'
            b'1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n'
            b'2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n'
            b'3 0 obj<</Type/Page/MediaBox[0 0 3 3]>>endobj\n'
            b'xref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000058 00000 n\n0000000106 00000 n\n'
            b'trailer<</Size 4/Root 1 0 R>>\n'
            b'startxref\n149\n%%EOF'
        )
        pdf_file = FileStorage(stream=io.BytesIO(pdf_content), filename='test.pdf', content_type='application/pdf')
        
        res = client.post(
            '/api/upload-document', headers=auth_headers,
            data={'file': pdf_file, 'name': 'My First PDF'}, content_type='multipart/form-data'
        )
        
        assert res.status_code == 201, f"文件上传失败, 状态码: {res.status_code}, 内容: {res.json}"
        doc_data = res.json
        doc_id = doc_data['id']
        assert doc_data['name'] == 'My First PDF'

        # 2. 获取文档列表和单个文档
        res = client.get('/api/list-documents', headers=auth_headers)
        assert res.status_code == 200
        assert len(res.json['documents']) == 1

        res = client.get(f'/api/get-document/{doc_id}', headers=auth_headers)
        assert res.status_code == 200
        assert res.data == pdf_content

        # 3. 创建水印
        res = client.post(f'/api/create-watermark/{doc_id}', headers=auth_headers, json={
            'method': 'wjj-watermark', 'secret': 'top-secret'
        })
        assert res.status_code == 201
        version_link = res.json['link']

        # 4. 读取水印
        res = client.post(f'/api/read-watermark/{doc_id}', headers=auth_headers, json={
            'method': 'wjj-watermark', 'link': version_link
        })
        assert res.status_code == 200
        assert res.json['secret'] == 'decoded-secret'

        # 5. 删除文档
        res = client.delete(f'/api/delete-document/{doc_id}', headers=auth_headers)
        assert res.status_code == 200
        
        # 6. 确认已删除
        res = client.get(f'/api/get-document/{doc_id}', headers=auth_headers)
        assert res.status_code == 404
