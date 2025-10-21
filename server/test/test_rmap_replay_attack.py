import json, base64

def _handshake(client):
    r1 = client.post("/api/rmap-initiate", json={"client_pubkey_id": "Grp_08"})
    s1 = json.loads(base64.b64decode(r1.get_json()["payload"][4:].encode()).decode())
    enc2 = "enc:" + base64.b64encode(json.dumps(
        {"nonceClient":"C"*32,"nonceServer":s1["nonceServer"]}, sort_keys=True
    ).encode()).decode()
    r2 = client.post("/api/rmap-get-link", json={"client_pubkey_id":"Grp_08","payload":enc2})
    return r2.get_json()["result"]

def test_replay_fails(client):
    token = _handshake(client)
    ok = client.get(f"/api/rmap-download?token={token}")
    assert ok.status_code == 200 or ok.is_json  # 有的实现只返回 download_url
    bad = client.get(f"/api/rmap-download?token={token}")
    assert bad.status_code in (400, 401, 403, 410)

