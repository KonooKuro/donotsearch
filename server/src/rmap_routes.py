# -*- coding: utf-8 -*-
"""
rmap_routes.py
--------------
RMAP 四步握手的接口定义（Blueprint 版本）

提供两个API:
  - POST /rmap-initiate  (Step 1 -> Step 2)
  - POST /rmap-get-link  (Step 3 -> Step 4)
  - GET  /dl/<sid>.pdf   (下载水印PDF)
"""

from flask import Blueprint, request, jsonify, send_file, url_for
from pathlib import Path
from rmap.identity_manager import IdentityManager
from rmap.rmap import RMAP
from datetime import datetime, timedelta
from hidden import HiddenObjectB64Method
import hashlib
import os

# ------------------------------
# 会话（内存字典，仅教学用途）
# ------------------------------
_SESS = {}  # key: Ns -> {identity, Nc, Ns, expires_at}

def _save_session(identity, Nc, Ns, ttl=600):
    _SESS[Ns] = {
        "identity": identity,
        "Nc": int(Nc),
        "Ns": int(Ns),
        "expires_at": datetime.utcnow() + timedelta(seconds=ttl),
    }

def _pop_session_by_ns(Ns: int):
    rec = _SESS.get(int(Ns))
    if not rec:
        return None
    if rec["expires_at"] < datetime.utcnow():
        del _SESS[int(Ns)]
        return None
    del _SESS[int(Ns)]  # 一次性消费，防重放
    return rec

# ------------------------------
# 路径设置（尽量不要硬编码绝对路径）
# ------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]  # == 项目根（你原来 parent.parent.parent）
ASSET_DIR = BASE_DIR / "tatou_keys"
SRC_DIR   = BASE_DIR / "server" / "src"

# ⚠️ SUGGESTION: 把 PDF_BASE/OUT_DIR 改为相对项目根，避免换机路径失效
PDF_BASE    = (SRC_DIR / "Group_7.pdf").resolve()            # 老师给的PDF
PDF_OUT_DIR = (SRC_DIR / "storage").resolve()                # 输出目录
PDF_OUT_DIR.mkdir(parents=True, exist_ok=True)

clients_dir = ASSET_DIR / "client_keys"
server_pub  = ASSET_DIR / "server_pub.asc"
server_priv = ASSET_DIR / "server_priv.asc"

# 🔒 SUGGESTION: 私钥口令使用环境变量，避免硬编码泄露

im = IdentityManager(
    client_keys_dir=clients_dir,
    server_public_key_path=server_pub,
    server_private_key_path=server_priv,
)
rmap = RMAP(im)

# ------------------------------
# Blueprint 定义
# ------------------------------
rmap_bp = Blueprint("rmap", __name__)

# ⚠️ SUGGESTION: 用 "/" 当首页；如果注册时有 url_prefix="/rmap"，最终就是 /rmap/
@rmap_bp.route("/rmap", methods=["GET"])
def index():
    """根路由：用于测试服务是否正常运行"""
    return jsonify({
        "status": "RMAP server running",
        "endpoints": ["/rmap-initiate", "/rmap-get-link", "/get-version/<sid>"]  # ✅ 补上下载端点
    })

# ===========================================================
# Step 1 & Step 2: Client → Server (Message1)，Server → Client (Response1)
# ===========================================================
@rmap_bp.route("/rmap-initiate", methods=["POST"])
def rmap_initiate():
    try:
        msg1 = request.get_json(force=True)
        # 看看客户端传来的外层
        print("[RX] raw msg1 keys =", list(msg1.keys()), "payload_len=", len(msg1.get("payload","")))

        # 让库解密；如果这里抛异常，说明 server_priv / client 公钥问题
        resp1 = rmap.handle_message1(msg1)

        # 你的封装里应该把明文字段带出来，便于保存会话（identity/Nc/Ns）
        print("[RX] decrypted identity =", resp1.get("identity"),
              "Nc =", resp1.get("nonceClient"),
              "Ns =", resp1.get("nonceServer"))

        identity = resp1["identity"]
        Nc = int(resp1["nonceClient"])
        Ns = int(resp1["nonceServer"])
        _save_session(identity, Nc, Ns)

        return jsonify({"payload": resp1["payload"]})
    except Exception as e:
        print("[ERR] rmap-initiate failed:", repr(e))
        return jsonify({"error": str(e)}), 400

