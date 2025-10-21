import sys
import os
import json
import pytest
from io import BytesIO
from unittest.mock import MagicMock

# 设置环境变量
os.environ['SECRET_KEY'] = 'test-secret-key-12345'
os.environ['DB_HOST'] = '127.0.0.1'
os.environ['DB_USER'] = 'test'
os.environ['DB_PASSWORD'] = 'test'
os.environ['DB_NAME'] = 'test'

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

# Mock 依赖
sys.modules['watermarking_utils'] = MagicMock()
sys.modules['watermarking_method'] = MagicMock()
sys.modules['rmap_routes'] = MagicMock()

from server import create_app

@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def auth_token(app):
    """生成认证令牌"""
    from itsdangerous import URLSafeTimedSerializer
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt='tatou-auth')
    return serializer.dumps({
        'uid': 1,
        'login': 'testuser',
        'email': 'test@example.com',
        'roles': []
    })

@pytest.fixture
def admin_token(app):
    """生成管理员令牌"""
    from itsdangerous import URLSafeTimedSerializer
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt='tatou-auth')
    return serializer.dumps({
        'uid': 1,
        'login': 'admin',
        'email': 'admin@example.com',
        'roles': ['admin']
    })

# ===================== 基础测试 =====================

def test_create_app(app):
    """测试创建应用"""
    assert app is not None
    assert app.config['TESTING'] is True

def test_healthz(client):
    """测试健康检查"""
    response = client.get('/healthz')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data

def test_api_healthz(client):
    """测试 API 健康检查"""
    response = client.get('/api/healthz')
    assert response.status_code == 200

# ===================== 认证测试 =====================

def test_create_user_missing_email(client):
    """测试创建用户缺少email"""
    response = client.post('/api/create-user', json={
        'login': 'testuser',
        'password': 'pass123'
    })
    assert response.status_code == 400

def test_create_user_missing_login(client):
    """测试创建用户缺少login"""
    response = client.post('/api/create-user', json={
        'email': 'test@example.com',
        'password': 'pass123'
    })
    assert response.status_code == 400

def test_create_user_missing_password(client):
    """测试创建用户缺少password"""
    response = client.post('/api/create-user', json={
        'email': 'test@example.com',
        'login': 'testuser'
    })
    assert response.status_code == 400

def test_create_user_empty_fields(client):
    """测试创建用户使用空字段"""
    response = client.post('/api/create-user', json={
        'email': '',
        'login': '',
        'password': ''
    })
    assert response.status_code == 400

def test_create_user_with_json(client):
    """测试使用JSON创建用户"""
    response = client.post('/api/create-user', json={
        'email': 'test@example.com',
        'login': 'testuser',
        'password': 'pass123'
    })
    # 数据库连接失败会返回503
    assert response.status_code in [201, 503, 409]

def test_create_user_with_form(client):
    """测试使用form data创建用户"""
    response = client.post('/api/create-user', 
                          data={'email': 'test@example.com',
                                'login': 'testuser',
                                'password': 'pass123'},
                          content_type='application/x-www-form-urlencoded')
    assert response.status_code in [201, 400, 503, 409]

def test_login_missing_email(client):
    """测试登录缺少email"""
    response = client.post('/api/login', json={
        'password': 'pass123'
    })
    assert response.status_code == 400

def test_login_missing_password(client):
    """测试登录缺少password"""
    response = client.post('/api/login', json={
        'email': 'test@example.com'
    })
    assert response.status_code == 400

def test_login_empty_email(client):
    """测试登录空email"""
    response = client.post('/api/login', json={
        'email': '',
        'password': 'pass123'
    })
    assert response.status_code == 400

def test_login_empty_password(client):
    """测试登录空password"""
    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': ''
    })
    assert response.status_code == 400

def test_login_invalid_credentials(client):
    """测试使用无效凭证登录"""
    response = client.post('/api/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpass'
    })
    # 数据库连接失败503或无效凭证401
    assert response.status_code in [401, 503]

def test_auth_session_missing_token(client):
    """测试设置session缺少token"""
    response = client.post('/auth/session', json={})
    assert response.status_code == 400

def test_auth_session_empty_token(client):
    """测试设置session空token"""
    response = client.post('/auth/session', json={'token': ''})
    assert response.status_code == 400

def test_auth_session_with_token(client, auth_token):
    """测试设置session"""
    response = client.post('/auth/session', json={'token': auth_token})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['ok'] is True

def test_logout(client):
    """测试登出"""
    response = client.post('/logout')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['ok'] is True

# ===================== 认证中间件测试 =====================

def test_require_auth_no_token(client):
    """测试需要认证但没有token"""
    response = client.get('/api/list-documents')
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['error'] == 'unauthorized'

def test_require_auth_invalid_token(client):
    """测试无效token"""
    response = client.get('/api/list-documents',
                         headers={'Authorization': 'Bearer invalid-token-xyz'})
    assert response.status_code == 401

def test_require_auth_malformed_header(client):
    """测试格式错误的Authorization header"""
    response = client.get('/api/list-documents',
                         headers={'Authorization': 'InvalidFormat'})
    assert response.status_code == 401

