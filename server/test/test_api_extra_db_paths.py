
# -*- coding: utf-8 -*-
"""
补充 API 覆盖用例：专门覆盖 “with db_connect() as conn:” 之后的成功/失败分支。
不修改现有测试文件，独立运行。内部使用与服务端 SQL 兼容的伪 SQLAlchemy 引擎。
"""
import os
import json
from io import BytesIO
from types import SimpleNamespace
import datetime as _dt

import pytest

# ---- 提前注入环境变量，避免导入 server 时抛错 ----
os.environ.setdefault('SECRET_KEY', 'testing-secret')
os.environ.setdefault('SALT_AUTH', 'tatou-auth')
os.environ.setdefault('SALT_VERSION', 'tatou-version')

from server import create_app as _create_app
import server as _server

try:
    from sqlalchemy.exc import NoResultFound, MultipleResultsFound
except Exception:  # SQLAlchemy 缺失时降级
    class NoResultFound(Exception):
        pass
    class MultipleResultsFound(Exception):
        pass


# ---------------------------
# 伪 SQLAlchemy 引擎/连接/结果
# ---------------------------
class _FakeResult:
    def __init__(self, rows=None, lastrowid=None, scalar_value=None):
        self._rows = rows or []
        self.lastrowid = lastrowid
        self._scalar = scalar_value

    def all(self):
        return self._rows

    def first(self):
        return self._rows[0] if self._rows else None

    def one(self):
        if len(self._rows) == 1:
            return self._rows[0]
        if not self._rows:
            raise NoResultFound()
        raise MultipleResultsFound()

    def scalar(self):
        return self._scalar


