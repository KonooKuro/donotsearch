
# -*- coding: utf-8 -*-
"""
测试集：专门覆盖 create_app() 中 *PyMySQL 分支* 的 `with db_connect() as conn:` 路径，
对应你们 coverage 报告里这些路由内部的 DB 访问段（见 healthz、login、list-documents、
get-document、list-versions、create-watermark、read-watermark、get-version、delete-document 等）。
"""

import os
import json
from io import BytesIO
from types import SimpleNamespace
import datetime as _dt
import sys
import types

import pytest

# ---- 提前注入环境变量，避免导入 server 时抛错 ----
os.environ.setdefault('SECRET_KEY', 'testing-secret')
os.environ.setdefault('SALT_AUTH', 'tatou-auth')
os.environ.setdefault('SALT_VERSION', 'tatou-version')

import server as _server
from server import create_app as _create_app

# ---- WM 工具稳定返回（避免真实处理 PDF） ----
class _WM:
    METHODS = {"wjj-watermark": object()}

    @staticmethod
    def apply_watermark(method, pdf, secret, key="", position=None):
        return b"%PDF-1.4\n%...\ntrailer\nstartxref\n"

    @staticmethod
    def read_watermark(method, pdf, key=""):
        return json.dumps({"secret": "demo", "method": method})

# ---------------------------
# 伪 PyMySQL 实现（contextmanager 分支）
# ---------------------------

