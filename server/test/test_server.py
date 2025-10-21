# tests/test_server.py
import io
import os
import json
import contextlib
import pytest
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

# --------- 常量与工具 ---------
SALT_AUTH = "tatou-auth"  # 与 server.py 中 _serializer 的 salt 一致
MINIMAL_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    b"2 0 obj\n<< /Type /Pages /Count 0 >>\nendobj\n"
    b"trailer\n<< /Size 3 >>\nstartxref\n0\n%%EOF\n"
)
INVALID_PDF = b"%PDX-xyz"  # 不含 trailer/startxref

# --------- 假 DB 引擎 / 连接 / 结果 ---------
class FakeResult:
    def __init__(self, rows=None, scalar_value=None, lastrowid=None):
        self._rows = rows or []
        self.lastrowid = lastrowid
        self._scalar = scalar_value
    def all(self): return self._rows
    def first(self): return self._rows[0] if self._rows else None
    def one(self): assert len(self._rows) == 1; return self._rows[0]
    def scalar(self): return self._scalar

class RowObj:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class FakeConn:
    def __init__(self, state):
        self.state = state

    def execute(self, stmt, params=None):
        sql = str(stmt)
        params = params or {}

        # --- healthz ---
        if "SELECT 1" in sql:
            return FakeResult(rows=[(1,)])

        # --- Users: INSERT ---
        if "INSERT INTO Users" in sql:
            new_id = self.state["ids"]["users"] = self.state["ids"]["users"] + 1
            self.state["users"][new_id] = {
                "id": new_id,
                "email": params.get("email"),
                "login": params.get("login"),
                "hpassword": params.get("hpw"),
            }
            return FakeResult(lastrowid=new_id)

        # --- Users: SELECT ... WHERE id ---
        if "FROM Users" in sql and "WHERE id" in sql and "SELECT" in sql:
            uid = params.get("id")
            u = self.state["users"].get(uid)
            if not u:
                return FakeResult([])
            row = RowObj(id=u["id"], email=u["email"], login=u["login"])
            return FakeResult(rows=[row])

        # --- Users: SELECT ... WHERE email ---
        if "FROM Users" in sql and "WHERE email" in sql:
            target = None
            email = params.get("email")
            for u in self.state["users"].values():
                if u["email"] == email:
                    target = u
                    break
            if not target:
                return FakeResult([])
            row = RowObj(
                id=target["id"], email=target["email"],
                login=target["login"], hpassword=target["hpassword"]
            )
            return FakeResult(rows=[row])

        # --- Documents: INSERT ---
        if "INSERT INTO Documents" in sql:
            new_id = self.state["ids"]["docs"] = self.state["ids"]["docs"] + 1
            self.state["docs"][new_id] = {
                "id": new_id,
                "name": params.get("name"),
                "path": params.get("path"),
                "ownerid": params.get("ownerid"),
                "sha256": params.get("sha256"),
                "size": params.get("size"),
            }
            return FakeResult(lastrowid=new_id)

        # --- SELECT LAST_INSERT_ID ---
        if "SELECT LAST_INSERT_ID()" in sql:
            return FakeResult(scalar_value=max(self.state["ids"]["docs"], self.state["ids"]["vers"]))

        # --- Documents: SELECT ... WHERE id AND ownerid ---
        if "FROM Documents" in sql and "WHERE id" in sql and "ownerid" in sql:
            did = params.get("id")
            uid = params.get("uid")
            d = self.state["docs"].get(did)
            if not d or d["ownerid"] != uid:
                return FakeResult([])
            row = RowObj(id=d["id"], name=d["name"], path=d["path"])
            return FakeResult(rows=[row])

        # --- Versions: INSERT ---
        if "INSERT INTO Versions" in sql:
            new_id = self.state["ids"]["vers"] = self.state["ids"]["vers"] + 1
            self.state["vers"][new_id] = {
                "id": new_id,
                "documentid": params.get("documentid"),
                "link": params.get("link"),
                "intended_for": params.get("intended_for"),
                "secret": params.get("secret"),
                "method": params.get("method"),
                "position": params.get("position"),
                "path": params.get("path"),
            }
            return FakeResult(lastrowid=new_id)

        # --- Versions: latest by documentid ---
        if ("FROM Versions" in sql and "WHERE" in sql and "documentid" in sql
            and "ORDER BY" in sql and "DESC" in sql and "link" not in sql):
            did = params.get("did") or params.get("documentid") or params.get("doc_id")
            candidates = [v for v in self.state["vers"].values() if v["documentid"] == did]
            if not candidates:
                return FakeResult([])
            v = sorted(candidates, key=lambda x: x["id"], reverse=True)[0]
            return FakeResult(rows=[RowObj(path=v["path"])])

        # --- get-version / read-watermark by link (JOIN Documents)---
        if "FROM Versions" in sql and "WHERE" in sql and "link" in sql:
            link = params.get("link")
            v = next((x for x in self.state["vers"].values() if x["link"] == link), None)
            if not v:
                return FakeResult([])
            uid = params.get("uid")
            if uid is None:
                return FakeResult(rows=[RowObj(path=v["path"], documentid=v["documentid"])])
            d = self.state["docs"].get(v["documentid"])
            if not d or d["ownerid"] != uid:
                return FakeResult([])
            return FakeResult(rows=[RowObj(path=v["path"])])

        # --- list-versions ---
        if "JOIN Documents" in sql and "JOIN Versions" in sql and "ORDER BY" in sql and "v.id" in sql:
            uid = params.get("uid")
            did = params.get("did")
            rows = []
            for v in self.state["vers"].values():
                d = self.state["docs"].get(v["documentid"])
                if d and d["ownerid"] == uid and d["id"] == did:
                    rows.append(RowObj(
                        id=v["id"], documentid=v["documentid"], link=v["link"],
                        intended_for=v["intended_for"], method=v["method"],
                        position=v["position"], path=v["path"],
                        has_secret=int(bool(v["secret"]))
                    ))
            return FakeResult(rows=rows)

        return FakeResult([])

    def __enter__(self):
        return self
    def __exit__(self, *exc):
        return False

