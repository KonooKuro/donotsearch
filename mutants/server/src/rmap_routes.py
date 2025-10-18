"""
rmap_routes.py
--------------
RMAP 四步握手的接口定义（Blueprint 版本）

提供两个API:
  - POST /rmap-initiate  (Step 1 -> Step 2)
  - POST /rmap-get-link  (Step 3 -> Step 4)
"""

from flask import Blueprint, request, jsonify
from pathlib import Path
from rmap.identity_manager import IdentityManager
from rmap.rmap import RMAP

# ------------------------------
# 初始化 IdentityManager & RMAP
# ------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSET_DIR = BASE_DIR / "tatou_keys"

clients_dir = ASSET_DIR / "client_keys"
server_pub = ASSET_DIR / "server_pub.asc"
server_priv = ASSET_DIR / "server_priv.asc"

im = IdentityManager(
    client_keys_dir=clients_dir,
    server_public_key_path=server_pub,
    server_private_key_path=server_priv,
    server_private_key_passphrase="Wjj15800593543"  # 你的服务器私钥口令
)
rmap = RMAP(im)

# ------------------------------
# Blueprint 定义
# ------------------------------
rmap_bp = Blueprint("rmap", __name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

@rmap_bp.route("/", methods=["GET"])
def index():
    """根路由：用于测试服务是否正常运行"""
    return jsonify({
        "status": "RMAP server running",
        "endpoints": ["/rmap-initiate", "/rmap-get-link"]
    })


# ===========================================================
# Step 1 & Step 2: Client → Server (Message1)，Server → Client (Response1)
# ===========================================================
@rmap_bp.route("/rmap-initiate", methods=["POST"])
def rmap_initiate():
    """
    Step 1: 客户端 → 服务器
      - 客户端发送 {nonceClient, identity}，用服务器公钥加密
    Step 2: 服务器 → 客户端
      - 服务器生成 nonceServer
      - 返回 {nonceServer}，用客户端公钥加密
    """
    try:
        msg1 = request.get_json()
        resp1 = rmap.handle_message1(msg1)
        return jsonify(resp1)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ===========================================================
# Step 3 & Step 4: Client → Server (Message2)，Server → Client (Result)
# ===========================================================
@rmap_bp.route("/rmap-get-link", methods=["POST"])
def rmap_get_link():
    """
    Step 3: 客户端 → 服务器
      - 客户端发送 {nonceClient, nonceServer}，用服务器公钥加密
    Step 4: 服务器 → 客户端
      - 服务器验证 nonces
      - 拼接 (nonceClient << 64) | nonceServer
      - 返回 result (32位16进制字符串)
    """
    try:
        msg2 = request.get_json()
        resp2 = rmap.handle_message2(msg2)
        return jsonify(resp2)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
