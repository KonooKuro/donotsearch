# test/test_rmap_happy_path.py
import json, base64

def _pack(obj: dict) -> str:
    return "enc:" + base64.b64encode(json.dumps(obj, sort_keys=True).encode()).decode()

def _unpack(enc: str) -> dict:
    assert isinstance(enc, str) and enc.startswith("enc:")
    return json.loads(base64.b64decode(enc[4:].encode()).decode())

def test_full_handshake(client):

    nonce_c = "1" * 20
    msg1 = _pack({"identity": "Grp_08", "nonceClient": nonce_c})
    r1 = client.post("/api/rmap-initiate", json={"payload": msg1})
    assert r1.status_code == 200, r1.data
    j1 = r1.get_json()
    assert "payload" in j1

    s1 = _unpack(j1["payload"])
    assert "nonceClient" in s1 and "nonceServer" in s1
    assert s1["nonceClient"] == 11111111111111111111
    nonce_s = s1["nonceServer"]

    msg2 = _pack({"nonceServer": nonce_s})
    r2 = client.post("/api/rmap-get-link", json={"payload": msg2})
    assert r2.status_code == 200, r2.data
    token = r2.get_json()["result"]
    assert isinstance(token, str) and token

    r3 = client.get(f"/api/rmap-download?token={token}")
    if r3.status_code == 200 and not r3.is_json:
        assert r3.data.startswith(b"%PDF")