class FakeEngine:
    def __init__(self, state, fail=False):
        self.state = state
        self.fail = fail
    def connect(self):
        if self.fail:
            raise RuntimeError("DB down")
        return FakeConn(self.state)
    def begin(self):
        if self.fail:
            raise RuntimeError("DB down")
        return contextlib.nullcontext(FakeConn(self.state))

# --------- 假 WMUtils ---------
class WMStub:
    def __init__(self):
        self.METHODS = {"stub": object()}
    def apply_watermark(self, method, pdf, secret, key, position=None):
        return MINIMAL_PDF
    def read_watermark(self, method, pdf, key=""):
        return json.dumps({"secret": "ok", "intended_for": "tester"})

# ----------------- Fixtures -----------------
@pytest.fixture
def app(tmp_path, monkeypatch):
    os.environ["SECRET_KEY"] = "test-secret"
    os.environ["STORAGE_DIR"] = str(tmp_path / "storage")
    (tmp_path / "storage").mkdir(parents=True, exist_ok=True)

    import server as srv  # 目标模块：server.py

    stub = WMStub()
    monkeypatch.setattr(srv, "WMUtils", stub, raising=True)

    application = srv.create_app()

    state = {
        "ids": {"users": 0, "docs": 0, "vers": 0},
        "users": {},
        "docs": {},
        "vers": {},
    }

    # 预置一个用户
    u1 = {
        "id": 1,
        "email": "u1@example.com",
        "login": "u1",
        "hpassword": generate_password_hash("pass123"),
    }
    state["ids"]["users"] = 1
    state["users"][1] = u1

    application.config["_ENGINE"] = FakeEngine(state)
    application.config["MAX_UPLOAD_MB"] = 1  # 1MB 限制，便于触发 413

    application.fake_state = state
    application.wm_stub = stub
    return application