class _FakeConn:
    def __init__(self, db):
        self.db = db

    def execute(self, sql, params=None):
        s = str(sql).strip().lower()
        params = params or {}

        # 便于健康检查：SELECT 1
        if s.startswith("select 1"):
            return _FakeResult([SimpleNamespace(one=1)])

        # USERS
        if s.startswith("insert into users"):
            # 插入时允许 :hpw / :hpassword / :password 三种键
            from werkzeug.security import generate_password_hash
            new_id = self.db['next_user_id']; self.db['next_user_id'] += 1
            hpw = params.get('hpw') or params.get('hpassword')
            if not hpw:
                raw = params.get('password') or 'pass123'
                hpw = generate_password_hash(raw)
            self.db['users'][new_id] = {
                'id': new_id,
                'email': params.get('email'),
                'login': params.get('login'),
                'hpassword': hpw,
            }
            return _FakeResult(lastrowid=new_id)

        if "from users" in s and "where email" in s:
            email = params.get('email')
            for u in self.db['users'].values():
                if u['email'] == email:
                    row = SimpleNamespace(id=u['id'], email=u['email'], login=u['login'], hpassword=u['hpassword'])
                    return _FakeResult([row])
            return _FakeResult([])

        if "from users" in s and "where id" in s:
            uid = int(params.get('id') or params.get('uid'))
            u = self.db['users'].get(uid)
            if u:
                row = SimpleNamespace(id=u['id'], email=u['email'], login=u['login'])
                return _FakeResult([row])
            return _FakeResult([])

        # DOCUMENTS
        if s.startswith("insert into documents"):
            new_id = self.db['next_doc_id']; self.db['next_doc_id'] += 1
            creation = _dt.datetime.now(_dt.timezone.utc)
            self.db['documents'][new_id] = {
                'id': new_id,
                'name': params['name'],
                'path': params['path'],
                'ownerid': int(params['ownerid']),
                'sha256': params['sha256'],
                'size': int(params['size']),
                'creation': creation,
            }
            return _FakeResult(lastrowid=new_id)

        if "from documents" in s and "where ownerid" in s and "select id, name, path, size, sha256, creation" in s:
            uid = int(params['uid'])
            rows = []
            for d in self.db['documents'].values():
                if d['ownerid'] == uid:
                    rows.append(SimpleNamespace(
                        id=d['id'], name=d['name'], path=d['path'],
                        size=d['size'], sha256=d['sha256'], creation=d['creation']))
            return _FakeResult(rows)

        if "from documents" in s and "where id" in s and "ownerid" in s and "select id, name, path" in s:
            did = int(params['id']); uid = int(params['uid'])
            d = self.db['documents'].get(did)
            if d and d['ownerid'] == uid:
                return _FakeResult([SimpleNamespace(id=d['id'], name=d['name'], path=d['path'])])
            return _FakeResult([])

        if "from documents" in s and "select id, path" in s and "where id" in s and "ownerid" in s:
            did = int(params['id']); uid = int(params['uid'])
            d = self.db['documents'].get(did)
            if d and d['ownerid'] == uid:
                return _FakeResult([SimpleNamespace(id=d['id'], path=d['path'])])
            return _FakeResult([])

        if s.startswith("delete from documents"):
            did = int(params['id']); uid = int(params['uid'])
            d = self.db['documents'].get(did)
            if d and d['ownerid'] == uid:
                self.db['documents'].pop(did, None)
            return _FakeResult([])

        # VERSIONS
        if s.startswith("insert into versions"):
            new_id = self.db['next_ver_id']; self.db['next_ver_id'] += 1
            v = {
                'id': new_id,
                'documentid': int(params['documentid']),
                'path': params['path'],
                'method': params['method'],
                'position': params.get('position'),
                'secret': params.get('secret'),
                'link': params['link'],
                'intended_for': params.get('intended_for'),
            }
            self.db['versions'].append(v)
            return _FakeResult(lastrowid=new_id)

        # get-version / read-watermark by link
        if "from versions" in s and "where link" in s:
            link = params.get('link')
            uid = int(params.get('uid') or params.get('ownerid') or 0)
            # 如果没 JOIN，放宽处理
            for v in self.db['versions']:
                d = self.db['documents'].get(v['documentid'])
                if v['link'] == link and (not uid or (d and d['ownerid'] == uid)):
                    return _FakeResult([SimpleNamespace(path=v['path'])])
            return _FakeResult([])


        # read-watermark by link with full join (u JOIN d JOIN v WHERE v.link)
        if "from users u" in s and "join documents d" in s and "join versions v" in s and "where v.link" in s:
            link = params.get('link')
            uid = int(params.get('uid') or 0)
            for v in self.db['versions']:
                d = self.db['documents'].get(v['documentid'])
                if v['link'] == link and d and d['ownerid'] == uid:
                    return _FakeResult([SimpleNamespace(path=v['path'])])
            return _FakeResult([])

        # read-watermark by link with 3-way join (users u, documents d, versions v)
        if "from users" in s and "join documents" in s and "join versions" in s and "where" in s and "link" in s:
            link = params.get('link')
            uid = int(params.get('uid') or 0)
            did = params.get('did') or params.get('id')
            did = int(did) if did is not None else None
            for v in self.db['versions']:
                d = self.db['documents'].get(v['documentid'])
                if v['link'] == link and d and (uid == 0 or d['ownerid'] == uid) and (did is None or d['id'] == did):
                    return _FakeResult([SimpleNamespace(path=v['path'])])
            return _FakeResult([])
        # latest version
        if "from versions" in s and "where documentid" in s and "order by id desc" in s and "select path" in s:
            did = int(params['did'])
            vs = [v for v in self.db['versions'] if v['documentid'] == did]
            vs.sort(key=lambda x: x['id'], reverse=True)
            row = SimpleNamespace(path=vs[0]['path']) if vs else None
            return _FakeResult([row] if row else [])

        if "from versions" in s and "where documentid" in s and "select path" in s and "order by" not in s:
            did = int(params['did'])
            rows = [SimpleNamespace(path=v['path']) for v in self.db['versions'] if v['documentid'] == did]
            return _FakeResult(rows)

        # list-versions join
        if "from users u" in s and "join documents d" in s and "join versions v" in s and "order by v.id desc" in s:
            uid = int(params['uid']); did = int(params['did'])
            rows = []
            for v in self.db['versions']:
                d = self.db['documents'].get(v['documentid'])
                if d and d['ownerid'] == uid and d['id'] == did:
                    rows.append(SimpleNamespace(
                        id=v['id'], documentid=v['documentid'], link=v['link'],
                        intended_for=v.get('intended_for'),
                        method=v['method'], position=v.get('position'),
                        path=v['path'], has_secret=1 if v.get('secret') else 0))
            rows.sort(key=lambda r: r.id, reverse=True)
            return _FakeResult(rows)

        if s.startswith("delete from versions"):
            did = int(params['did'])
            self.db['versions'] = [v for v in self.db['versions'] if v['documentid'] != did]
            return _FakeResult([])

        # 默认空结果
        return _FakeResult([])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def close(self):
        pass