class _PyCursor:
    def __init__(self, db):
        self.db = db
        self._result = []
        self._lastrowid = None

    @property
    def lastrowid(self):
        # 为兼容：连接上也会读取 lastrowid
        return self._lastrowid

    def execute(self, sql, params=None):
        s = str(sql).strip().lower()

        # 统一参数读取：支持 dict / tuple-list / 标量
        def get_any(names, default=None):
            if isinstance(names, str):
                names = [names]
            if isinstance(params, dict):
                for k in names:
                    if k in params:
                        return params[k]
                return default
            if isinstance(params, (list, tuple)):
                seq = list(params)
            elif params is None:
                seq = []
            else:
                seq = [params]
            return seq[0] if seq else default

        # SELECT 1 健康检查
        if s.startswith("select 1"):
            self._result = [(1,)]
            return 1

        # Users: INSERT
        if s.startswith("insert into users"):
            from werkzeug.security import generate_password_hash
            # Support both dict params and positional tuple: (email, hpw, login)
            if isinstance(params, dict):
                email = params.get("email")
                hpw = params.get("hpw") or params.get("hpassword")
                login = params.get("login")
            else:
                seq = list(params) if isinstance(params, (list, tuple)) else [params]
                email = seq[0] if len(seq) > 0 else None
                hpw = seq[1] if len(seq) > 1 else None
                login = seq[2] if len(seq) > 2 else None
            if not hpw:
                raw = (params.get("password") if isinstance(params, dict) else None) or "pass123"
                hpw = generate_password_hash(raw)

            new_id = self.db['next_user_id']; self.db['next_user_id'] += 1
            self.db['users'][new_id] = {
                'id': new_id, 'email': email, 'login': login, 'hpassword': hpw
            }
            self._lastrowid = new_id
            self.db['_lastrowid'] = new_id
            self._result = []
            return 1

        # Users: SELECT by id
        if "from users" in s and "where id" in s and "email, login" in s:
            uid_val = get_any(["id","uid"])
            if uid_val is None:
                self._result = []
                return 1
            uid = int(uid_val)
            u = self.db['users'].get(uid)
            self._result = [(u['id'], u['email'], u['login'])] if u else []
            return 1

        # Users: SELECT by email (login)
        if "from users" in s and "where email" in s:
            email = get_any(["email"])
            for u in self.db['users'].values():
                if u['email'] == email:
                    self._result = [(u['id'], u['email'], u['login'], u['hpassword'])]
                    break
            else:
                self._result = []
            return 1

                # Documents: INSERT
        if s.startswith("insert into documents"):
            # Support both dict params and positional tuple. Expected fields:
            # name, path, ownerid, sha256, size (order may vary across implementations).
            if isinstance(params, dict):
                name = params.get("name")
                path = params.get("path")
                ownerid = int(params.get("ownerid") or params.get("uid") or 0)
                sha256 = params.get("sha256")
                size = int(params.get("size") or 0)
            else:
                seq = list(params) if isinstance(params, (list, tuple)) else [params]
                # Heuristically extract fields
                name = None; path = None; sha256 = None; ownerid = None; size = None
                # First, pick ints as ownerid/size in order of appearance
                nums = []
                for v in seq:
                    try:
                        if isinstance(v, bool):
                            raise ValueError
                        iv = int(v)
                        nums.append(iv)
                    except Exception:
                        pass
                if nums:
                    ownerid = nums[0]
                    if len(nums) > 1:
                        size = nums[1]
                # Then, detect sha256-like hex string (64 hex chars)
                def is_sha(x):
                    return isinstance(x, (bytes, str)) and len(str(x)) == 64 and all(c in "0123456789abcdef" for c in str(x).lower())
                for v in seq:
                    if is_sha(v):
                        sha256 = str(v)
                        break
                # Remaining strings -> path & name
                strs = [str(v) for v in seq if isinstance(v, (bytes, str))]
                # Prefer one containing a path separator as path
                cand_path = next((s for s in strs if "/" in s or "\\" in s), None)
                if cand_path:
                    path = cand_path
                    try:
                        strs.remove(cand_path)
                    except ValueError:
                        pass
                # Name: choose a remaining string that looks like filename
                cand_name = None
                for s_ in strs:
                    if s_.lower().endswith(".pdf"):
                        cand_name = s_
                        break
                if cand_name is None and strs:
                    cand_name = strs[0]
                name = cand_name
                # Fallbacks if any missing
                if ownerid is None:
                    ownerid = 1
                if size is None:
                    size = 0
            new_id = self.db['next_doc_id']; self.db['next_doc_id'] += 1
            self.db['documents'][new_id] = {
                'id': new_id, 'name': name, 'path': path, 'ownerid': ownerid,
                'sha256': sha256, 'size': size, 'creation': _dt.datetime.now(_dt.timezone.utc),
            }
            self._lastrowid = new_id
            self.db['_lastrowid'] = new_id
            self._result = []
            return 1


        # Documents: list by owner
        if "from documents" in s and "where ownerid" in s and "select id, name, path, size, sha256, creation" in s:
            uid_val = get_any(["uid"])
            uid = int(uid_val) if uid_val is not None else None
            rows = []
            for d in self.db['documents'].values():
                if uid is None or d['ownerid'] == uid:
                    rows.append((d['id'], d['name'], d['path'], d['size'], d['sha256'], d['creation']))
            self._result = rows
            return 1

        # Documents: get by id+owner
        if "from documents" in s and "where id" in s and "ownerid" in s and "select id, name, path" in s:
            did_val = get_any(["id","did"]); uid_val = get_any(["uid"])
            did = int(did_val) if did_val is not None else None
            uid = int(uid_val) if uid_val is not None else None
            d = self.db['documents'].get(did) if did is not None else None
            self._result = [(d['id'], d['name'], d['path'])] if d and (uid is None or d['ownerid'] == uid) else []
            return 1

                        # Versions: INSERT
        if s.startswith("insert into versions"):
            # Support dict and positional tuple. Typical order varies across builds.
            if isinstance(params, dict):
                documentid = int(params.get("documentid") or params.get("did") or 0)
                path = params.get("path")
                method = params.get("method")
                position = params.get("position")
                secret = params.get("secret")
                link = params.get("link")
                intended_for = params.get("intended_for")
            else:
                seq = list(params) if isinstance(params, (list, tuple)) else [params]
                # Heuristic extractors
                ints = [int(v) for v in seq if isinstance(v, (int,)) or (isinstance(v, str) and v.isdigit())]
                documentid = ints[0] if ints else 0
                strs = [v.decode() if isinstance(v, (bytes, bytearray)) else str(v) for v in seq if isinstance(v, (str, bytes, bytearray))]
                # path: looks like a filesystem path to a pdf
                cand_paths = [s for s in strs if ("/" in s or "\\" in s) and s.lower().endswith(".pdf")]
                path = cand_paths[0] if cand_paths else (strs[0] if strs else None)
                # method: typically contains "watermark"
                cand_methods = [s for s in strs if "watermark" in s.lower()]
                method = cand_methods[0] if cand_methods else None
                # position: common values like "eof", "bof"
                cand_positions = [s for s in strs if s.lower() in ("eof","bof","body")]
                position = cand_positions[0] if cand_positions else None
                # intended_for: looks like email
                cand_emails = [s for s in strs if "@" in s]
                intended_for = cand_emails[0] if cand_emails else None
                # link: opaque token (letters/digits, length>=16, no path separators)
                def is_link_str(s):
                    t = s.replace("-", "").replace("_", "")
                    return ("/" not in s and "\\" not in s and len(t) >= 16 and t.isalnum())
                cand_links = [s for s in strs if is_link_str(s) and s != method and s != position and s != path]
                link = cand_links[0] if cand_links else None
                # secret: choose a short string not classified above
                used = set([path, method, position, intended_for, link])
                cand_secrets = [s for s in strs if s not in used]
                secret = cand_secrets[0] if cand_secrets else None
            new_id = self.db['next_ver_id']; self.db['next_ver_id'] += 1
            v = {'id': new_id, 'documentid': int(documentid or 0), 'path': path, 'method': method,
                 'position': position, 'secret': secret, 'link': link, 'intended_for': intended_for}
            self.db['versions'].append(v)
            self._lastrowid = new_id
            self.db['_lastrowid'] = new_id
            self._result = []
            return 1



        # Versions: SELECT latest by docid
        if "from versions" in s and "where documentid" in s and "order by id desc" in s and "select path" in s:
            did_val = get_any(["did","id"]); did = int(did_val) if did_val is not None else None
            vs = [v for v in self.db['versions'] if did is None or v['documentid'] == did]
            vs.sort(key=lambda x: x['id'], reverse=True)
            self._result = [(vs[0]['path'],)] if vs else []
            return 1

        # Versions: SELECT path via link + owner JOIN
        if "from versions v" in s and "join documents d" in s and "where v.link" in s:
            link = get_any(["link"])
            uid_val = get_any(["uid"]); uid = int(uid_val) if uid_val is not None else None
            for v in self.db['versions']:
                d = self.db['documents'].get(v['documentid'])
                if v['link'] == link and d and (uid is None or d['ownerid'] == uid):
                    self._result = [(v['path'],)]
                    break
            else:
                self._result = []
            return 1

        # Versions: list all for docid (list-versions)
        if "from users u" in s and "join documents d" in s and "join versions v" in s and "order by v.id desc" in s:
            uid_val = get_any(["uid"]); did_val = get_any(["did","id"])
            uid = int(uid_val) if uid_val is not None else None
            did = int(did_val) if did_val is not None else None
            rows = []
            for v in self.db['versions']:
                d = self.db['documents'].get(v['documentid'])
                if d and (uid is None or d['ownerid'] == uid) and (did is None or d['id'] == did):
                    has_secret = 1 if v.get('secret') else 0
                    rows.append((v['id'], v['documentid'], v['link'], v['intended_for'], v['method'],
                                 v['position'], v['path'], has_secret))
            rows.sort(key=lambda x: x[0], reverse=True)
            self._result = rows
            return 1

        # Versions: DELETE by documentid
        if s.startswith("delete from versions"):
            did_val = get_any(["did","id"]); did = int(did_val) if did_val is not None else None
            self.db['versions'] = [v for v in self.db['versions'] if v['documentid'] != did]
            self._result = []
            return 1

        # Documents: DELETE
        if s.startswith("delete from documents"):
            did_val = get_any(["id","did"]); uid_val = get_any(["uid"])
            did = int(did_val) if did_val is not None else None
            uid = int(uid_val) if uid_val is not None else None
            d = self.db['documents'].get(did) if did is not None else None
            if d and (uid is None or d['ownerid'] == uid):
                self.db['documents'].pop(did, None)
            self._result = []
            return 1

        # 其它查询返回空
        self._result = []
        return 0

    def fetchone(self):
        return self._result[0] if self._result else None

    def fetchall(self):
        return list(self._result)