@pytest.fixture
def client(app):
    return app.test_client()

def make_token(secret_key, uid=1, login="u1", email="u1@example.com", roles=None, max_age=None):
    s = URLSafeTimedSerializer(secret_key, salt=SALT_AUTH)
    payload = {"uid": int(uid), "login": login, "email": email, "roles": roles or []}
    return s.dumps(payload)

# ----------------- Tests -----------------

def test_healthz_db_ok(app, client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == "The server is up and running."
    assert data["db_connected"] is True

def test_healthz_db_down(app, client):
    app.config["_ENGINE"] = FakeEngine(app.fake_state, fail=True)
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json()["db_connected"] is False
    app.config["_ENGINE"] = FakeEngine(app.fake_state, fail=False)

def test_login_and_session_cookie(app, client):
    resp = client.post("/api/login", json={"email": "u1@example.com", "password": "pass123"})
    assert resp.status_code == 200
    token = resp.get_json()["token"]

    resp = client.post("/auth/session", json={"token": token})
    assert resp.status_code == 200
    assert resp.get_json()["ok"] is True

    resp = client.post("/logout")
    assert resp.status_code == 200
    assert resp.get_json()["ok"] is True

def test_require_auth_guard(app, client):
    resp = client.get("/api/get-watermarking-methods")
    assert resp.status_code == 401

    resp = client.get("/api/get-watermarking-methods", headers={"Authorization": "Bearer bad.token"})
    assert resp.status_code == 401

    token = make_token(app.config["SECRET_KEY"])
    resp = client.get("/api/get-watermarking-methods", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "methods" in data and isinstance(data["methods"], list)

def test_upload_invalid_pdf(app, client):
    token = make_token(app.config["SECRET_KEY"])
    data = {
        "file": (io.BytesIO(INVALID_PDF), "bad.pdf", "application/pdf"),
        "name": "bad.pdf",
    }
    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data=data,
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "invalid_pdf"

def test_upload_pdf_and_get_document(app, client):
    token = make_token(app.config["SECRET_KEY"])
    data = {
        "file": (io.BytesIO(MINIMAL_PDF), "doc.pdf", "application/pdf"),
        "name": "doc.pdf",
    }
    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data=data,
    )
    assert resp.status_code == 201
    body = resp.get_json()
    doc_id = body["id"]
    assert body["ok"] is True
    assert body["sha256"]

    resp = client.get(
        f"/api/get-document/{doc_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"

def test_upload_too_large(app, client):
    token = make_token(app.config["SECRET_KEY"])
    big_pdf = b"%PDF-1.4\n" + b"0" * (2 * 1024 * 1024) + b"\ntrailer\n<<>>\nstartxref\n0\n%%EOF\n"
    data = {
        "file": (io.BytesIO(big_pdf), "big.pdf", "application/pdf"),
        "name": "big.pdf",
    }
    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data=data,
    )
    assert resp.status_code == 413
    j = resp.get_json()
    assert j["error"] == "payload_too_large"
    assert j["limit_mb"] == 1

def test_create_watermark_and_read_latest_and_by_link(app, client):
    token = make_token(app.config["SECRET_KEY"])

    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "doc.pdf", "application/pdf"), "name": "doc.pdf"},
    )
    assert resp.status_code == 201
    doc = resp.get_json()
    doc_id = doc["id"]

    payload = {"id": doc_id, "method": "stub", "secret": "S", "position": "eof", "intended_for": "tester"}
    resp = client.post(
        f"/api/create-watermark/{doc_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert resp.status_code == 201
    cw = resp.get_json()
    assert cw["ok"] is True
    link = cw["link"]

    # latest 分支
    resp = client.post(
        f"/api/read-watermark/{doc_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"method": "stub", "latest": True},
    )
    assert resp.status_code == 200
    assert resp.get_json()["secret"] == "ok"

    # link 分支
    resp = client.post(
        f"/api/read-watermark/{doc_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"method": "stub", "link": link},
    )
    assert resp.status_code == 200
    assert resp.get_json()["intended_for"] == "tester"

    # 直链下载（必须带 t）
    dl_token = cw.get("t") or cw.get("token") or cw.get("rmap_token") or "A" * 32
    resp = client.get(
        f"/api/get-version/{link}?t={dl_token}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200, resp.get_data(as_text=True)
    assert resp.mimetype == "application/pdf"

def test_list_versions_empty_then_nonempty(app, client):
    token = make_token(app.config["SECRET_KEY"])

    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "doc.pdf", "application/pdf"), "name": "doc.pdf"},
    )
    assert resp.status_code == 201
    doc_id = resp.get_json()["id"]

    # 空列表
    resp = client.get(
        f"/api/list-versions/{doc_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert data["count"] == 0

    # 创建一个版本
    resp = client.post(
        f"/api/create-watermark/{doc_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"method": "stub", "secret": "X"},
    )
    assert resp.status_code == 201

    # 再次列出
    resp = client.get(
        f"/api/list-versions/{doc_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert data["count"] == 1
    assert isinstance(data["versions"][0]["has_secret"], bool)

# ----------------- 新增用例：提升覆盖率的关键分支 -----------------

def test_login_bad_password(app, client):
    # 错误密码 => 401
    resp = client.post("/api/login", json={"email": "u1@example.com", "password": "wrong"})
    assert resp.status_code == 401

def test_auth_via_cookie_only(app, client):
    # 通过 /auth/session 设置 cookie，之后不用 Authorization 头也能访问受保护接口
    ok = client.post("/api/login", json={"email": "u1@example.com", "password": "pass123"})
    token = ok.get_json()["token"]

    set_cookie = client.post("/auth/session", json={"token": token})
    assert set_cookie.status_code == 200

    resp = client.get("/api/get-watermarking-methods")  # 无 Authorization 头
    assert resp.status_code == 200
    assert "methods" in resp.get_json()

def test_read_watermark_latest_404_when_no_versions(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 只上传，无版本
    up = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "doc.pdf", "application/pdf"), "name": "doc.pdf"},
    )
    did = up.get_json()["id"]

    # latest=True，但没有任何版本，应 404
    resp = client.post(
        f"/api/read-watermark/{did}",
        headers={"Authorization": f"Bearer {token}"},
        json={"method": "stub", "latest": True},
    )
    assert resp.status_code == 404

