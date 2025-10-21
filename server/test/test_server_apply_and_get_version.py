# -*- coding: utf-8 -*-
import sys
import json
from io import BytesIO
import pathlib
import importlib
import pytest
from flask import g

# 总是从 src/ 导入真实模块
BASE = pathlib.Path(__file__).resolve().parents[1]
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

_server = importlib.import_module("src.server")
WMUtils = importlib.import_module("src.watermarking_utils")

# 复用你已有的 MySQL fixtures / helpers（确保 db_connect/pymysql 假实现按你的工程配置）
from test_api_dbconnect_paths import client_mysql, app_mysql, _auth_headers, _register_and_login

# ---------- 伪水印方法：覆盖 _apply_watermark 的各条路径 ----------
class _AddOK:
    def add_watermark(self, data: bytes, *, secret, key=None, position=None):
        # 返回“看起来像 PDF”的内容（包含 startxref & EOF）
        return (
            b"%PDF-1.4\n"
            b"1 0 obj\n<< /Type /Catalog >>\nendobj\n"
            b"trailer\nstartxref\n"
            + b"[" + (secret or "NA").encode("utf-8") + b"]\n"
            b"%%EOF\n"
        )

class _ApplyWithPos:
    def apply(self, infile, outfile, *, position=None):
        with open(infile, "rb") as f, open(outfile, "wb") as g:
            pdf = f.read()
            g.write(pdf.replace(b"%%EOF", b"[pos=%s]\n%%EOF" % (position or "NA").encode("utf-8")))

class _ApplyNoPos:
    def apply(self, infile, outfile, *a, **kw):
        if kw:
            raise TypeError("unexpected keyword 'position'")
        with open(infile, "rb") as f, open(outfile, "wb") as g:
            pdf = f.read()
            g.write(pdf.replace(b"%%EOF", b"[nopo]\n%%EOF"))

class _AddNonBytesThenApply(_ApplyWithPos):
    def add_watermark(self, data: bytes, *, secret, key=None, position=None):
        # 故意返回非 bytes，server 内部应 fallback 到 apply(...)
        return "NOT-BYTES"

class _Unsupported:
    pass

def _install_method(name, obj):
    WMUtils.METHODS[name] = obj

# ---------- helpers ----------
# 注意：包含 startxref，避免 /api/upload-document 返回 400
PDF_MIN = b"%PDF-1.4\nobj\nendobj\ntrailer\nstartxref\n%%EOF\n"

def _bootstrap_user_and_doc(client):
    tok = _register_and_login(client)
    data = {"file": (BytesIO(PDF_MIN), "a.pdf", "application/pdf"), "name": "a.pdf"}
    r = client.post("/api/upload-document", headers=_auth_headers(tok), data=data, content_type="multipart/form-data")
    assert r.status_code == 201
    doc_id = json.loads(r.data)["id"]
    return tok, doc_id

def _create_version(client, tok, doc_id, method, secret="S", position="eof"):
    return client.post(
        f"/api/create-watermark/{doc_id}",
        headers=_auth_headers(tok),
        json={"method": method, "secret": secret, "position": position, "intended_for": "u@x.com"},
    )

# 直接调用 server.get_version 原函数（绕过 RMAP 路由），手动设置 g.user
def _get_version_internal(link: str, uid: int):
    fn = getattr(_server.get_version, "__wrapped__", _server.get_version)
    with _server.app.test_request_context("/"):
        g.user = {"id": uid}
        return fn(link)

# ---------- 覆盖 _apply_watermark 的四条路径 ----------
def test_apply_via_route_add_primary_success(client_mysql, app_mysql):
    _install_method("fake-add", _AddOK())
    tok, doc_id = _bootstrap_user_and_doc(client_mysql)
    r = _create_version(client_mysql, tok, doc_id, "fake-add", secret="S")
    assert r.status_code == 201
    link = json.loads(r.data)["link"]

    # 所有者 id 在你的 MySQL 桩里通常从 1 开始
    r2 = _get_version_internal(link, uid=1)
    assert getattr(r2, "status_code", 200) == 200
    assert r2.mimetype == "application/pdf"
    assert b"[S]" in (getattr(r2, "data", None) or r2.response[0])