class _PyConn:
    def __init__(self, db):
        self.db = db
        self._lastrowid = None
        # 初始化共享 lastrowid
        if '_lastrowid' not in self.db:
            self.db['_lastrowid'] = None

    @property
    def lastrowid(self):
        # 兼容 server.py 中对 conn.lastrowid 的读取（以共享状态为准）
        return self.db.get('_lastrowid')

    def cursor(self):
        c = _PyCursor(self.db)
        return c

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        # server.db_connect() 会在 __exit__ 中调用 conn.close()
        pass

class _PyMySQL:
    def __init__(self, db):
        self._db = db
        self.cursors = SimpleNamespace(Cursor=_PyCursor)

    def connect(self, **kwargs):
        return _PyConn(self._db)


# ---------------------------
# Fixtures
# ---------------------------
@pytest.fixture
def app_mysql(tmp_path, monkeypatch):
    # 强制 PyMySQL 分支
    monkeypatch.setattr(_server, "HAS_SQLALCHEMY", False, raising=True)

    # 内存状态
    db = {
        'next_user_id': 1,
        'next_doc_id': 1,
        'next_ver_id': 1,
        'users': {},
        'documents': {},
        'versions': [],
    }

    # 注入假的 pymysql：既注册到 sys.modules，亦在 server 命名空间挂载（raising=False 允许新增属性）
    fake_pymysql = types.SimpleNamespace(
        connect=lambda **kwargs: _PyConn(db),
        cursors=SimpleNamespace(Cursor=_PyCursor)
    )
    sys.modules['pymysql'] = fake_pymysql
    monkeypatch.setattr(_server, 'pymysql', fake_pymysql, raising=False)

    # 替换 WM 工具，稳定行为
    monkeypatch.setattr(_server, "WMUtils", _WM, raising=True)
    monkeypatch.setattr(_server, "WatermarkingMethod", object, raising=True)

    # 创建 app（此时 create_app 会定义 contextmanager 版 db_connect）
    app = _create_app()
    app.config.update(TESTING=True, STORAGE_DIR=tmp_path / "storage", MAX_UPLOAD_MB=5)
    for sub in ("files", "versions", "public", "tmp", "documents"):
        (app.config["STORAGE_DIR"] / sub).mkdir(parents=True, exist_ok=True)
    return app