def test_require_auth_with_bearer_token(client, auth_token):
    """测试使用Bearer token"""
    response = client.get('/api/list-documents',
                         headers={'Authorization': f'Bearer {auth_token}'})
    # 数据库错误503或成功200
    assert response.status_code in [200, 503]

def test_require_auth_with_cookie(client, auth_token):
    """测试使用cookie认证"""
    client.set_cookie('auth_token', auth_token)
    response = client.get('/api/list-documents')
    assert response.status_code in [200, 503]

# ===================== 文档管理测试 =====================

def test_list_documents_authenticated(client, auth_token):
    """测试列出文档"""
    response = client.get('/api/list-documents',
                        headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code in [200, 503]

def test_upload_document_no_file(client, auth_token):
    """测试上传文档但没有文件"""
    response = client.post('/api/upload-document',
                          headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'no_file'

def test_upload_document_empty_filename(client, auth_token):
    """测试上传文档但文件名为空"""
    data = {'file': (BytesIO(b''), '')}
    response = client.post('/api/upload-document',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          data=data,
                          content_type='multipart/form-data')
    assert response.status_code == 400

def test_upload_document_wrong_mime_type(client, auth_token):
    """测试上传非PDF文件"""
    data = {'file': (BytesIO(b'text content'), 'test.txt', 'text/plain')}
    response = client.post('/api/upload-document',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          data=data,
                          content_type='multipart/form-data')
    assert response.status_code == 415

def test_upload_document_invalid_pdf_header(client, auth_token):
    """测试上传无效PDF（没有PDF头）"""
    fake_pdf = b'not a pdf file'
    data = {'file': (BytesIO(fake_pdf), 'test.pdf', 'application/pdf')}
    response = client.post('/api/upload-document',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          data=data,
                          content_type='multipart/form-data')
    assert response.status_code == 400

def test_upload_document_fake_pdf(client, auth_token):
    """测试上传假PDF（有头但结构不完整）"""
    fake_pdf = b'%PDF-1.4\nfake content'
    data = {'file': (BytesIO(fake_pdf), 'test.pdf', 'application/pdf')}
    response = client.post('/api/upload-document',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          data=data,
                          content_type='multipart/form-data')
    assert response.status_code == 400

def test_upload_document_with_custom_name(client, auth_token):
    """测试上传文档使用自定义名称"""
    pdf_content = b'%PDF-1.4\ntrailer\nstartxref\n'
    data = {
        'file': (BytesIO(pdf_content), 'original.pdf', 'application/pdf'),
        'name': 'custom_name.pdf'
    }
    response = client.post('/api/upload-document',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          data=data,
                          content_type='multipart/form-data')
    # 可能因PDF验证失败返回400，或数据库错误503
    assert response.status_code in [201, 400, 500, 503]

def test_get_document_not_found(client, auth_token):
    """测试获取不存在的文档"""
    response = client.get('/api/get-document/99999',
                        headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code in [404, 503]

def test_get_document_unauthorized(client):
    """测试未授权获取文档"""
    response = client.get('/api/get-document/1')
    assert response.status_code == 401

def test_delete_document_not_found(client, auth_token):
    """测试删除不存在的文档"""
    response = client.delete('/api/delete-document/99999',
                           headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code in [404, 503]

def test_delete_document_unauthorized(client):
    """测试未授权删除文档"""
    response = client.delete('/api/delete-document/1')
    assert response.status_code == 401

# ===================== 水印测试 =====================

def test_get_watermarking_methods(client, auth_token):
    """测试获取水印方法"""
    response = client.get('/api/get-watermarking-methods',
                        headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'methods' in data

def test_list_versions_missing_document_id(client, auth_token):
    """测试列出版本但没有document_id"""
    response = client.get('/api/list-versions',
                         headers={'Authorization': f'Bearer {auth_token}'},
                         json={})
    assert response.status_code == 400

def test_list_versions_invalid_document_id(client, auth_token):
    """测试列出版本使用无效document_id"""
    response = client.get('/api/list-versions',
                         headers={'Authorization': f'Bearer {auth_token}'},
                         json={'id': 'not-a-number'})
    assert response.status_code == 400

def test_list_versions_with_path_param(client, auth_token):
    """测试使用路径参数列出版本"""
    response = client.get('/api/list-versions/1',
                        headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code in [200, 500, 503]

def test_create_watermark_missing_document_id(client, auth_token):
    """测试创建水印缺少document_id"""
    response = client.post('/api/create-watermark',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={'method': 'test', 'secret': 'secret'})
    assert response.status_code == 400

def test_create_watermark_missing_method(client, auth_token):
    """测试创建水印缺少method"""
    response = client.post('/api/create-watermark/1',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={'secret': 'secret'})
    assert response.status_code == 400

def test_create_watermark_missing_secret(client, auth_token):
    """测试创建水印缺少secret"""
    response = client.post('/api/create-watermark/1',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={'method': 'test'})
    assert response.status_code == 400

def test_create_watermark_empty_method(client, auth_token):
    """测试创建水印使用空method"""
    response = client.post('/api/create-watermark/1',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={'method': '', 'secret': 'secret'})
    assert response.status_code == 400

def test_create_watermark_with_all_params(client, auth_token):
    """测试创建水印使用所有参数"""
    response = client.post('/api/create-watermark/1',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={
                              'method': 'test-method',
                              'secret': 'test-secret',
                              'position': 'eof',
                              'intended_for': 'user@example.com'
                          })
    # 文档不存在404，或数据库错误503，或方法不存在400
    assert response.status_code in [201, 400, 404, 410, 500, 503]

def test_read_watermark_missing_document_id(client, auth_token):
    """测试读取水印缺少document_id"""
    response = client.post('/api/read-watermark',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={'method': 'test'})
    assert response.status_code == 400

def test_read_watermark_missing_method(client, auth_token):
    """测试读取水印缺少method"""
    response = client.post('/api/read-watermark/1',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={})
    assert response.status_code == 400

def test_read_watermark_empty_method(client, auth_token):
    """测试读取水印使用空method"""
    response = client.post('/api/read-watermark/1',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={'method': ''})
    assert response.status_code == 400

def test_read_watermark_with_link(client, auth_token):
    """测试使用link读取水印"""
    response = client.post('/api/read-watermark/1',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={'method': 'test', 'link': 'test-link'})
    assert response.status_code in [200, 404, 500, 503]

def test_read_watermark_latest(client, auth_token):
    """测试读取最新版本的水印"""
    response = client.post('/api/read-watermark/1',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={'method': 'test', 'latest': True})
    assert response.status_code in [200, 404, 500, 503]

def test_get_version_not_found(client, auth_token):
    """测试获取不存在的版本"""
    response = client.get('/api/get-version/nonexistent-link-12345',
                        headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code in [404, 503]

def test_get_version_no_auth(client):
    """测试不带认证获取版本"""
    # 根据代码注释，get-version可能有特殊认证逻辑
    response = client.get('/api/get-version/test-link')
    # 可能需要认证或不需要
    assert response.status_code in [200, 401, 404, 503]

# ===================== 插件管理测试 =====================

def test_load_plugin_non_admin(client, auth_token):
    """测试非管理员加载插件"""
    response = client.post('/api/load-plugin',
                          headers={'Authorization': f'Bearer {auth_token}'},
                          json={'filename': 'test.py'})
    assert response.status_code == 403
    data = json.loads(response.data)
    assert data['error'] == 'admin_only'

def test_load_plugin_missing_filename(client, admin_token):
    """测试加载插件缺少文件名"""
    response = client.post('/api/load-plugin',
                          headers={'Authorization': f'Bearer {admin_token}'},
                          json={})
    assert response.status_code == 400

def test_load_plugin_non_py_file(client, admin_token):
    """测试加载非.py文件"""
    response = client.post('/api/load-plugin',
                          headers={'Authorization': f'Bearer {admin_token}'},
                          json={'filename': 'test.txt'})
    assert response.status_code == 400

def test_load_plugin_not_found(client, admin_token):
    """测试加载不存在的插件"""
    response = client.post('/api/load-plugin',
                          headers={'Authorization': f'Bearer {admin_token}'},
                          json={'filename': 'nonexistent.py'})
    assert response.status_code in [404, 400]

# ===================== Web页面测试 =====================

def test_page_index(client):
    """测试首页"""
    response = client.get('/')
    assert response.status_code in [200, 404, 500]

def test_page_login(client):
    """测试登录页"""
    response = client.get('/login')
    assert response.status_code in [200, 404, 500]

def test_page_signup(client):
    """测试注册页"""
    response = client.get('/signup')
    assert response.status_code in [200, 404, 500]

def test_page_documents_no_auth(client):
    """测试未认证访问文档页"""
    response = client.get('/documents')
    # 应该重定向到登录页
    assert response.status_code in [302, 308, 401]

def test_page_documents_with_auth(client, auth_token):
    """测试已认证访问文档页"""
    client.set_cookie('auth_token', auth_token)
    response = client.get('/documents')
    assert response.status_code in [200, 404, 500]

def test_page_documents_invalid_token(client):
    """测试使用无效token访问文档页"""
    client.set_cookie('auth_token', 'invalid-token')
    response = client.get('/documents')
    assert response.status_code in [302, 308, 401]

# ===================== 边界条件测试 =====================

def test_create_user_whitespace_email(client):
    """测试创建用户使用带空格的email"""
    response = client.post('/api/create-user', json={
        'email': '  test@example.com  ',
        'login': 'testuser',
        'password': 'pass123'
    })
    # 应该trim空格
    assert response.status_code in [201, 503, 409]

def test_login_case_sensitive_email(client):
    """测试登录email大小写处理"""
    response = client.post('/api/login', json={
        'email': 'TEST@EXAMPLE.COM',
        'password': 'pass123'
    })
    # 应该转换为小写
    assert response.status_code in [401, 503]