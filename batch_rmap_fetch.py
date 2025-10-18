#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_rmap_fetch.py
批量对各组发起 RMAP 四步握手并下载水印 PDF（兼容多种返回格式）

使用前请在“配置区”检查/修改：
- OUR_IDENTITY: 你们自己的组名（非常关键）
- CLIENT_PRIV_PATH / CLIENT_PRIV_PASSPHRASE: 你们客户端私钥与口令
- SERVER_PUB_DIR: 存放各组“服务器公钥”的目录（不是 client_keys）
- PORT: 对方服务器端口（默认 5000）
"""

import json, base64, secrets, time
from pathlib import Path
import requests
from pgpy import PGPKey, PGPMessage

# ===================== 配置区（按需修改） =====================

OUR_IDENTITY = "Group_07"  # ★★★ 必须是“你们自己的组名”，不是对方的

CLIENT_PRIV_PATH = Path("/home/lab/Desktop/Group_07_Private_Key.asc")  # 你的私钥
CLIENT_PRIV_PASSPHRASE = None  # 有口令写字符串，否则 None

# 存放“各组服务器公钥”的目录；脚本会在此找 <Group_XX>.asc。没有则尝试去目标主机拉取。
SERVER_PUB_DIR = Path("/home/lab/Desktop/tatou-team2/tatou_keys/client_keys")
SERVER_PUB_DIR.mkdir(parents=True, exist_ok=True)

# 若本地没有对方 server_pub.asc，尝试在目标主机这些路径拉取：
SERVER_PUB_URL_CANDIDATES = [
    "/server_pub.asc",
    "/rmap/server_pub.asc",
    "/tatou_keys/server_pub.asc",
    "/keys/server_pub.asc",
]

PORT = 5000
HTTP_TIMEOUT = 8
RETRY_ATTEMPTS = 2
SLEEP_BETWEEN = 0.4

DOWNLOAD_DIR = Path("./downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 目标列表（带 health）；USE_ONLY_HEALTH_OK=True 时只访问 OK 的
TARGETS_ALL = [
    ("Group_19","10.11.12.17","OK"),
    ("Group_08","10.11.12.7","OK"),
    ("Group_22","10.11.12.8","OK"),
    ("Group_20","10.11.12.9","OK"),
    ("Group_09","10.11.12.10","OK"),
    ("Group_14","10.11.12.18","OK"),
    ("Group_04","10.11.12.19","OK"),
    ("Group_26","10.11.12.12","OK"),
    ("Group_03","10.11.12.13","OK"),
    ("Group_07","10.11.12.14","OK"),
    ("Group_24","10.11.12.15","OK"),
]
USE_ONLY_HEALTH_OK = True
TARGETS = [(g, ip) for (g, ip, h) in TARGETS_ALL if (not USE_ONLY_HEALTH_OK) or (h.upper() == "OK")]

# =======DEBUG_BUTTEN==============
DEBUG = True

def log(*a):
    if DEBUG:
        print(*a)

def preview_response(r):
    try:
        t = r.text.strip().replace("\n","")
        return t[:180] + ("..." if len(t) > 180 else "")
    except Exception:
       return "<no text>"

from pgpy import PGPKey
def key_fingerprint(pub_path: Path) -> str:
    try:
        k, _ = PGPKey.from_file(str(pub_path))
        return str(k.fingerprint)
    except Exception:
        return "<fp-error>"

# ===================== 工具函数 =====================

def is_pgp_public_key(text: str) -> bool:
    return "BEGIN PGP PUBLIC KEY BLOCK" in text

def local_server_pub_path(group_name: str) -> Path:
    # 以组名存 server 公钥：peer_server_pubs/Group_11.asc
    return SERVER_PUB_DIR / f"{group_name}.asc"

def fetch_and_cache_server_pub(ip: str, group_name: str) -> Path | None:
    base = f"http://{ip}:{PORT}"
    for rel in SERVER_PUB_URL_CANDIDATES:
        url = base + rel
        try:
            r = requests.get(url, timeout=HTTP_TIMEOUT)
            if r.status_code == 200 and is_pgp_public_key(r.text):
                p = local_server_pub_path(group_name)
                p.write_text(r.text)
                print(f"[INFO] cached server_pub for {group_name} from {url} -> {p}")
                return p
        except Exception:
            pass
    return None

def find_or_get_server_pub(group_name: str, ip: str) -> Path | None:
    p = local_server_pub_path(group_name)
    if p.exists():
        return p
    else:
        print(f"[WARN]{group_name}public key fail found,homefile:{p}")
        return None

def encrypt_for_server(plaintext: dict, server_pub_path: Path) -> str:
    """PGP 装甲 -> 再 base64 外包一层（通用做法）"""
    pub, _ = PGPKey.from_file(str(server_pub_path))
    msg = PGPMessage.new(json.dumps(plaintext))
    enc = pub.encrypt(msg)
    return base64.b64encode(str(enc).encode()).decode()

def decrypt_for_client(payload_any, priv_path: Path, passphrase: str | None):
    """
    兼容三种服务端返回：
      A) base64(ASCII-armored PGP)
      B) ASCII-armored PGP
      C) base64(二进制 PGP)
    """
    priv, _ = PGPKey.from_file(str(priv_path))
    if passphrase:
        priv.unlock(passphrase)

    if not isinstance(payload_any, (str, bytes)):
        raise ValueError(f"unexpected payload type: {type(payload_any)}")

    payload = payload_any if isinstance(payload_any, str) else payload_any.decode("latin1", errors="ignore")

    try:
        raw = base64.b64decode(payload, validate=False)
        try:
            armored_str = raw.decode("utf-8")
            pgp_msg = PGPMessage.from_blob(armored_str)  # A
        except UnicodeDecodeError:
            pgp_msg = PGPMessage.from_blob(raw)          # C
    except Exception:
        pgp_msg = PGPMessage.from_blob(payload)         # B

    decrypted = priv.decrypt(pgp_msg).message
    return json.loads(decrypted)

def try_post_or_get(url, json_body):
    for attempt in range(RETRY_ATTEMPTS):
        try:
            r = requests.post(url, json=json_body, timeout=HTTP_TIMEOUT)
            if r.status_code == 405:
                r = requests.get(url, timeout=HTTP_TIMEOUT)
            return r
        except Exception as e:
            if attempt + 1 < RETRY_ATTEMPTS:
                time.sleep(SLEEP_BETWEEN)
            else:
                raise

def preview_response(r):
    try:
        text = r.text.strip().replace("\n","")
        return text[:180] + ("..." if len(text)>180 else "")
    except Exception:
        return str(r)

# ===================== 主流程 =====================

def run_one_target(group_name: str, ip: str):
    print(f"\n=== {group_name} @ {ip} ===")

    # 1) 准备“对方服务器公钥”
    server_pub = find_or_get_server_pub(group_name, ip)
    if server_pub is None:
        print(f"[SKIP] 无法获取 {group_name} 的 server_pub.asc")
        return {"group": group_name, "ip": ip, "ok": False, "reason": "no_server_pub"}
    log(f"[DBG] using server_pub: {server_pub}  fp={key_fingerprint(server_pub)}")

    base_url = f"http://{ip}:{PORT}"
    # 有的组使用前缀 /rmap，有的没有；都尝试

    ROUTE_CANDIDATES_INIT = [
        "/api/rmap-initiate",
        "/rmap/rmap-initiate",
        "/rmap-initiate",
        "/initiate"
]

    ROUTE_CANDIDATES_GETLINK = [
        "/api/rmap-get-link",
        "/rmap-get-link",
        "/rmap/rmap-get-link",
        "/get-link"
]

    init_urls = [f"{base_url}{r}" for r in ROUTE_CANDIDATES_INIT]
    getlink_urls = [f"{base_url}{r}" for r in ROUTE_CANDIDATES_GETLINK]

    # 2) Step1：C->S（用“对方 server 公钥”），identity 必须是“我们自己”
    nonce_client = secrets.randbits(64)
    m1_plain = {"nonceClient": nonce_client, "identity": OUR_IDENTITY}
    payload1 = encrypt_for_server(m1_plain, server_pub)
    log(f"[STEP1] identity={OUR_IDENTITY}  Nc={nonce_client}")

    r1 = None
    for u in init_urls:
        log(f"[->]{u}  (POST;405->GET)")
        try:
            r1 = try_post_or_get(u, {"payload": payload1})
        except Exception as e:
            print(f"[ERR]POST/GET {u} fail: {e}")
            continue
        print(f"[<-] {u} {r1.status_code}{preview_response(r1)}")
        if r1.status_code == 200:
            break
    if r1 is None or r1.status_code != 200:
        return {"group": group_name, "ip": ip, "ok": False, "reason": f"post_init_failed({r1.status_code if r1 else 'no_response'})"}

    try:
        data1 = r1.json()
    except Exception:
        return {"group": group_name, "ip": ip, "ok": False, "reason": f"bad_json_init: {r1.text[:150]!r}"}
    if "payload" not in data1:
        return {"group": group_name, "ip": ip, "ok": False, "reason": data1}

    # 3) Step2：S->C（用我们的私钥解密）
    if not CLIENT_PRIV_PATH.exists():
        return {"group": group_name, "ip": ip, "ok": False, "reason": "no_client_priv"}
    try:
        resp1_plain = decrypt_for_client(data1["payload"], CLIENT_PRIV_PATH, CLIENT_PRIV_PASSPHRASE)
    except Exception as e:
        return {"group": group_name, "ip": ip, "ok": False, "reason": f"decrypt_resp1_err: {e}"}

    nonce_server = resp1_plain.get("nonceServer")
    if nonce_server is None:
        return {"group": group_name, "ip": ip, "ok": False, "reason": f"no_nonceServer_in_resp1: {resp1_plain}"}

    # 4) Step3：C->S（只发 nonceServer；仍用对方 server 公钥加密）
    m2_plain = {"nonceServer": int(nonce_server)}
    payload2 = encrypt_for_server(m2_plain, server_pub)

    r2 = None
    for u in getlink_urls:
        try:
            r2 = try_post_or_get(u, {"payload": payload2})
            print(f"[→] {u} -> {r2.status_code}")
            if r2.status_code == 200:
                break
        except Exception as e:
            print(f"[ERR] POST {u} 失败: {e}")
    if r2 is None or r2.status_code != 200:
        reason = f"post_getlink_failed ({r2.status_code if r2 else 'no_response'})"
        return {"group": group_name, "ip": ip, "ok": False, "reason": reason}

    try:
        data2 = r2.json()
    except Exception:
        return {"group": group_name, "ip": ip, "ok": False, "reason": f"bad_json_getlink: {r2.text[:150]!r}"}

    # 5) Step4：下载（优先用返回的 url；否则用 result 组装两种可能路径）
    if "url" in data2:
        candidate_urls = [data2["url"]]
        log(f"[DEBUG] url={data2['url']}")
    elif "result" in data2:
        sid = data2["result"]
        candidate_urls = [f"{base_url}/dl/{sid}.pdf", f"{base_url}/api/get-version/{sid}", f"{base_url}/api/get-version/{sid}.pdf"]
        log(f"[DEBUG] result={sid} candidates={candidate_urls}")
    else:
        return {"group": group_name, "ip": ip, "ok": False, "reason": data2}

    for du in candidate_urls:
        try:
            rr = requests.get(du, timeout=HTTP_TIMEOUT)
            print(f"[DEBUG] {du} -> {rr.status_code} {rr.headers.get('Content-Type','')}")
            if rr.status_code == 200 and rr.headers.get("Content-Type","").startswith("application/pdf"):
                name = f"{group_name}_{ip.replace(':','_')}.pdf"  # 以组名+IP命名
                out = DOWNLOAD_DIR / name
                out.write_bytes(rr.content)
                print(f"[OK] 下载成功 -> {out}")
                return {"group": group_name, "ip": ip, "ok": True, "file": str(out)}
        except Exception as e:
            log(f"[ERR] DOWNLODED ERROR: {e}")

    return {"group": group_name, "ip": ip, "ok": False, "reason": "download_failed"}

def main():
    print("Batch RMAP fetch (server_pub + tolerant decrypt) starting...")
    results = []
    for grp, ip in TARGETS:
        res = run_one_target(grp, ip)
        results.append(res)
        time.sleep(0.2)

    # 导出结果 CSV
    import csv
    with open("batch_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["group","ip","ok","file","reason"])
        writer.writeheader()
        for r in results:
            writer.writerow({
                "group": r.get("group"),
                "ip": r.get("ip"),
                "ok": r.get("ok"),
                "file": r.get("file",""),
                "reason": r.get("reason",""),
            })
    print("Done. Results written to batch_results.csv")

if __name__ == "__main__":
    main()