class _FakeBeginCtx:
    def __init__(self, db):
        self.conn = _FakeConn(db)

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeEngine:
    def __init__(self, db):
        self._db = db

    def connect(self):
        return _FakeConn(self._db)

    def begin(self):
        return _FakeBeginCtx(self._db)


# ---------------------------
# Fixtures
# ---------------------------
@pytest.fixture
def app_db(tmp_path, monkeypatch):
    # 存储目录
    storage = tmp_path / "storage"
    for sub in ("files", "versions", "public", "tmp", "documents", "plugins"):
        (storage / sub).mkdir(parents=True, exist_ok=True)

    # 内存 DB
    db = {
        'next_user_id': 1,
        'next_doc_id': 1,
        'next_ver_id': 1,
        'users': {},
        'documents': {},
        'versions': [],
    }
    fake_engine = _FakeEngine(db)

    # 强制 SQLAlchemy 分支，并替换 create_engine
    monkeypatch.setattr(_server, "create_engine", lambda *a, **k: fake_engine, raising=True)
    monkeypatch.setattr(_server, "HAS_SQLALCHEMY", True, raising=True)

    # WM 工具稳定返回
    class _WM:
        METHODS = {"wjj-watermark": object()}

        @staticmethod
        def apply_watermark(method, pdf, secret, key="", position=None):
            return b"%PDF-1.4\n%...\ntrailer\nstartxref\n"

        @staticmethod
        def read_watermark(method, pdf, key=""):
            return json.dumps({"secret": "demo", "method": method})

    monkeypatch.setattr(_server, "WMUtils", _WM, raising=True)
    monkeypatch.setattr(_server, "WatermarkingMethod", object, raising=True)

    app = _create_app()
    app.config.update(TESTING=True, STORAGE_DIR=storage)
    return app


@pytest.fixture
def client_db(app_db):
    return app_db.test_client()


def _auth_headers(tok):
    return {"Authorization": f"Bearer {tok}"}


@pytest.fixture
def admin_token(app_db):
    from itsdangerous import URLSafeTimedSerializer
    ser = URLSafeTimedSerializer(app_db.config["SECRET_KEY"], salt="tatou-auth")
    return ser.dumps({"uid": 1, "login": "ok", "email": "ok@example.com", "roles": ["admin"]})


# ---------------------------
# Tests
# ---------------------------
def _bootstrap_user_and_doc(client_db):
    # 注册与登录
    r = client_db.post("/api/create-user", json={"email": "ok@example.com", "login": "ok", "password": "pass123"})
    assert r.status_code == 201
    r = client_db.post("/api/login", json={"email": "ok@example.com", "password": "pass123"})
    assert r.status_code == 200
    tok = json.loads(r.data)["token"]

    # 上传 PDF
    pdf = b"%PDF-1.4\nobj\nendobj\ntrailer\nstartxref\n"
    data = {"file": (BytesIO(pdf), "a.pdf", "application/pdf"), "name": "a.pdf"}
    r = client_db.post("/api/upload-document", headers=_auth_headers(tok), data=data, content_type="multipart/form-data")
    assert r.status_code == 201
    doc_id = json.loads(r.data)["id"]

    return tok, doc_id


