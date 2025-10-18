"""
identity_manager.py
-------------------
管理密钥加载 & 加解密
"""

import base64
import json
from pathlib import Path
from pgpy import PGPKey, PGPMessage

print("ooooooooooooooooo")

class IdentityManager:
    def __init__(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None):
        print("xxxxxxxxxxxx")
        self.client_keys_dir = client_keys_dir
        print("Debug place 1")
        self.server_pub, _ = PGPKey.from_file(str(server_public_key_path))
        print("Debug place 2")
        self.server_priv = None

        if server_private_key_path and Path(server_private_key_path).exists():
            print("Debug place 3")
            self.server_priv, _ = PGPKey.from_file(str(server_private_key_path))
                
    # ========== 客户端 → 服务端 ==========
    def encrypt_for_server(self, plaintext: dict) -> str:
        """客户端用服务器公钥加密消息"""
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = self.server_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    def decrypt_for_server(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("Server private key not loaded!")
        armored = base64.b64decode(payload).decode()
        pgp_msg = PGPMessage.from_blob(armored)

        if hasattr(self, 'server_passphrase') and self.server_passphrase:
            with self.server_priv.unlock(self.server_passphrase):
                decrypted = self.server_priv.decrypt(pgp_msg)
        else:
            decrypted = self.server_priv.decrypt(pgp_msg)

        return json.loads(decrypted.message)

    # ========== 服务端 → 客户端 ==========
    def encrypt_for_client(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()
