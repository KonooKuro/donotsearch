import base64
import json
import io
import types
import pytest
from pathlib import Path
from src.rmap import identity_manager as im


# ---------- Fixture 模拟 key 对象 ----------
class DummyPGPKey:
    def __init__(self, name="pub"):
        self.name = name
        self._unlocked = False
        self.decrypted = None

    @staticmethod
    def from_file(path):
        # 模拟返回 (key, extra)
        return (DummyPGPKey(path), None)

    def encrypt(self, msg):
        return f"[ENCRYPTED-{self.name}]{msg.message}"

    def decrypt(self, pgp_msg):
        # 模拟解密内容
        class DummyMsg:
            def __init__(self, message):
                self.message = message
        return DummyMsg(json.dumps({"ok": True, "msg": "decrypted"}))

    def unlock(self, passphrase):
        # 模拟上下文管理器
        self._unlocked = True
        class DummyCtx:
            def __enter__(self2): return self
            def __exit__(self2, *a): self._unlocked = False
        return DummyCtx()


class DummyPGPMessage:
    @staticmethod
    def new(txt):
        return types.SimpleNamespace(message=txt)
    @staticmethod
    def from_blob(blob):
        return types.SimpleNamespace(blob=blob, message="decoded")


@pytest.fixture(autouse=True)
def patch_pgpy(monkeypatch):
    monkeypatch.setattr(im, "PGPKey", DummyPGPKey)
    monkeypatch.setattr(im, "PGPMessage", DummyPGPMessage)
    yield


# ---------- __init__ 覆盖 ----------

def test_init_with_public_only(tmp_path):
    pub = tmp_path / "server_pub.asc"
    pub.write_text("pubkey")
    obj = im.IdentityManager(tmp_path, pub)
    assert obj.server_priv is None
    assert obj.server_pub.name.endswith("server_pub.asc")


def test_init_with_public_and_private(tmp_path):
    pub = tmp_path / "server_pub.asc"
    priv = tmp_path / "server_priv.asc"
    pub.write_text("pubkey")
    priv.write_text("privkey")
    obj = im.IdentityManager(tmp_path, pub, priv)
    assert obj.server_priv.name.endswith("server_priv.asc")


# ---------- encrypt_for_server ----------

def test_encrypt_for_server(monkeypatch, tmp_path):
    pub = tmp_path / "server_pub.asc"
    pub.write_text("pubkey")
    obj = im.IdentityManager(tmp_path, pub)
    result = obj.encrypt_for_server({"a": 1})
    # base64 decode should start with "[ENCRYPTED"
    decoded = base64.b64decode(result).decode()
    assert "[ENCRYPTED" in decoded


# ---------- decrypt_for_server ----------

def test_decrypt_for_server_no_private(tmp_path):
    pub = tmp_path / "pub.asc"
    pub.write_text("pub")
    obj = im.IdentityManager(tmp_path, pub)
    with pytest.raises(ValueError):
        obj.decrypt_for_server("xxx")


def test_decrypt_for_server_normal(monkeypatch, tmp_path):
    pub = tmp_path / "pub.asc"
    priv = tmp_path / "priv.asc"
    pub.write_text("pub")
    priv.write_text("priv")

    obj = im.IdentityManager(tmp_path, pub, priv)
    obj.server_passphrase = None  # 不走 unlock 分支
    payload = base64.b64encode(b"some-pgp").decode()
    result = obj.decrypt_for_server(payload)
    assert result["ok"] is True

def test_decrypt_for_server_with_passphrase(monkeypatch, tmp_path):
    pub = tmp_path / "pub.asc"
    priv = tmp_path / "priv.asc"
    pub.write_text("pub")
    priv.write_text("priv")

    obj = im.IdentityManager(tmp_path, pub, priv)
    obj.server_passphrase = "1234"
    payload = base64.b64encode(b"pgp-data").decode()
    result = obj.decrypt_for_server(payload)
    assert "msg" in result and obj.server_priv._unlocked is False


# ---------- encrypt_for_client ----------

def test_encrypt_for_client_missing_key(tmp_path):
    pub = tmp_path / "pub.asc"
    pub.write_text("pub")
    obj = im.IdentityManager(tmp_path, pub)
    with pytest.raises(FileNotFoundError):
        obj.encrypt_for_client("nonexist", {"data": 1})


def test_encrypt_for_client_success(tmp_path):
    pub = tmp_path / "pub.asc"
    cli = tmp_path / "client1.asc"
    cli.write_text("clientkey")
    obj = im.IdentityManager(tmp_path, pub)
    result = obj.encrypt_for_client("client1", {"x": 2})
    decoded = base64.b64decode(result).decode()
    assert "[ENCRYPTED" in decoded