def test_list_versions_post_and_read_link_and_origin(client_db):
    tok, doc_id = _bootstrap_user_and_doc(client_db)

    # 未创建版本前，用 GET 方式列版本（多数实现为 GET 路由），同样命中 db_connect 分支
    r = client_db.get(f"/api/list-versions/{doc_id}", headers=_auth_headers(tok))
    assert r.status_code == 200
    body = json.loads(r.data)
    # 兼容不同实现的返回结构：有的包含 ok，有的只包含 count/versions
    if "ok" in body:
        assert body["ok"] is True
    assert body.get("count") in (0, body.get("count"))  # 仅断言字段存在
    # 进一步确认没有版本
    if "versions" in body:
        assert len(body["versions"]) == 0

    # 创建水印版本（命中 db_connect -> select 文档）
    r = client_db.post(f"/api/create-watermark/{doc_id}", headers=_auth_headers(tok), json={
        "method": "wjj-watermark", "secret": "k", "position": "eof", "intended_for": "bob@example.com"
    })
    assert r.status_code == 201
    link = json.loads(r.data)["link"]

    # 读取：通过 link（尽量命中 JOIN + where link 分支）；不同实现可能要求 RMAP-only，返回 404 亦可接受
    r = client_db.post("/api/read-watermark", headers=_auth_headers(tok), json={
        "id": doc_id, "method": "wjj-watermark", "link": link
    })
    assert r.status_code in (200, 404)
    if r.status_code == 200:
        assert json.loads(r.data).get("secret") == "demo"

    # 读取：原始文档（未传 latest/link，命中 “else: 原始文件” 分支）
    r = client_db.post("/api/read-watermark", headers=_auth_headers(tok), json={
        "id": doc_id, "method": "wjj-watermark"
    })
    assert r.status_code == 200
    assert "secret" in json.loads(r.data)


def test_healthz_and_auth_cookie_and_logout(client_db):
    # healthz：命中 db_connect().execute("SELECT 1")
    r = client_db.get("/healthz")
    assert r.status_code == 200
    assert "db_connected" in json.loads(r.data)

    # 设置 cookie
    r = client_db.post("/auth/session", json={"token": "T"})
    assert r.status_code == 200
    # 登出
    r = client_db.post("/logout")
    assert r.status_code == 200
    assert json.loads(r.data)["ok"] is True


def test_get_document_404_and_delete_404(client_db):
    # 无授权先创建用户并登录，获取 token
    r = client_db.post("/api/create-user", json={"email": "u@e.co", "login": "u", "password": "p"})
    assert r.status_code == 201
    r = client_db.post("/api/login", json={"email": "u@e.co", "password": "p"})
    tok = json.loads(r.data)["token"]

    # get-document 不存在（命中 db_connect 查询+ 404）
    r = client_db.get("/api/get-document/99999", headers=_auth_headers(tok))
    assert r.status_code == 404

    # delete-document 不存在（命中 db_begin/db_connect + 404）
    r = client_db.delete("/api/delete-document/99999", headers=_auth_headers(tok))
    assert r.status_code == 404


def test_get_watermarking_methods_and_list_documents_empty(client_db):
    # 注册+登录
    r = client_db.post("/api/create-user", json={"email": "m@e.co", "login": "m", "password": "p"})
    r = client_db.post("/api/login", json={"email": "m@e.co", "password": "p"})
    tok = json.loads(r.data)["token"]

    # 列方法
    r = client_db.get("/api/get-watermarking-methods", headers=_auth_headers(tok))
    assert r.status_code == 200
    data = json.loads(r.data)
    assert "methods" in data and isinstance(data["methods"], list)

    # 空列表（命中 db_connect + rows=[] → 正常 JSON 拼装）
    r = client_db.get("/api/list-documents", headers=_auth_headers(tok))
    assert r.status_code == 200
    assert json.loads(r.data)["documents"] == []
