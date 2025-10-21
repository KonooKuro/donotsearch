import os
import sys
import json
import base64
import importlib
import types
import pytest
from unittest.mock import MagicMock

# --- 让 Python 能 import 到 src/ 包 ---
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../server
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# --- stub pikepdf，避免导入时崩掉，并提供 open() ---
if "pikepdf" not in sys.modules:
    import types as _types

    class _DummyPdf:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def save(self, *args, **kwargs):
            return None

        def close(self):
            return None

    pike_stub = _types.SimpleNamespace()
    pike_stub.open = staticmethod(lambda *a, **k: _DummyPdf())
    Pdf = _types.SimpleNamespace()
    Pdf.open = staticmethod(lambda *a, **k: _DummyPdf())
    pike_stub.Pdf = Pdf
    pike_stub.Name = staticmethod(lambda s: s)
    pike_stub.Object = object
    pike_stub.Array = list
    pike_stub.Dictionary = dict

    sys.modules["pikepdf"] = pike_stub
# --- end stub ---

def _apply_identity_manager_mocks():
    """在导入 server 之前，对 IdentityManager 做 enc:base64(json) 打桩。"""
    def _pack(obj: dict) -> str:
        return "enc:" + base64.b64encode(json.dumps(obj, sort_keys=True).encode()).decode()

    def _unpack(payload: str) -> dict:
        if isinstance(payload, bytes):
            payload = payload.decode()
        assert isinstance(payload, str) and payload.startswith("enc:")
        return json.loads(base64.b64decode(payload[4:].encode()).decode())

    def _patch(mod):
        if not hasattr(mod, "IdentityManager"):
            return False
        IM = mod.IdentityManager

        def fake_encrypt_for_server(self, plaintext: dict) -> str:
            return _pack(plaintext)

        def fake_decrypt_for_server(self, payload: str) -> dict:
            return _unpack(payload)

        def fake_encrypt_for_client(self, identity: str, plaintext: dict) -> str:
            return _pack(plaintext)

        def fake_generate_nonce(length: int = 32) -> str:
            return "N" * length

        IM.encrypt_for_server = fake_encrypt_for_server
        IM.decrypt_for_server = fake_decrypt_for_server
        IM.encrypt_for_client = fake_encrypt_for_client
        setattr(IM, "generate_nonce", fake_generate_nonce)
        return True

    patched = False
    for modname in ("src.rmap.identity_manager", "rmap.identity_manager"):
        try:
            mod = importlib.import_module(modname)
            patched = _patch(mod) or patched
        except Exception:
            pass
    return patched

def _patch_pdf_builder():
    """mock PDF 生成，避免真实算法/系统依赖。"""
    for modname in ("src.rmap.watermark", "rmap.watermark"):
        try:
            wm = importlib.import_module(modname)

            def fake_build_pdf(session_token: str) -> bytes:
                return b"%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\n%%EOF"

            for fname in ("build_watermarked_pdf", "generate_watermarked_pdf", "create_pdf"):
                if hasattr(wm, fname):
                    setattr(wm, fname, fake_build_pdf)
                    break
        except Exception:
            pass

@pytest.fixture(scope="session")
def app():
    """先打桩 IdentityManager，再导入 server.create_app。"""
    os.environ["PYTEST_CURRENT_TEST"] = "1"
    _apply_identity_manager_mocks()
    _patch_pdf_builder()

    server = importlib.import_module("src.server")
    create_app = getattr(server, "create_app")

    try:
        flask_app = create_app("testing")
    except TypeError:
        flask_app = create_app()
    flask_app.config.update(TESTING=True)
    return flask_app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def mocker(monkeypatch):
    """简易 mocker 垫片"""
    class _SimpleMocker:
        def patch(self, target, new=MagicMock(), **kwargs):
            mod_name, attr = target.rsplit('.', 1)
            mod = importlib.import_module(mod_name)
            monkeypatch.setattr(mod, attr, new)
            return new
    return _SimpleMocker()
