#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RMAP 本地客户端测试脚本（修正版）
--------------------------------
用途：
  1) 生成 nonceClient + identity，用服务器公钥加密后 POST /rmap-initiate
  2) 用客户端私钥解密服务器返回，取出 nonceServer
  3) 只发送 {"nonceServer": ...}（⭐ 与作业表格一致）到 /rmap-get-link
  4) 处理两种返回：{"url": "..."} 或 {"result": "<32-hex>"}；若是 URL 自动下载 PDF

运行：
  python3 rmap_test_client.py
"""

import json, secrets, base64, sys
from pathlib import Path
import requests
from pgpy import PGPKey, PGPMessage

# ==============================
# 路径/配置（按你机器实际情况改）
# ==============================
ASSETS = Path("/home/lab/Desktop/tatou-team2/tatou_keys")
SERVER_PUB = ASSETS / "server_pub3.asc"
CLIENTS_DIR = ASSETS / "client_keys"
BASE_URL = "http://10.11.12.13:5000"  # 你的 Flask 服务地址

# 选择一个 identity（与你 server 的 clients_dir 里公钥一致）
IDENTITY = "Group_07"

# 客户端私钥（用来解密服务器回的 payload；没有就到 Step2 停）
CLIENT_PRIV_PATH = Path("/home/lab/Desktop/Group_07_Private_Key.asc")
CLIENT_PRIV_PASSPHRASE = None  # 如果有口令就填上

# 下载输出目录
OUT_DIR = Path("./rmap_downloads")
OUT_DIR.mkdir(parents=True, exist_ok=True)
# ==============================

def encrypt_for_server(plaintext: dict) -> str:
    """客户端用服务器公钥加密消息 -> base64(ASCII-armored) 字符串"""
    server_pub, _ = PGPKey.from_file(str(SERVER_PUB))
    msg = PGPMessage.new(json.dumps(plaintext))
    enc = server_pub.encrypt(msg)
    return base64.b64encode(str(enc).encode()).decode()


def decrypt_for_client(payload_b64: str, priv_path: Path, passphrase: str | None):
    """客户端用自己的私钥解密服务器返回的 payload（base64 装甲）"""
    priv, _ = PGPKey.from_file(str(priv_path))
    if passphrase:
        priv.unlock(passphrase)
    armored = base64.b64decode(payload_b64).decode()
    pgp_msg = PGPMessage.from_blob(armored)
    return json.loads(priv.decrypt(pgp_msg).message)


def main():
    print(f"[DEBUG] Using server pub: {SERVER_PUB}")
    if not SERVER_PUB.exists():
        print(f"[ERR] server_pub.asc not existed：{SERVER_PUB}")
        sys.exit(1)

    # ---------------------------
    # Step 1: C->S（Message1）
    # ---------------------------
    nonce_client = secrets.randbits(64)
    # ⭐ 与作业表一致：Message1 明文 = {"nonceClient": u64, "identity": "GroupName"}
    msg1_plain = {"nonceClient": nonce_client, "identity": IDENTITY}
    payload1 = encrypt_for_server(msg1_plain)

    print(f"[→] POST {BASE_URL}/rmap-initiate")
    r1 = requests.post(f"{BASE_URL}/rmap-initiate", json={"payload": payload1})
    print("[←] status:", r1.status_code)
    print("[←] body:", r1.text)

    if r1.status_code != 200:
        print("[!] /rmap-initiate 调用失败。")
        return

    data1 = r1.json()
    if "payload" not in data1:
        print("[!] 服务器没有返回 payload，无法继续。")
        return

    # ---------------------------
    # Step 2: 解密 S->C（Response1）
    # ---------------------------
    if not CLIENT_PRIV_PATH.exists():
        print(f"[i] 未找到客户端私钥 {CLIENT_PRIV_PATH}，到此结束（已完成 Step1/2）。")
        return

    print(f"[i]decrypt the server response using the server private key: {CLIENT_PRIV_PATH}")
    plain_resp1 = decrypt_for_client(data1["payload"], CLIENT_PRIV_PATH, CLIENT_PRIV_PASSPHRASE)

    # 服务器返回的明文应包含 nonceClient 与 nonceServer
    # 作业表格：rmap-initiate 返回的解密明文 = {"nonceClient": u64, "nonceServer": u64}
    nonce_server = int(plain_resp1["nonceServer"])
    nonce_client_echo = int(plain_resp1.get("nonceClient", -1))
    print(f"[✓] nonceServer = {nonce_server}")
    if nonce_client_echo != nonce_client:
        print(f"[!] 警告：服务器回显的 nonceClient={nonce_client_echo} 与本地发送的不一致！")

    # ---------------------------
    # Step 3: C->S（Message2）
    # ---------------------------
    # ⭐ 关键修改：根据表3，第二次加密消息只需要 {"nonceServer": u64}
    msg2_plain = {"nonceServer": nonce_server}
    payload2 = encrypt_for_server(msg2_plain)

    print(f"[→] POST {BASE_URL}/rmap-get-link")
    r2 = requests.post(f"{BASE_URL}/rmap-get-link", json={"payload": payload2})
    print("[←] status:", r2.status_code)
    print("[←] body:", r2.text)

    if r2.status_code != 200:
        print("[!] /rmap-get-link 调用失败。")
        return

    data2 = r2.json()

    # ---------------------------
    # Step 4: 处理返回（两种协议风格都支持）
    # ---------------------------
    if "url" in data2:
        url = data2["url"]
        print(f"[✓] succeed link：{url}")
        # 自动下载保存
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("application/pdf"):
                # 文件名用 url 尾部或生成一个
                name = url.rsplit("/", 1)[-1]
                if not name.endswith(".pdf"):
                    name = f"{name}.pdf"
                out_path = OUT_DIR / name
                out_path.write_bytes(resp.content)
                print(f"[✓] downloaded：{out_path.resolve()}")
            else:
                print(f"[!] 获取 PDF 失败：HTTP {resp.status_code} / Content-Type={resp.headers.get('Content-Type')}")
        except Exception as e:
            print(f"[!] 下载异常：{e}")

    elif "result" in data2:
        token = data2["result"]
        print(f"[✓] 四步握手成功！result = {token}")
        # 如果你的服务实现了 /dl/<sid>.pdf，可以尝试拼一个下载地址：
        # （注意：这取决于你的 Blueprint 是否有 url_prefix）
        guess_url = f"{BASE_URL}/dl/{token}.pdf"
        print(f"[i] 试着用猜测的下载地址获取：{guess_url}")
        resp = requests.get(guess_url, timeout=30)
        if resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("application/pdf"):
            out_path = OUT_DIR / f"{token}.pdf"
            out_path.write_bytes(resp.content)
            print(f"[✓] 已下载到：{out_path.resolve()}")
        else:
            print(f"[!] 下载失败（可能你的服务器不返回 URL、只返回 token，需要自己再 GET 正确的下载端点）。")
    else:
        print(f"[!] 未识别的响应：{data2}")


if __name__ == "__main__":
    main()

