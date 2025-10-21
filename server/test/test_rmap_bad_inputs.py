import json, base64

def _pack(obj: dict) -> str:
    return "enc:" + base64.b64encode(json.dumps(obj, sort_keys=True).encode()).decode()

def _unpack(enc: str) -> dict:
    return json.loads(base64.b64decode(enc[4:].encode()).decode())

def test_initiate_missing_identity(client):
    # 缺 identity（或为空）应返回 400/422
    msg1 = _pack({"nonceClient": "1" * 32})
    r = client.post("/api/rmap-initiate", json={"payload": msg1})
    assert r.status_code in (400, 422)

def test_respond_missing_payload(client):
    r = client.post("/api/rmap-get-link", json={})
    assert r.status_code in (400, 422)

def test_respond_wrong_server_nonce(client):
    # 正确的 Step 1，拿到合法的 server_nonce（以及服务端回显的 client_nonce）
    msg1 = _pack({"identity": "Grp_08", "nonceClient": "1" * 20})
    r1 = client.post("/api/rmap-initiate", json={"payload": msg1})
    assert r1.status_code == 200, r1.data
    s1 = _unpack(r1.get_json()["payload"])
    assert "nonceServer" in s1

    # Step 2 伪造错误 server_nonce
    bad_nonce_server = "110" + "5" * 29
    bad_msg2 = _pack({"nonceServer": bad_nonce_server})
    r2 = client.post("/api/rmap-get-link", json={"payload": bad_msg2})
    assert r2.status_code in (400, 401, 403)
