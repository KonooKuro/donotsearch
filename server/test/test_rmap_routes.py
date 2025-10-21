import io
import json
import os
from pathlib import Path
import pytest
from flask import Flask
import types

import src.rmap_routes as rr


@pytest.fixture
def app(monkeypatch, tmp_path):
    # 临时存储目录替换 PDF_OUT_DIR
    monkeypatch.setattr(rr, "PDF_OUT_DIR", tmp_path)
    rr.PDF_OUT_DIR.mkdir(exist_ok=True)
    rr._SESS.clear()

    app = Flask(__name__)
    app.register_blueprint(rr.rmap_bp)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# ---------------- index ----------------

def test_index_ok(client):
    resp = client.get("/rmap")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "RMAP server running" in data["status"]
    assert "/rmap-initiate" in data["endpoints"]


# ---------------- rmap_initiate ----------------

def test_rmap_initiate_normal(monkeypatch, client):
    called = {}
    def fake_handle_message1(msg):
        called["ok"] = True
        return {"identity": "cli", "nonceClient": 1, "nonceServer": 2, "payload": "xyz"}
    monkeypatch.setattr(rr.rmap, "handle_message1", fake_handle_message1)
    resp = client.post("/rmap-initiate", json={"payload": "xxx"})
    assert resp.status_code == 200
    j = resp.get_json()
    assert j["payload"] == "xyz"
    assert (2 in rr._SESS)  # 已保存 session


def test_rmap_initiate_exception(monkeypatch, client):
    def bad_handle(_): raise RuntimeError("boom")
    monkeypatch.setattr(rr.rmap, "handle_message1", bad_handle)
    resp = client.post("/rmap-initiate", json={"payload": "xxx"})
    assert resp.status_code == 400
    assert "boom" in resp.get_data(as_text=True)


# ---------------- rmap_get_link ----------------

def test_rmap_get_link_normal(monkeypatch, tmp_path, client):
    rr._SESS.clear()
    rr._save_session("cli", 11, 22)
    # 伪造 handle_message2 正常返回
    def fake_hm2(msg): return {"nonceServer": 22}
    monkeypatch.setattr(rr.rmap, "handle_message2", fake_hm2)
    # 替换 HiddenObjectB64Method
    class DummyHidden:
        def add_watermark(self, pdf_path, secret):
            return b"%PDF-1.4 test"
    monkeypatch.setattr(rr, "HiddenObjectB64Method", lambda : DummyHidden())
    # 替换 PDF_BASE 避免文件不存在
    monkeypatch.setattr(rr, "PDF_BASE", tmp_path / "base.pdf")
    rr.PDF_BASE.write_bytes(b"%PDF-1.4")

    resp = client.post("/rmap-get-link", json={"payload": "p"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "result" in data
    sid = data["result"]
    # 应该已生成对应 pdf 文件
    f = tmp_path / f"{sid}.pdf"
    assert f.exists() and f.read_bytes().startswith(b"%PDF")


def test_rmap_get_link_no_session(monkeypatch, client):
    rr._SESS.clear()
    monkeypatch.setattr(rr.rmap, "handle_message2", lambda _: {"nonceServer": 999})
    resp = client.post("/rmap-get-link", json={"payload": "x"})
    assert resp.status_code == 400
    assert "session not found" in resp.get_data(as_text=True)


def test_rmap_get_link_exception(monkeypatch, client):
    def bad(_): raise RuntimeError("fail")
    monkeypatch.setattr(rr.rmap, "handle_message2", bad)
    resp = client.post("/rmap-get-link", json={"payload": "x"})
    assert resp.status_code == 400
    assert "fail" in resp.get_data(as_text=True)


# ---------------- api_get_version ----------------

def test_get_version_invalid_sid(client):
    resp = client.get("/get-version/zzz")
    assert resp.status_code == 400
    assert "invalid" in resp.get_data(as_text=True)


def test_get_version_file_not_found(client):
    sid = "a" * 32
    resp = client.get(f"/get-version/{sid}")
    assert resp.status_code == 404


def test_get_version_empty_file(monkeypatch, tmp_path, client):
    sid = "b" * 32
    f = tmp_path / f"{sid}.pdf"
    f.write_bytes(b"")
    monkeypatch.setattr(rr, "PDF_OUT_DIR", tmp_path)
    resp = client.get(f"/get-version/{sid}")
    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"


def test_get_version_stat_error(monkeypatch, tmp_path, client):
    sid = "c" * 32
    f = tmp_path / f"{sid}.pdf"
    f.write_bytes(b"abc")
    # 指向临时输出目录
    monkeypatch.setattr(rr, "PDF_OUT_DIR", tmp_path)

    # 仅在 rr 模块内拦截 os.stat，且兼容 follow_symlinks 等可选参数
    orig_stat = rr.os.stat

    def fake_stat(path, *args, **kwargs):
        # 只对这个目标文件制造 OSError，其它路径走原始 stat
        if Path(path) == f:
            raise OSError("nope")
        return orig_stat(path, *args, **kwargs)

    monkeypatch.setattr(rr.os, "stat", fake_stat)

    resp = client.get(f"/get-version/{sid}")
    assert resp.status_code == 200  # 路由里对 stat 失败做了降级处理



def test_get_version_unexpected_exception(monkeypatch, client):
    def bad_send(*a, **kw): raise RuntimeError("sendfail")
    monkeypatch.setattr(rr, "send_file", bad_send)
    sid = "d" * 32
    # 创建伪 PDF
    p = rr.PDF_OUT_DIR / f"{sid}.pdf"
    p.write_bytes(b"pdfdata")
    resp = client.get(f"/get-version/{sid}")
    assert resp.status_code == 500
    assert "server error" in resp.get_data(as_text=True)
