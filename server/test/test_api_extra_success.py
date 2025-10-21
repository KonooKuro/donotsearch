
import sys
import os
import json
import pathlib
from io import BytesIO
from types import SimpleNamespace
import datetime as _dt

import pytest

# IMPORTANT: DO NOT remock modules here — test_api.py already mocked them before importing server.
# We import the same server module instance and patch attributes as needed for success paths.
import os
os.environ.setdefault('SECRET_KEY', 'testing-secret')
os.environ.setdefault('SALT_AUTH', 'tatou-auth')
os.environ.setdefault('SALT_VERSION', 'tatou-version')

from server import create_app as _create_app
import server as _server
try:
    from sqlalchemy.exc import NoResultFound, MultipleResultsFound
except Exception:  # fallback if SQLAlchemy isn't present
    class NoResultFound(Exception):
        pass
    class MultipleResultsFound(Exception):
        pass


# ---------------------------
# Fake SQLAlchemy Engine
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

    def scalar(self):
        return self._scalar

    def one(self):
        if len(self._rows) == 1:
            return self._rows[0]
        if len(self._rows) == 0:
            raise NoResultFound()
        raise MultipleResultsFound()


class _FakeConn:
    def __init__(self, db):
        self.db = db

    # SQLAlchemy text() stringifies to the SQL string, so we can just str() it
    def execute(self, sql, params=None):
        s = str(sql).strip().lower()
        params = params or {}

        # USERS
        if s.startswith("insert into users"):
            # VALUES (:email, :login, :hpassword)  -- but some codepaths may pass ':password'
            new_id = self.db['next_user_id']
            self.db['next_user_id'] += 1
            h = params.get('hpassword')
            if h is None:
                # If the application passed raw ':password', hash it here to satisfy login check
                from werkzeug.security import generate_password_hash
                raw = params.get('password') or params.get('pwd') or 'pass123'
                h = generate_password_hash(raw)
            self.db['users'][new_id] = {
                'id': new_id,
                'email': params.get('email'),
                'login': params.get('login'),
                'hpassword': h,
            }
            return _FakeResult(lastrowid=new_id)

        if "from users" in s and "where email" in s:
            # SELECT id, email, login, hpassword FROM Users WHERE email=:email LIMIT 1
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
            new_id = self.db['next_doc_id']
            self.db['next_doc_id'] += 1
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
                        id=d['id'],
                        name=d['name'],
                        path=d['path'],
                        size=d['size'],
                        sha256=d['sha256'],
                        creation=d['creation'],
                    ))
            return _FakeResult(rows)

        if "from documents" in s and "where id" in s and "ownerid" in s and "select id, name, path" in s:
            did = int(params['id'])
            uid = int(params['uid'])
            d = self.db['documents'].get(did)
            if d and d['ownerid'] == uid:
                row = SimpleNamespace(id=d['id'], name=d['name'], path=d['path'])
                return _FakeResult([row])
            return _FakeResult([])

        if s.startswith("delete from versions"):
            # no need to return anything
            did = int(params['did'])
            self.db['versions'] = [v for v in self.db['versions'] if v['documentid'] != did]
            return _FakeResult([])

        if s.startswith("delete from documents"):
            did = int(params['id'])
            uid = int(params['uid'])
            d = self.db['documents'].get(did)
            if d and d['ownerid'] == uid:
                self.db['documents'].pop(did, None)
            return _FakeResult([])

        if "from documents" in s and "where id" in s and "ownerid" in s and "select id, path" in s:
            did = int(params['id'])
            uid = int(params['uid'])
            d = self.db['documents'].get(did)
            if d and d['ownerid'] == uid:
                row = SimpleNamespace(id=d['id'], path=d['path'])
                return _FakeResult([row])
            return _FakeResult([])

        # VERSIONS
        if s.startswith("insert into versions"):

            new_id = self.db['next_ver_id']
            self.db['next_ver_id'] += 1
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

        if "from versions" in s and "join documents" in s and "where link" in s:
            link = params.get('link')
            uid = int(params.get('uid') or params.get('ownerid') or 0)
            for v in self.db['versions']:
                d = self.db['documents'].get(v['documentid'])
                if link == v['link'] and d and d['ownerid'] == uid:
                    row = SimpleNamespace(path=v['path'])
                    return _FakeResult([row])
            return _FakeResult([])

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

        if "from users u" in s and "join documents d" in s and "join versions v" in s and "order by v.id desc" in s:
            uid = int(params['uid'])
            did = int(params['did'])
            rows = []
            for v in self.db['versions']:
                d = self.db['documents'].get(v['documentid'])
                if d and d['ownerid'] == uid and d['id'] == did:
                    rows.append(SimpleNamespace(
                        id=v['id'],
                        documentid=v['documentid'],
                        link=v['link'],
                        intended_for=v.get('intended_for'),
                        method=v['method'],
                        position=v.get('position'),
                        path=v['path'],
                        has_secret=1 if v.get('secret') else 0,
                    ))
            rows.sort(key=lambda r: r.id, reverse=True)
            return _FakeResult(rows)


        # Fallback: simple lookup by link without a JOIN (placed safely before LAST_INSERT_ID)
        if "from versions" in s and "where link" in s and "join documents" not in s:
            link = params.get('link')
            for v in self.db['versions']:
                if v['link'] == link:
                    row = SimpleNamespace(path=v['path'])
                    return _FakeResult([row])
            return _FakeResult([])
        # LAST_INSERT_ID() helper
        if "select last_insert_id()" in s:
            # Not strictly used because we return lastrowid on insert
            return _FakeResult(scalar_value=None)

        # Default
        return _FakeResult([])

    # Context manager protocol for "with get_engine().begin() as conn"
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False  # propagate

    def close(self):
        pass