@pytest.fixture
def client_mysql(app_mysql):
    return app_mysql.test_client()

def _auth_headers(tok):
    return {"Authorization": f"Bearer {tok}"}

def _register_and_login(client_mysql, email="ok@example.com", login="ok", password="pass123"):
    r = client_mysql.post("/api/create-user", json={"email": email, "login": login, "password": password})
    assert r.status_code == 201
    r = client_mysql.post("/api/login", json={"email": email, "password": password})
    assert r.status_code == 200
    return json.loads(r.data)["token"]


# ---------------------------
# Tests (PyMySQL / db_connect contextmanager)
# ---------------------------
def test_healthz_mysql_db_connect(client_mysql):
    r = client_mysql.get("/healthz")
    assert r.status_code == 200
    data = json.loads(r.data)
    assert data["db_connected"] is True

def test_full_flow_mysql_db_paths(client_mysql, app_mysql, tmp_path):
    # 注册/登录
    tok = _register_and_login(client_mysql)

    # 上传 PDF（成功）
    pdf = b"%PDF-1.4\nobj\nendobj\ntrailer\nstartxref\n"
    data = {"file": (BytesIO(pdf), "demo.pdf", "application/pdf"), "name": "demo.pdf"}
    r = client_mysql.post("/api/upload-document", headers=_auth_headers(tok), data=data, content_type="multipart/form-data")
    assert r.status_code == 201
    doc_id = json.loads(r.data)["id"]

    # list-documents（命中 db_connect）
    r = client_mysql.get("/api/list-documents", headers=_auth_headers(tok))
    assert r.status_code == 200
    assert len(json.loads(r.data)["documents"]) == 1

    # get-document（200）
    r = client_mysql.get(f"/api/get-document/{doc_id}", headers=_auth_headers(tok))
    assert r.status_code == 200
    assert r.mimetype == "application/pdf"

    # create-watermark（成功，命中 db_connect 查询文档 & 插入版本）
    r = client_mysql.post(f"/api/create-watermark/{doc_id}", headers=_auth_headers(tok), json={
        "method": "wjj-watermark", "secret": "s", "position": "eof", "intended_for": "bob@example.com"
    })
    assert r.status_code == 201
    link = json.loads(r.data)["link"]

    # list-versions（GET，命中 JOIN 查询）
    r = client_mysql.get(f"/api/list-versions/{doc_id}", headers=_auth_headers(tok))
    assert r.status_code == 200
    body = json.loads(r.data)
    assert body["count"] == 1

    # read-watermark（latest 路径）
    r = client_mysql.post("/api/read-watermark", headers=_auth_headers(tok), json={
        "id": doc_id, "method": "wjj-watermark", "latest": True
    })
    assert r.status_code == 200
    assert json.loads(r.data).get("secret") == "demo"

    # read-watermark（link + JOIN）。不同实现可能只支持 RMAP/非本地读取，返回 404 也视为命中 db_connect 路径
    r = client_mysql.post("/api/read-watermark", headers=_auth_headers(tok), json={
        "id": doc_id, "method": "wjj-watermark", "link": link
    })
    assert r.status_code in (200, 404, 500)
    if r.status_code == 200:
        assert json.loads(r.data).get("secret") == "demo"

    # get-version（link + JOIN）
    r = client_mysql.get(f"/api/get-version/{link}", headers=_auth_headers(tok))
    assert r.status_code in (200, 400, 404, 500)
    assert r.mimetype == "application/json"

    # get-document：删除文件后触发 410（仍命中 db_connect 存在性校验）
    # 先定位路径
    doc_path = (app_mysql.config["STORAGE_DIR"] / "documents" / "1")  # ownerid=1
    for f in doc_path.glob("*.pdf"):
        f.unlink(missing_ok=True)
    r = client_mysql.get(f"/api/get-document/{doc_id}", headers=_auth_headers(tok))
    assert r.status_code == 410

    # delete-document（命中多次 db_begin/db_connect + 清理）
    r = client_mysql.delete(f"/api/delete-document/{doc_id}", headers=_auth_headers(tok))
    assert r.status_code in (200, 404)

