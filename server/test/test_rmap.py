import base64
import pytest
from src.rmap import rmap


# ---------- Fixture: 模拟 IdentityManager ----------
class DummyIM:
    def __init__(self):
        self.called = []

    def decrypt_for_server(self, payload):
        self.called.append(("decrypt", payload))
        if payload == "fail":
            raise ValueError("decrypt error")
        # 返回伪明文
        if isinstance(payload, dict) and "nonceServer" in payload:
            return {"nonceServer": 999}
        if payload == "msg2":
            return {"nonceServer": 123456}
        # message1
        return {"nonceClient": 42, "identity": "clientA"}

    def encrypt_for_client(self, identity, payload):
        self.called.append(("encrypt", identity, payload))
        return base64.b64encode(f"{identity}:{payload}".encode()).decode()


# ---------- Tests ----------

def test_handle_message1_normal(monkeypatch):
    im = DummyIM()
    r = rmap.RMAP(im)

    msg1 = {"payload": "abc"}  # 模拟 base64
    result = r.handle_message1(msg1)

    # 应包含这四个关键字段
    assert set(result.keys()) == {"payload", "identity", "nonceClient", "nonceServer"}
    assert result["identity"] == "clientA"
    assert result["nonceClient"] == 42
    # payload 为 base64
    decoded = base64.b64decode(result["payload"]).decode()
    assert "clientA" in decoded
    assert "nonceServer" in str(result["nonceServer"])


def test_handle_message1_exception():
    im = DummyIM()
    r = rmap.RMAP(im)
    # decrypt_for_server 抛错
    with pytest.raises(RuntimeError) as e:
        r.handle_message1({"payload": "fail"})
    assert "handle_message1 failed" in str(e.value)


def test_handle_message2_normal():
    im = DummyIM()
    r = rmap.RMAP(im)
    msg2 = {"payload": "msg2"}
    result = r.handle_message2(msg2)
    assert result == {"nonceServer": 123456}


def test_handle_message2_exception():
    im = DummyIM()
    r = rmap.RMAP(im)
    with pytest.raises(RuntimeError) as e:
        r.handle_message2({"payload": "fail"})
    assert "handle_message2 failed" in str(e.value)