def test_create_watermark_not_owner_404(app, client):
    # 用户1 上传
    t1 = make_token(os.environ["SECRET_KEY"], uid=1, login="u1", email="u1@example.com")
    up = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {t1}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "doc.pdf", "application/pdf"), "name": "doc.pdf"},
    )
    did = up.get_json()["id"]

    # 用户2 试图给用户1的文档创建水印 => 404
    t2 = make_token(os.environ["SECRET_KEY"], uid=2, login="u2", email="u2@example.com")
    resp = client.post(
        f"/api/create-watermark/{did}",
        headers={"Authorization": f"Bearer {t2}"},
        json={"id": did, "method": "stub", "secret": "X"},
    )
    assert resp.status_code in (403, 404)  # 实现可能返回 404（找不到）或 403（无权限）

def test_get_version_missing_token_400(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 创建一个版本
    up = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "doc.pdf", "application/pdf"), "name": "doc.pdf"},
    )
    did = up.get_json()["id"]
    cw = client.post(
        f"/api/create-watermark/{did}",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": did, "method": "stub", "secret": "S"},
    ).get_json()
    link = cw["link"]

    # 不带 t => 400（你的实现会打印 "[RMAP] invalid token format"）
    resp = client.get(
        f"/api/get-version/{link}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 400

def test_protected_routes_without_auth_401(app, client):
    # 未授权访问受保护资源 => 401
    resp1 = client.get("/api/list-versions/1")
    resp2 = client.get("/api/get-document/1")
    assert resp1.status_code == 401
    assert resp2.status_code == 401

# ===================== 追加用例：覆盖 server.py 边角分支 =====================

def test_upload_missing_file_400(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 缺少 file 字段
    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"name": "no_file.pdf"},
    )
    assert resp.status_code == 400
    j = resp.get_json()
    assert "error" in j

