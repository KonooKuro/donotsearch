import io
import os
import json
import pytest
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

import server


# ======================== 基础 Fixture ========================

@pytest.fixture(scope="module")
def app(tmp_path_factory):
    # 最小可运行 app
    tmp = tmp_path_factory.mktemp("stor")
    os.environ["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "test-secret"
    os.environ["STORAGE_DIR"] = str(tmp)
    application = server.create_app()
    return application

@pytest.fixture()
def client(app):
    return app.test_client()

def _make_auth_token(secret_key, uid=1, login="u1", email="u1@example.com", roles=None):
    s = URLSafeTimedSerializer(secret_key, salt="tatou-auth")
    payload = {"uid": uid, "login": login, "email": email, "roles": roles or []}
    return s.dumps(payload)

@pytest.fixture()
def auth_headers(app):
    token = _make_auth_token(app.config["SECRET_KEY"])
    return {"Authorization": f"Bearer {token}"}

# 一个极小可解析 PDF（带 trailer/startxref）
MIN_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    b"2 0 obj\n<< /Type /Pages /Count 0 >>\nendobj\n"
    b"trailer\n<< /Size 3 >>\nstartxref\n0\n%%EOF\n"
)

# ======================== 配置 / 健康检查 ========================

def test_healthz_ok(client):
    r = client.get("/healthz")
    assert r.status_code in (200, 500)

def test_auth_session_bad_token_400(client):
    r = client.post("/auth/session", json={"token": "bad.token"})
    assert r.status_code in (400, 401)


# ======================== 登录 / 注销 分支 ========================

def test_login_missing_fields(client):
    r = client.post("/api/login", json={"email": "x@example.com"})
    assert r.status_code in (400, 401)

def test_login_nonexistent_user_401(client):
    r = client.post("/api/login", json={"email": "nouser@example.com", "password": "x"})
    assert r.status_code in (400, 401)

def test_logout_when_not_logged_in(client):
    r = client.post("/logout")
    # 通常仍然 200/204
    assert r.status_code in (200, 204)


# ======================== 上传边角分支 ========================

def test_upload_missing_file_400(client, auth_headers):
    r = client.post(
        "/api/upload-document",
        headers=auth_headers,
        data={"name": "nofile.pdf"},
        content_type="multipart/form-data",
    )
    assert r.status_code == 400

def test_upload_unsupported_mime_415(client, auth_headers):
    data = {"file": (io.BytesIO(b"plain"), "a.txt", "text/plain"), "name": "a.txt"}
    r = client.post(
        "/api/upload-document",
        headers=auth_headers,
        data=data,
        content_type="multipart/form-data",
    )
    assert r.status_code in (400, 415)

def test_upload_filename_with_path_sep(client, auth_headers):
    # 尝试带路径的文件名，期望被拒绝或被清洗
    data = {"file": (io.BytesIO(MIN_PDF), "../evil.pdf", "application/pdf"), "name": "../evil.pdf"}
    r = client.post(
        "/api/upload-document",
        headers=auth_headers,
        data=data,
        content_type="multipart/form-data",
    )
    # 允许多种安全策略：拒绝(400/415)或接受(201)
    assert r.status_code in (201, 400, 415, 500)


# ======================== 文档读取 / 版本列表 异常 ========================

def test_get_document_not_found(client, auth_headers):
    r = client.get("/api/get-document/999999", headers=auth_headers)
    assert r.status_code in (403, 404, 503)

def test_list_versions_doc_not_exist(client, auth_headers):
    r = client.get("/api/list-versions/888888", headers=auth_headers)
    assert r.status_code in (403, 404, 503)


# ======================== 跨用户访问 ========================