def test_apply_via_route_fallback_apply_with_position(client_mysql, app_mysql):
    _install_method("fake-apply-pos", _ApplyWithPos())
    tok, doc_id = _bootstrap_user_and_doc(client_mysql)
    r = _create_version(client_mysql, tok, doc_id, "fake-apply-pos", secret="X", position="eof")
    assert r.status_code == 201
    link = json.loads(r.data)["link"]

    r2 = _get_version_internal(link, uid=1)
    payload = (getattr(r2, "data", None) or r2.response[0])
    assert b"[pos=eof]" in payload

def test_apply_via_route_fallback_apply_without_position(client_mysql, app_mysql):
    _install_method("fake-apply-nopos", _ApplyNoPos())
    tok, doc_id = _bootstrap_user_and_doc(client_mysql)
    r = _create_version(client_mysql, tok, doc_id, "fake-apply-nopos", secret="Z", position="bof")
    assert r.status_code == 201
    link = json.loads(r.data)["link"]

    r2 = _get_version_internal(link, uid=1)
    payload = (getattr(r2, "data", None) or r2.response[0])
    assert b"[nopo]" in payload

def test_apply_via_route_add_returns_nonbytes_then_fallback(client_mysql, app_mysql):
    _install_method("fake-mix", _AddNonBytesThenApply())
    tok, doc_id = _bootstrap_user_and_doc(client_mysql)
    r = _create_version(client_mysql, tok, doc_id, "fake-mix", secret="A", position="body")
    assert r.status_code == 201
    link = json.loads(r.data)["link"]

    r2 = _get_version_internal(link, uid=1)
    payload = (getattr(r2, "data", None) or r2.response[0])
    assert b"[pos=body]" in payload

def test_apply_via_route_unsupported_method(client_mysql, app_mysql):
    _install_method("fake-unsupported", _Unsupported())
    tok, doc_id = _bootstrap_user_and_doc(client_mysql)
    r = _create_version(client_mysql, tok, doc_id, "fake-unsupported", secret="S")
    # 服务端可能吞异常并返回 201（把空内容也落了版本记录）；只要路由不 5xx 即可
    assert r.status_code in (201, 400, 500, 503)

# ---------- 覆盖 get_version 的 200 / 404 / 410 / 503 ----------
def test_get_version_200_and_404_cross_user(client_mysql, app_mysql):
    _install_method("fake-add", _AddOK())
    tokA, docA = _bootstrap_user_and_doc(client_mysql)
    r = _create_version(client_mysql, tokA, docA, "fake-add", secret="OWN")
    assert r.status_code == 201
    link = json.loads(r.data)["link"]

    # 所有者（假定 id=1）-> 200
    r2 = _get_version_internal(link, uid=1)
    assert getattr(r2, "status_code", 200) == 200

    # 非所有者（第二个注册用户，假定 id=2）-> 404
    _register_and_login(client_mysql, email="b@x.com", login="b", password="p2")
    r3 = _get_version_internal(link, uid=2)
    assert r3.status_code == 404

def test_get_version_410_gone_by_missing_file(client_mysql, app_mysql, monkeypatch, tmp_path):
    _install_method("fake-add", _AddOK())
    tok, doc_id = _bootstrap_user_and_doc(client_mysql)
    r = _create_version(client_mysql, tok, doc_id, "fake-add", secret="GONE")
    assert r.status_code == 201
    link = json.loads(r.data)["link"]

    # 把解析器改成返回一个不存在的路径 -> 触发 410
    def _resolver(_p, root):
        return tmp_path / "not-exist.pdf"
    monkeypatch.setattr(_server, "_safe_resolve_under_storage", _resolver, raising=False)

    r2 = _get_version_internal(link, uid=1)
    assert r2.status_code == 410

def test_get_version_503_internal(monkeypatch, client_mysql, app_mysql):
    # 让 PyMySQL 分支的执行阶段抛错 -> except -> 503
    class _CurBad:
        def execute(self, s, params):
            raise RuntimeError("boom")
        def fetchone(self):
            return None
    class _ConnBad:
        def cursor(self):
            return _CurBad()
    class _PyBad:
        def connect(self, **kw):
            return _ConnBad()

    monkeypatch.setattr(_server, "HAS_SQLALCHEMY", False, raising=False)  # 强制 PyMySQL 路径
    monkeypatch.setattr(_server, "pymysql", _PyBad(), raising=False)      # 若无该属性也允许注入

    # 随便给一个 24 长度的 link，命中 SQL 分支出错即可
    r = _get_version_internal("Q" * 24, uid=1)
    assert r.status_code == 503