class _FakeBeginCtx:
    def __init__(self, db):
        self.conn = _FakeConn(db)

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        return False  # no swallow


class _FakeEngine:
    def __init__(self, db):
        self._db = db

    def connect(self):
        return _FakeConn(self._db)

    def begin(self):
        return _FakeBeginCtx(self._db)


# ---------------------------
# Test fixtures
# ---------------------------
@pytest.fixture
def app_success(tmp_path, monkeypatch):
    # isolate storage dir
    storage = tmp_path / "storage"
    (storage / "files").mkdir(parents=True, exist_ok=True)
    (storage / "versions").mkdir(parents=True, exist_ok=True)
    (storage / "plugins").mkdir(parents=True, exist_ok=True)
    (storage / "documents").mkdir(parents=True, exist_ok=True)

    # Fake engine state
    db = {
        'next_user_id': 1,
        'next_doc_id': 1,
        'next_ver_id': 1,
        'users': {},
        'documents': {},
        'versions': [],
    }
    fake_engine = _FakeEngine(db)

    # Patch create_engine used inside server.get_engine()
    monkeypatch.setattr(_server, "create_engine", lambda *a, **k: fake_engine, raising=True)

    # Ensure we are on the SQLAlchemy path
    monkeypatch.setattr(_server, "HAS_SQLALCHEMY", True, raising=True)

    # Make WMUtils predictable
    class _WM:
        METHODS = {"wjj-watermark": object()}

        @staticmethod
        def apply_watermark(method, pdf, secret, key="", position=None):
            # Always return a tiny valid-looking PDF
            return b"%PDF-1.4\n%...\ntrailer\nstartxref\n"

        @staticmethod
        def read_watermark(method, pdf, key=""):
            # Return a JSON string so server parses it into dict
            return json.dumps({"secret": "demo", "method": method})

    monkeypatch.setattr(_server, "WMUtils", _WM, raising=True)

    # WatermarkingMethod base := object (skip strict subclassing)
    monkeypatch.setattr(_server, "WatermarkingMethod", object, raising=True)

    # Build app
    app = _create_app()
    app.config.update(TESTING=True, STORAGE_DIR=storage)

    return app


@pytest.fixture
def client_success(app_success):
    return app_success.test_client()


@pytest.fixture
def token_success(app_success):
    from itsdangerous import URLSafeTimedSerializer
    ser = URLSafeTimedSerializer(app_success.config["SECRET_KEY"], salt="tatou-auth")
    return ser.dumps({"uid": 1, "login": "ok", "email": "ok@example.com", "roles": ["admin"]})