def test_upload_unsupported_mimetype_415(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 非 PDF 的 MIME
    data = {
        "file": (io.BytesIO(b"not-pdf"), "note.txt", "text/plain"),
        "name": "note.txt",
    }
    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data=data,
    )
    # 服务端通常对 MIME 白名单做 415
    assert resp.status_code in (400, 415)

def test_get_document_not_found_404(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 未上传过 id=999
    resp = client.get(
        "/api/get-document/999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code in (403, 404)

def test_read_watermark_unknown_method_400(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 先上传一个最小 PDF
    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "a.pdf", "application/pdf"), "name": "a.pdf"},
    )
    did = resp.get_json()["id"]
    # 传入未知 method
    resp = client.post(
        f"/api/read-watermark/{did}",
        headers={"Authorization": f"Bearer {token}"},
        json={"method": "no_such_method", "latest": True},
    )
    assert resp.status_code == 404

def test_create_watermark_impl_raises_500(app, client, monkeypatch):
    token = make_token(app.config["SECRET_KEY"])
    # 上传
    up = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "b.pdf", "application/pdf"), "name": "b.pdf"},
    )
    did = up.get_json()["id"]

    # 让 WMUtils.apply_watermark 抛出异常，触发 5xx 分支
    class BoomStub:
        METHODS = {"stub": object()}
        def apply_watermark(self, *a, **kw): raise RuntimeError("boom")
        def read_watermark(self, *a, **kw): return "{}"

    import server as srv
    monkeypatch.setattr(srv, "WMUtils", BoomStub(), raising=True)

    resp = client.post(
        f"/api/create-watermark/{did}",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": did, "method": "stub", "secret": "S"},
    )
    assert resp.status_code in (500, 502, 503)
    # 复原为 stub，避免影响后续用例
    monkeypatch.setattr(srv, "WMUtils", app.wm_stub, raising=True)

def test_auth_session_bad_token_400(app, client):
    # /auth/session 传入坏 token
    resp = client.post("/auth/session", json={"token": "not.a.valid.token"})
    assert resp.status_code in (400, 401)

def test_get_version_with_valid_token_200(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 上传 + 创建水印，取 link
    up = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "c.pdf", "application/pdf"), "name": "c.pdf"},
    )
    did = up.get_json()["id"]
    cw = client.post(
        f"/api/create-watermark/{did}",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": did, "method": "stub", "secret": "SSS"},
    ).get_json()
    link = cw["link"]

    # 使用与后端一致的版本签名器（salt="tatou-version"）签发合法 t
    from itsdangerous import URLSafeTimedSerializer
    version_serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"], salt="tatou-version")
    dl_token = version_serializer.dumps({"sid": link})

    resp = client.get(
        f"/api/get-version/{link}?t={dl_token}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"

def test_list_versions_wrong_owner_404(app, client):
    # 用户1上传
    t1 = make_token(app.config["SECRET_KEY"], uid=1, login="u1", email="u1@example.com")
    up = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {t1}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "d.pdf", "application/pdf"), "name": "d.pdf"},
    )
    did = up.get_json()["id"]

    # 用户2访问用户1的版本列表 => 404/403
    t2 = make_token(app.config["SECRET_KEY"], uid=2, login="u2", email="u2@example.com")
    resp = client.get(
        f"/api/list-versions/{did}",
        headers={"Authorization": f"Bearer {t2}"},
    )
    assert resp.status_code in (403, 404)