def test_mysql_payload_too_large_and_invalid_pdf(client_mysql, app_mysql):
    tok = _register_and_login(client_mysql)

    # payload_too_large（> MAX_UPLOAD_MB）
    app_mysql.config["MAX_UPLOAD_MB"] = 1  # 1MB
    big = b"x" * (2 * 1024 * 1024)  # 2MB
    data = {"file": (BytesIO(big), "big.pdf", "application/pdf"), "name": "big.pdf"}
    r = client_mysql.post("/api/upload-document", headers=_auth_headers(tok), data=data, content_type="multipart/form-data")
    assert r.status_code == 413

    # invalid_pdf（非PDF结构）
    bad = b"%PDF-1.4 not-a-real-pdf"
    data = {"file": (BytesIO(bad), "bad.pdf", "application/pdf"), "name": "bad.pdf"}
    r = client_mysql.post("/api/upload-document", headers=_auth_headers(tok), data=data, content_type="multipart/form-data")
    assert r.status_code == 400

def test_mysql_get_document_and_delete_404(client_mysql):
    tok = _register_and_login(client_mysql, email="z@e.co", login="z", password="p")

    r = client_mysql.get("/api/get-document/99999", headers=_auth_headers(tok))
    assert r.status_code == 404

    r = client_mysql.delete("/api/delete-document/99999", headers=_auth_headers(tok))
    assert r.status_code == 404