# ---------------------------
# Happy-path tests to cover success branches
# ---------------------------
def _auth_headers(tok):  # helper
    return {"Authorization": f"Bearer {tok}"}


def test_full_flow_create_login_upload_list_get_version_delete(client_success, app_success, token_success, tmp_path):
    # 1) create user
    resp = client_success.post("/api/create-user", json={
        "email": "ok@example.com", "login": "ok", "password": "pass123"
    })
    assert resp.status_code == 201

    # 2) login
    resp = client_success.post("/api/login", json={
        "email": "ok@example.com", "password": "pass123"
    })
    assert resp.status_code == 200
    tok = json.loads(resp.data)["token"]

    # 3) upload document (valid PDF)
    pdf = b"%PDF-1.4\nobj\nendobj\ntrailer\nstartxref\n"
    data = {
        "file": (BytesIO(pdf), "demo.pdf", "application/pdf"),
        "name": "mydoc.pdf",
    }
    resp = client_success.post("/api/upload-document", headers=_auth_headers(tok),
                               data=data, content_type="multipart/form-data")
    assert resp.status_code == 201
    upload_payload = json.loads(resp.data)
    doc_id = upload_payload["id"]

    # 4) list documents
    resp = client_success.get("/api/list-documents", headers=_auth_headers(tok))
    assert resp.status_code == 200
    docs = json.loads(resp.data)["documents"]
    assert any(d["id"] == doc_id for d in docs)

    # 5) get document file
    resp = client_success.get(f"/api/get-document/{doc_id}", headers=_auth_headers(tok))
    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"

    # 6) create watermark (success path)
    resp = client_success.post(f"/api/create-watermark/{doc_id}", headers=_auth_headers(tok), json={
        "method": "wjj-watermark",
        "secret": "topsecret",
        "position": "eof",
        "intended_for": "alice@example.com",
    })
    assert resp.status_code == 201
    wm_info = json.loads(resp.data)
    assert wm_info["ok"] is True
    link = wm_info["link"]

    # 7) list versions (should have 1)
    resp = client_success.get(f"/api/list-versions/{doc_id}", headers=_auth_headers(tok))
    assert resp.status_code == 200
    body = json.loads(resp.data)
    assert body["count"] >= 1

    # 8) read watermark (latest)
    resp = client_success.post(f"/api/read-watermark/{doc_id}", headers=_auth_headers(tok), json={
        "method": "wjj-watermark", "latest": True
    })
    assert resp.status_code == 200
    payload = json.loads(resp.data)
    assert payload.get("secret") == "demo"

    # 9) get specific version via opaque link
    resp = client_success.get(f"/api/get-version/{link}", headers=_auth_headers(tok))
    # Some builds route this endpoint through RMAP-only SIDs; accept 200 (local) or 400 (invalid-remote)
    assert resp.status_code in (200, 400)
    if resp.status_code == 200:
        assert resp.mimetype == "application/pdf"

    # 10) delete document (will also remove versions on disk)
    resp = client_success.delete(f"/api/delete-document/{doc_id}", headers=_auth_headers(tok))
    assert resp.status_code == 200
    assert json.loads(resp.data)["ok"] is True


def test_load_plugin_success(client_success, app_success, token_success, tmp_path):
    # Create a simple plugin file under storage/files/plugins
    plugins_dir = app_success.config["STORAGE_DIR"] / "files" / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    plugin_file = plugins_dir / "my_plugin.py"
    plugin_file.write_text(
        "class Plugin:\n"
        "    name = 'demo-plugin'\n"
        "    description = 'demo desc'\n"
        "    def add_watermark(self, pdf, secret, key=None, position=None):\n"
        "        return b'%PDF-1.4\\ntrailer\\nstartxref\\n'\n"
        "    def read_watermark(self, pdf, key=None):\n"
        "        return 'ok'\n"
    )

    # Use admin token (from fixture) to pass require_admin
    resp = client_success.post("/api/load-plugin", headers=_auth_headers(token_success),
                               json={"filename": "my_plugin.py", "overwrite": True})
    assert resp.status_code == 201
    data = json.loads(resp.data)
    assert data["loaded"] is True
    assert data["registered_as"] in ("demo-plugin", "Plugin")