# ===========================================================
# Step 3 & Step 4: Client → Server (Message2)，Server → Client (Result/URL)
# ===========================================================
@rmap_bp.route("/rmap-get-link", methods=["POST"])
def rmap_get_link():
    """
    Step 3: 客户端 → 服务器
      - 客户端发送 {nonceServer}，用服务器公钥加密
    Step 4: 服务器 → 客户端
      - 服务器验证 nonces
      - 生成一次性 token (32位16进制)
      - 返回下载链接（或 token）
    """
    try:
        msg2 = request.get_json(force=True)
        parsed = rmap.handle_message2(msg2)

        # ⚠️ TODO: 确认 handle_message2 返回 {"nonceServer": Ns}
        Ns = int(parsed["nonceServer"])

        # 取出并校验会话（一致且未过期；一次性消费）
        sess = _pop_session_by_ns(Ns)
        if not sess:
            return jsonify({"error": "session not found or expired"}), 400

        identity = sess["identity"]
        Nc = int(sess["Nc"])

        # 会话 secret -> 32 hex token（题目要 32-hex）
        sid = hashlib.sha256(f"{Nc}:{Ns}".encode()).hexdigest()[:32]
        out_path = PDF_OUT_DIR / f"{sid}.pdf"

        # 使用你们的“最佳水印”（hidden.py）
        method = HiddenObjectB64Method()
        secret = f"{identity}:{sid}"  # ✅ 建议嵌入身份+一次性ID，便于回溯
        pdf_bytes = method.add_watermark(str(PDF_BASE), secret)

        with open(out_path, "wb") as f:
            f.write(pdf_bytes)

        try:
            import os
            sz = os.path.getsize(out_path)
            print(f"[RMAP] wrote {out_path} ({sz} bytes)")
        except Exception as e:
            print(f"[RMAP] write-check failed: (out_path)->{e}")
        # 返回可访问的下载URL（避免硬编码域名/端口）
        # download_url = url_for("rmap.download_pdf", sid=sid, _external=True)
        # return jsonify({"url": download_url})

        # 如果课程严格要求 {"result":"<32-hex>"}：
        return jsonify({"result": sid})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
@rmap_bp.route("/get-version/<sid>", methods=["GET"])
def api_get_version(sid: str):
    try:
        print(f"[RMAP] api_get_version sid={sid!r}")

        # 1) 校验 32-hex
        if (not isinstance(sid, str) or len(sid) != 32
                or any(c not in "0123456789abcdefABCDEF" for c in sid)):
            print("[RMAP] invalid token format")
            return jsonify({"error": "invalid token"}), 400

        # 2) 目标文件
        path = PDF_OUT_DIR / f"{sid}.pdf"
        print(f"[RMAP] target path = {path}")

        if not path.exists():
            print("[RMAP] file not found")
            return jsonify({"error": "file not found"}), 404

        # 3) 大小/权限检查
        import os
        try:
            st = os.stat(path)
            print(f"[RMAP] file size = {st.st_size} bytes, mode={oct(st.st_mode)}")
            if st.st_size == 0:
                print("[RMAP] file is empty (size=0)")
        except Exception as e:
            print(f"[RMAP] os.stat failed: {e}")

        # 4) 发送文件
        return send_file(
            str(path),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{sid}.pdf",
            max_age=0
        )

    except Exception as e:
        # 捕获所有未预期错误，避免框架把它包成 503
        import traceback
        print("[RMAP] api_get_version ERROR:", e)
        traceback.print_exc()
        return jsonify({"error": "server error", "detail": str(e)}), 500


print("[rmap_test]client_keys_dir = ",clients_dir)
ids = sorted([p.stem for p in Path(clients_dir).glob("*.asc")])
print("[rmap_test] accepted identities:",ids)
