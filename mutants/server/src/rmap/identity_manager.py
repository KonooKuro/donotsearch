"""
identity_manager.py
-------------------
管理密钥加载 & 加解密
"""

import base64
import json
from pathlib import Path
from pgpy import PGPKey, PGPMessage
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


class IdentityManager:
    def xǁIdentityManagerǁ__init____mutmut_orig(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = PGPKey.from_file(str(server_public_key_path))

        self.server_priv = None
        if server_private_key_path and Path(server_private_key_path).exists():
            self.server_priv, _ = PGPKey.from_file(str(server_private_key_path))
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_1(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = None
        self.server_pub, _ = PGPKey.from_file(str(server_public_key_path))

        self.server_priv = None
        if server_private_key_path and Path(server_private_key_path).exists():
            self.server_priv, _ = PGPKey.from_file(str(server_private_key_path))
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_2(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = None

        self.server_priv = None
        if server_private_key_path and Path(server_private_key_path).exists():
            self.server_priv, _ = PGPKey.from_file(str(server_private_key_path))
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_3(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = PGPKey.from_file(None)

        self.server_priv = None
        if server_private_key_path and Path(server_private_key_path).exists():
            self.server_priv, _ = PGPKey.from_file(str(server_private_key_path))
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_4(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = PGPKey.from_file(str(None))

        self.server_priv = None
        if server_private_key_path and Path(server_private_key_path).exists():
            self.server_priv, _ = PGPKey.from_file(str(server_private_key_path))
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_5(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = PGPKey.from_file(str(server_public_key_path))

        self.server_priv = ""
        if server_private_key_path and Path(server_private_key_path).exists():
            self.server_priv, _ = PGPKey.from_file(str(server_private_key_path))
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_6(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = PGPKey.from_file(str(server_public_key_path))

        self.server_priv = None
        if server_private_key_path or Path(server_private_key_path).exists():
            self.server_priv, _ = PGPKey.from_file(str(server_private_key_path))
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_7(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = PGPKey.from_file(str(server_public_key_path))

        self.server_priv = None
        if server_private_key_path and Path(None).exists():
            self.server_priv, _ = PGPKey.from_file(str(server_private_key_path))
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_8(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = PGPKey.from_file(str(server_public_key_path))

        self.server_priv = None
        if server_private_key_path and Path(server_private_key_path).exists():
            self.server_priv, _ = None
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_9(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = PGPKey.from_file(str(server_public_key_path))

        self.server_priv = None
        if server_private_key_path and Path(server_private_key_path).exists():
            self.server_priv, _ = PGPKey.from_file(None)
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_10(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = PGPKey.from_file(str(server_public_key_path))

        self.server_priv = None
        if server_private_key_path and Path(server_private_key_path).exists():
            self.server_priv, _ = PGPKey.from_file(str(None))
            if server_private_key_passphrase:
                self.server_priv.unlock(server_private_key_passphrase)
    def xǁIdentityManagerǁ__init____mutmut_11(self, client_keys_dir: Path, server_public_key_path: Path,
                 server_private_key_path: Path = None, server_private_key_passphrase: str = None):
        self.client_keys_dir = client_keys_dir
        self.server_pub, _ = PGPKey.from_file(str(server_public_key_path))

        self.server_priv = None
        if server_private_key_path and Path(server_private_key_path).exists():
            self.server_priv, _ = PGPKey.from_file(str(server_private_key_path))
            if server_private_key_passphrase:
                self.server_priv.unlock(None)
    
    xǁIdentityManagerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁIdentityManagerǁ__init____mutmut_1': xǁIdentityManagerǁ__init____mutmut_1, 
        'xǁIdentityManagerǁ__init____mutmut_2': xǁIdentityManagerǁ__init____mutmut_2, 
        'xǁIdentityManagerǁ__init____mutmut_3': xǁIdentityManagerǁ__init____mutmut_3, 
        'xǁIdentityManagerǁ__init____mutmut_4': xǁIdentityManagerǁ__init____mutmut_4, 
        'xǁIdentityManagerǁ__init____mutmut_5': xǁIdentityManagerǁ__init____mutmut_5, 
        'xǁIdentityManagerǁ__init____mutmut_6': xǁIdentityManagerǁ__init____mutmut_6, 
        'xǁIdentityManagerǁ__init____mutmut_7': xǁIdentityManagerǁ__init____mutmut_7, 
        'xǁIdentityManagerǁ__init____mutmut_8': xǁIdentityManagerǁ__init____mutmut_8, 
        'xǁIdentityManagerǁ__init____mutmut_9': xǁIdentityManagerǁ__init____mutmut_9, 
        'xǁIdentityManagerǁ__init____mutmut_10': xǁIdentityManagerǁ__init____mutmut_10, 
        'xǁIdentityManagerǁ__init____mutmut_11': xǁIdentityManagerǁ__init____mutmut_11
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁIdentityManagerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁIdentityManagerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁIdentityManagerǁ__init____mutmut_orig)
    xǁIdentityManagerǁ__init____mutmut_orig.__name__ = 'xǁIdentityManagerǁ__init__'

    # ========== 客户端 → 服务端 ==========
    def xǁIdentityManagerǁencrypt_for_server__mutmut_orig(self, plaintext: dict) -> str:
        """客户端用服务器公钥加密消息"""
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = self.server_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 客户端 → 服务端 ==========
    def xǁIdentityManagerǁencrypt_for_server__mutmut_1(self, plaintext: dict) -> str:
        """客户端用服务器公钥加密消息"""
        msg = None
        enc = self.server_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 客户端 → 服务端 ==========
    def xǁIdentityManagerǁencrypt_for_server__mutmut_2(self, plaintext: dict) -> str:
        """客户端用服务器公钥加密消息"""
        msg = PGPMessage.new(None)
        enc = self.server_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 客户端 → 服务端 ==========
    def xǁIdentityManagerǁencrypt_for_server__mutmut_3(self, plaintext: dict) -> str:
        """客户端用服务器公钥加密消息"""
        msg = PGPMessage.new(json.dumps(None))
        enc = self.server_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 客户端 → 服务端 ==========
    def xǁIdentityManagerǁencrypt_for_server__mutmut_4(self, plaintext: dict) -> str:
        """客户端用服务器公钥加密消息"""
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = None
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 客户端 → 服务端 ==========
    def xǁIdentityManagerǁencrypt_for_server__mutmut_5(self, plaintext: dict) -> str:
        """客户端用服务器公钥加密消息"""
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = self.server_pub.encrypt(None)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 客户端 → 服务端 ==========
    def xǁIdentityManagerǁencrypt_for_server__mutmut_6(self, plaintext: dict) -> str:
        """客户端用服务器公钥加密消息"""
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = self.server_pub.encrypt(msg)
        return base64.b64encode(None).decode()

    # ========== 客户端 → 服务端 ==========
    def xǁIdentityManagerǁencrypt_for_server__mutmut_7(self, plaintext: dict) -> str:
        """客户端用服务器公钥加密消息"""
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = self.server_pub.encrypt(msg)
        return base64.b64encode(str(None).encode()).decode()
    
    xǁIdentityManagerǁencrypt_for_server__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁIdentityManagerǁencrypt_for_server__mutmut_1': xǁIdentityManagerǁencrypt_for_server__mutmut_1, 
        'xǁIdentityManagerǁencrypt_for_server__mutmut_2': xǁIdentityManagerǁencrypt_for_server__mutmut_2, 
        'xǁIdentityManagerǁencrypt_for_server__mutmut_3': xǁIdentityManagerǁencrypt_for_server__mutmut_3, 
        'xǁIdentityManagerǁencrypt_for_server__mutmut_4': xǁIdentityManagerǁencrypt_for_server__mutmut_4, 
        'xǁIdentityManagerǁencrypt_for_server__mutmut_5': xǁIdentityManagerǁencrypt_for_server__mutmut_5, 
        'xǁIdentityManagerǁencrypt_for_server__mutmut_6': xǁIdentityManagerǁencrypt_for_server__mutmut_6, 
        'xǁIdentityManagerǁencrypt_for_server__mutmut_7': xǁIdentityManagerǁencrypt_for_server__mutmut_7
    }
    
    def encrypt_for_server(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁIdentityManagerǁencrypt_for_server__mutmut_orig"), object.__getattribute__(self, "xǁIdentityManagerǁencrypt_for_server__mutmut_mutants"), args, kwargs, self)
        return result 
    
    encrypt_for_server.__signature__ = _mutmut_signature(xǁIdentityManagerǁencrypt_for_server__mutmut_orig)
    xǁIdentityManagerǁencrypt_for_server__mutmut_orig.__name__ = 'xǁIdentityManagerǁencrypt_for_server'

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_orig(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("Server private key not loaded!")
        armored = base64.b64decode(payload).decode()
        pgp_msg = PGPMessage.from_blob(armored)
        return json.loads(self.server_priv.decrypt(pgp_msg).message)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_1(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is not None:
            raise ValueError("Server private key not loaded!")
        armored = base64.b64decode(payload).decode()
        pgp_msg = PGPMessage.from_blob(armored)
        return json.loads(self.server_priv.decrypt(pgp_msg).message)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_2(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError(None)
        armored = base64.b64decode(payload).decode()
        pgp_msg = PGPMessage.from_blob(armored)
        return json.loads(self.server_priv.decrypt(pgp_msg).message)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_3(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("XXServer private key not loaded!XX")
        armored = base64.b64decode(payload).decode()
        pgp_msg = PGPMessage.from_blob(armored)
        return json.loads(self.server_priv.decrypt(pgp_msg).message)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_4(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("server private key not loaded!")
        armored = base64.b64decode(payload).decode()
        pgp_msg = PGPMessage.from_blob(armored)
        return json.loads(self.server_priv.decrypt(pgp_msg).message)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_5(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("SERVER PRIVATE KEY NOT LOADED!")
        armored = base64.b64decode(payload).decode()
        pgp_msg = PGPMessage.from_blob(armored)
        return json.loads(self.server_priv.decrypt(pgp_msg).message)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_6(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("Server private key not loaded!")
        armored = None
        pgp_msg = PGPMessage.from_blob(armored)
        return json.loads(self.server_priv.decrypt(pgp_msg).message)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_7(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("Server private key not loaded!")
        armored = base64.b64decode(None).decode()
        pgp_msg = PGPMessage.from_blob(armored)
        return json.loads(self.server_priv.decrypt(pgp_msg).message)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_8(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("Server private key not loaded!")
        armored = base64.b64decode(payload).decode()
        pgp_msg = None
        return json.loads(self.server_priv.decrypt(pgp_msg).message)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_9(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("Server private key not loaded!")
        armored = base64.b64decode(payload).decode()
        pgp_msg = PGPMessage.from_blob(None)
        return json.loads(self.server_priv.decrypt(pgp_msg).message)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_10(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("Server private key not loaded!")
        armored = base64.b64decode(payload).decode()
        pgp_msg = PGPMessage.from_blob(armored)
        return json.loads(None)

    def xǁIdentityManagerǁdecrypt_for_server__mutmut_11(self, payload: str) -> dict:
        """服务端用服务器私钥解密消息"""
        if self.server_priv is None:
            raise ValueError("Server private key not loaded!")
        armored = base64.b64decode(payload).decode()
        pgp_msg = PGPMessage.from_blob(armored)
        return json.loads(self.server_priv.decrypt(None).message)
    
    xǁIdentityManagerǁdecrypt_for_server__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁIdentityManagerǁdecrypt_for_server__mutmut_1': xǁIdentityManagerǁdecrypt_for_server__mutmut_1, 
        'xǁIdentityManagerǁdecrypt_for_server__mutmut_2': xǁIdentityManagerǁdecrypt_for_server__mutmut_2, 
        'xǁIdentityManagerǁdecrypt_for_server__mutmut_3': xǁIdentityManagerǁdecrypt_for_server__mutmut_3, 
        'xǁIdentityManagerǁdecrypt_for_server__mutmut_4': xǁIdentityManagerǁdecrypt_for_server__mutmut_4, 
        'xǁIdentityManagerǁdecrypt_for_server__mutmut_5': xǁIdentityManagerǁdecrypt_for_server__mutmut_5, 
        'xǁIdentityManagerǁdecrypt_for_server__mutmut_6': xǁIdentityManagerǁdecrypt_for_server__mutmut_6, 
        'xǁIdentityManagerǁdecrypt_for_server__mutmut_7': xǁIdentityManagerǁdecrypt_for_server__mutmut_7, 
        'xǁIdentityManagerǁdecrypt_for_server__mutmut_8': xǁIdentityManagerǁdecrypt_for_server__mutmut_8, 
        'xǁIdentityManagerǁdecrypt_for_server__mutmut_9': xǁIdentityManagerǁdecrypt_for_server__mutmut_9, 
        'xǁIdentityManagerǁdecrypt_for_server__mutmut_10': xǁIdentityManagerǁdecrypt_for_server__mutmut_10, 
        'xǁIdentityManagerǁdecrypt_for_server__mutmut_11': xǁIdentityManagerǁdecrypt_for_server__mutmut_11
    }
    
    def decrypt_for_server(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁIdentityManagerǁdecrypt_for_server__mutmut_orig"), object.__getattribute__(self, "xǁIdentityManagerǁdecrypt_for_server__mutmut_mutants"), args, kwargs, self)
        return result 
    
    decrypt_for_server.__signature__ = _mutmut_signature(xǁIdentityManagerǁdecrypt_for_server__mutmut_orig)
    xǁIdentityManagerǁdecrypt_for_server__mutmut_orig.__name__ = 'xǁIdentityManagerǁdecrypt_for_server'

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_orig(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_1(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = None
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_2(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir * f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_3(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_4(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(None)
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_5(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = None
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_6(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(None)
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_7(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(None))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_8(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = None
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_9(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(None)
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_10(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(None))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_11(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = None
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_12(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(None)
        return base64.b64encode(str(enc).encode()).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_13(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(None).decode()

    # ========== 服务端 → 客户端 ==========
    def xǁIdentityManagerǁencrypt_for_client__mutmut_14(self, identity: str, plaintext: dict) -> str:
        """服务端用客户端公钥加密消息"""
        client_pub_path = self.client_keys_dir / f"{identity}.asc"
        if not client_pub_path.exists():
            raise FileNotFoundError(f"Missing client key: {client_pub_path}")
        client_pub, _ = PGPKey.from_file(str(client_pub_path))
        msg = PGPMessage.new(json.dumps(plaintext))
        enc = client_pub.encrypt(msg)
        return base64.b64encode(str(None).encode()).decode()
    
    xǁIdentityManagerǁencrypt_for_client__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁIdentityManagerǁencrypt_for_client__mutmut_1': xǁIdentityManagerǁencrypt_for_client__mutmut_1, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_2': xǁIdentityManagerǁencrypt_for_client__mutmut_2, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_3': xǁIdentityManagerǁencrypt_for_client__mutmut_3, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_4': xǁIdentityManagerǁencrypt_for_client__mutmut_4, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_5': xǁIdentityManagerǁencrypt_for_client__mutmut_5, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_6': xǁIdentityManagerǁencrypt_for_client__mutmut_6, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_7': xǁIdentityManagerǁencrypt_for_client__mutmut_7, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_8': xǁIdentityManagerǁencrypt_for_client__mutmut_8, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_9': xǁIdentityManagerǁencrypt_for_client__mutmut_9, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_10': xǁIdentityManagerǁencrypt_for_client__mutmut_10, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_11': xǁIdentityManagerǁencrypt_for_client__mutmut_11, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_12': xǁIdentityManagerǁencrypt_for_client__mutmut_12, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_13': xǁIdentityManagerǁencrypt_for_client__mutmut_13, 
        'xǁIdentityManagerǁencrypt_for_client__mutmut_14': xǁIdentityManagerǁencrypt_for_client__mutmut_14
    }
    
    def encrypt_for_client(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁIdentityManagerǁencrypt_for_client__mutmut_orig"), object.__getattribute__(self, "xǁIdentityManagerǁencrypt_for_client__mutmut_mutants"), args, kwargs, self)
        return result 
    
    encrypt_for_client.__signature__ = _mutmut_signature(xǁIdentityManagerǁencrypt_for_client__mutmut_orig)
    xǁIdentityManagerǁencrypt_for_client__mutmut_orig.__name__ = 'xǁIdentityManagerǁencrypt_for_client'