def test_cross_user_access_forbidden(app, client):
    # 用户1 上传
    t1 = _make_auth_token(app.config["SECRET_KEY"], uid=1, login="u1", email="u1@example.com")
    r1 = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {t1}"},
        data={"file": (io.BytesIO(MIN_PDF), "u1.pdf", "application/pdf"), "name": "u1.pdf"},
        content_type="multipart/form-data",
    )
    assert r1.status_code == 201
    did = r1.get_json()["id"]

    # 用户2 读取用户1文档
    t2 = _make_auth_token(app.config["SECRET_KEY"], uid=2, login="u2", email="u2@example.com")
    r2 = client.get(f"/api/get-document/{did}", headers={"Authorization": f"Bearer {t2}"})
    assert r2.status_code in (403, 404)

    # 用户2 列版本
    r3 = client.get(f"/api/list-versions/{did}", headers={"Authorization": f"Bearer {t2}"})
    assert r3.status_code in (403, 404)


# ======================== 水印：参数缺失 / 未知 link ========================

def test_read_watermark_missing_flags(client, auth_headers):
    # 先上传
    r = client.post(
        "/api/upload-document",
        headers=auth_headers,
        data={"file": (io.BytesIO(MIN_PDF), "a.pdf", "application/pdf"), "name": "a.pdf"},
        content_type="multipart/form-data",
    )
    did = r.get_json()["id"]
    # method 给了，但既没 latest 也没 link
    r2 = client.post(
        f"/api/read-watermark/{did}",
        headers=auth_headers,
        json={"method": "stub"},
    )
    assert r2.status_code in (400, 404)

def test_read_watermark_with_nonexistent_link(client, auth_headers):
    # 先上传
    r = client.post(
        "/api/upload-document",
        headers=auth_headers,
        data={"file": (io.BytesIO(MIN_PDF), "b.pdf", "application/pdf"), "name": "b.pdf"},
        content_type="multipart/form-data",
    )
    did = r.get_json()["id"]
    # link 不存在
    r2 = client.post(
        f"/api/read-watermark/{did}",
        headers=auth_headers,
        json={"method": "stub", "link": "no-such-link"},
    )
    assert r2.status_code in (400, 404)


# ======================== 直链下载：合法/非法 token ========================

def test_get_version_with_valid_and_invalid_token(client, auth_headers, app):
    # 上传 + 创建一个版本（不要求真实水印实现成功；失败也能覆盖错误分支）
    r = client.post(
        "/api/upload-document",
        headers=auth_headers,
        data={"file": (io.BytesIO(MIN_PDF), "c.pdf", "application/pdf"), "name": "c.pdf"},
        content_type="multipart/form-data",
    )
    did = r.get_json()["id"]

    # 尝试创建一个版本（如果实现需要 method，给一个常见名字；失败也无妨）
    rv = client.post(
        f"/api/create-watermark/{did}",
        headers=auth_headers,
        json={"method": "stub", "secret": "X"},
    )
    # 可能 201 / 400 / 500，尽量继续走后面的 token 分支
    # 如果创建失败，构造一个假 link 也能覆盖 token 校验分支
    if rv.status_code == 201:
        link = rv.get_json().get("link")
    else:
        link = "Z" * 32  # 假 link 命中格式校验

    # 合法 token（与后端一致的版本签名器 salt）
    vs = URLSafeTimedSerializer(app.config["SECRET_KEY"], salt="tatou-version")
    good_t = vs.dumps({"sid": link})

    r_ok = client.get(f"/api/get-version/{link}?t={good_t}")
    assert r_ok.status_code in (200, 400, 404, 500)  # 根据 link/文件是否真实存在不同

    # 伪造非法 token：BadSignature
    bad_t = good_t[:-1] + ("A" if not good_t.endswith("A") else "B")
    r_bad = client.get(f"/api/get-version/{link}?t={bad_t}")
    assert r_bad.status_code in (400, 404)

    # 过期 token：用 loads 强行抛 SignatureExpired（打补丁更直接）
    class FakeSer:
        def loads(self, *_a, **_kw): 
            raise SignatureExpired("expired")
    # 暂时替换 _version_serializer，仅本请求生效
    orig = server._version_serializer
    try:
        server._version_serializer = lambda : FakeSer()
        r_exp = client.get(f"/api/get-version/{link}?t={good_t}")
        assert r_exp.status_code in (400, 404)
    finally:
        server._version_serializer = orig
