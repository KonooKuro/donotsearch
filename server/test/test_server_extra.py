import io
import os
import pytest
from unittest.mock import patch, MagicMock
from itsdangerous import BadSignature, SignatureExpired

import server


@pytest.fixture
def client(app):
    return app.test_client()


# ========== 配置与健康检查分支 ==========

def test_missing_secret_key(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    with pytest.raises(ValueError):
        server.create_app()

def test_healthz_db_down(client, monkeypatch):
    with patch("server.get_engine", side_effect=RuntimeError("DB fail")):
        resp = client.get("/healthz")
        assert resp.status_code == 500
        assert "error" in resp.get_json()


# ========== 用户注册异常 ==========

def test_signup_missing_fields(client):
    r = client.post("/api/create-user", json={"email": "no_login@example.com"})
    assert r.status_code == 400

def test_signup_duplicate_email(client):
    data = {"email": "dup@example.com", "login": "u", "password": "p"}
    r1 = client.post("/api/create-user", json=data)
    r2 = client.post("/api/create-user", json=data)
    assert r2.status_code in (503, 400, 409)


# ========== 上传接口边界 ==========

def test_upload_no_file(client, auth_headers):
    r = client.post("/api/upload-document", headers=auth_headers,
                    data={"name": "nofile"}, content_type="multipart/form-data")
    assert r.status_code == 400

def test_upload_invalid_mime(client, auth_headers):
    data = {"file": (io.BytesIO(b"text"), "a.txt", "text/plain"), "name": "a.txt"}
    r = client.post("/api/upload-document", headers=auth_headers,
                    data=data, content_type="multipart/form-data")
    assert r.status_code in (400, 415)


# ========== 水印异常分支 ==========

def test_watermark_unknown_method(client, auth_headers):
    # 上传一个最小 PDF
    pdf = io.BytesIO(b"%PDF-1.0\n%%EOF")
    r = client.post("/api/upload-document", headers=auth_headers,
                    data={"file": (pdf, "x.pdf", "application/pdf"), "name": "x.pdf"},
                    content_type="multipart/form-data")
    doc_id = r.json["id"]

    # 调用未知 method
    r2 = client.post(f"/api/create-watermark/{doc_id}",
                     headers=auth_headers, json={"method": "no_such", "secret": "S"})
    assert r2.status_code in (400, 500)

def test_watermark_internal_error(client, auth_headers, monkeypatch):
    pdf = io.BytesIO(b"%PDF-1.0\n%%EOF")
    r = client.post("/api/upload-document", headers=auth_headers,
                    data={"file": (pdf, "y.pdf", "application/pdf"), "name": "y.pdf"},
                    content_type="multipart/form-data")
    doc_id = r.json["id"]

    with patch("server.WMUtils.apply_watermark", side_effect=Exception("boom")):
        r2 = client.post(f"/api/create-watermark/{doc_id}",
                         headers=auth_headers, json={"method": "wjj-watermark", "secret": "X"})
        assert r2.status_code in (500, 502, 503)


# ========== Token 错误分支 ==========

def test_token_bad_signature(client, monkeypatch):
    s = server._version_serializer()
    token = s.dumps({"sid": "x"})
    with patch("server._version_serializer", return_value=MagicMock(loads=MagicMock(side_effect=BadSignature("bad")))):
        r = client.get(f"/api/get-version/abc?t={token}")
        assert r.status_code == 400

def test_token_expired_signature(client, monkeypatch):
    s = server._version_serializer()
    token = s.dumps({"sid": "x"})
    with patch("server._version_serializer", return_value=MagicMock(loads=MagicMock(side_effect=SignatureExpired("exp")))):
        r = client.get(f"/api/get-version/abc?t={token}")
        assert r.status_code == 400