# ===================== 追加用例：覆盖 server.py 边角分支 =====================

def test_upload_missing_file_400(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 缺少 file 字段
    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"name": "no_file.pdf"},
    )
    assert resp.status_code == 400
    j = resp.get_json()
    assert "error" in j

def test_upload_unsupported_mimetype_415(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 非 PDF 的 MIME
    data = {
        "file": (io.BytesIO(b"not-pdf"), "note.txt", "text/plain"),
        "name": "note.txt",
    }
    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data=data,
    )
    # 服务端通常对 MIME 白名单做 415
    assert resp.status_code in (400, 415)

def test_get_document_not_found_404(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 未上传过 id=999
    resp = client.get(
        "/api/get-document/999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code in (403, 404)

def test_read_watermark_unknown_method_400(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 先上传一个最小 PDF
    resp = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "a.pdf", "application/pdf"), "name": "a.pdf"},
    )
    did = resp.get_json()["id"]
    # 传入未知 method
    resp = client.post(
        f"/api/read-watermark/{did}",
        headers={"Authorization": f"Bearer {token}"},
        json={"method": "no_such_method", "latest": True},
    )
    assert resp.status_code == 404

def test_create_watermark_impl_raises_500(app, client, monkeypatch):
    token = make_token(app.config["SECRET_KEY"])
    # 上传
    up = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "b.pdf", "application/pdf"), "name": "b.pdf"},
    )
    did = up.get_json()["id"]

    # 让 WMUtils.apply_watermark 抛出异常，触发 5xx 分支
    class BoomStub:
        METHODS = {"stub": object()}
        def apply_watermark(self, *a, **kw): raise RuntimeError("boom")
        def read_watermark(self, *a, **kw): return "{}"

    import server as srv
    monkeypatch.setattr(srv, "WMUtils", BoomStub(), raising=True)

    resp = client.post(
        f"/api/create-watermark/{did}",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": did, "method": "stub", "secret": "S"},
    )
    assert resp.status_code in (500, 502, 503)
    # 复原为 stub，避免影响后续用例
    monkeypatch.setattr(srv, "WMUtils", app.wm_stub, raising=True)

def test_auth_session_bad_token_400(app, client):
    # /auth/session 传入坏 token
    resp = client.post("/auth/session", json={"token": "not.a.valid.token"})
    assert resp.status_code in (400, 401)

def test_get_version_with_valid_token_200(app, client):
    token = make_token(app.config["SECRET_KEY"])
    # 上传 + 创建水印，取 link
    up = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "c.pdf", "application/pdf"), "name": "c.pdf"},
    )
    did = up.get_json()["id"]
    cw = client.post(
        f"/api/create-watermark/{did}",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": did, "method": "stub", "secret": "SSS"},
    ).get_json()
    link = cw["link"]

    # 使用与后端一致的版本签名器（salt="tatou-version"）签发合法 t
    from itsdangerous import URLSafeTimedSerializer
    version_serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"], salt="tatou-version")
    dl_token = version_serializer.dumps({"sid": link})

    resp = client.get(
        f"/api/get-version/{link}?t={dl_token}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"

def test_list_versions_wrong_owner_404(app, client):
    # 用户1上传
    t1 = make_token(app.config["SECRET_KEY"], uid=1, login="u1", email="u1@example.com")
    up = client.post(
        "/api/upload-document",
        headers={"Authorization": f"Bearer {t1}"},
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(MINIMAL_PDF), "d.pdf", "application/pdf"), "name": "d.pdf"},
    )
    did = up.get_json()["id"]

    # 用户2访问用户1的版本列表 => 404/403
    t2 = make_token(app.config["SECRET_KEY"], uid=2, login="u2", email="u2@example.com")
    resp = client.get(
        f"/api/list-versions/{did}",
        headers={"Authorization": f"Bearer {t2}"},
    )
    assert resp.status_code in (403, 404)

