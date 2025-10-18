"""
rmap.py
-------
RMAP 四步握手核心逻辑
"""

import secrets
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


class RMAP:
    def xǁRMAPǁ__init____mutmut_orig(self, identity_manager):
        self.im = identity_manager
        self.session = {}  # 存放会话状态
    def xǁRMAPǁ__init____mutmut_1(self, identity_manager):
        self.im = None
        self.session = {}  # 存放会话状态
    def xǁRMAPǁ__init____mutmut_2(self, identity_manager):
        self.im = identity_manager
        self.session = None  # 存放会话状态
    
    xǁRMAPǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRMAPǁ__init____mutmut_1': xǁRMAPǁ__init____mutmut_1, 
        'xǁRMAPǁ__init____mutmut_2': xǁRMAPǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRMAPǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRMAPǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁRMAPǁ__init____mutmut_orig)
    xǁRMAPǁ__init____mutmut_orig.__name__ = 'xǁRMAPǁ__init__'

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_orig(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_1(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = None
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_2(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(None)
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_3(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["XXpayloadXX"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_4(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["PAYLOAD"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_5(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = None
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_6(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(None)
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_7(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["XXnonceClientXX"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_8(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceclient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_9(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["NONCECLIENT"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_10(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = None

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_11(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["XXidentityXX"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_12(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["IDENTITY"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_13(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = None

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_14(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(None)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_15(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(65)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_16(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = None

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_17(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "XXnonceClientXX": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_18(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceclient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_19(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "NONCECLIENT": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_20(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "XXnonceServerXX": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_21(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceserver": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_22(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "NONCESERVER": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_23(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = None
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_24(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"XXnonceServerXX": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_25(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceserver": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_26(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"NONCESERVER": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_27(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = None

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_28(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(None, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_29(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, None)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_30(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_31(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, )

            return {"payload": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_32(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"XXpayloadXX": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_33(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"PAYLOAD": encrypted}

        except Exception as e:
            return {"error": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_34(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"XXerrorXX": f"handle_message1 failed: {e}"}

    # Step 1 + Step 2
    def xǁRMAPǁhandle_message1__mutmut_35(self, msg1: dict) -> dict:
        try:
            # 解密客户端消息
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # 保存会话
            self.session[identity] = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }

            # 返回加密的 nonceServer
            response_plain = {"nonceServer": nonce_server}
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            return {"payload": encrypted}

        except Exception as e:
            return {"ERROR": f"handle_message1 failed: {e}"}
    
    xǁRMAPǁhandle_message1__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRMAPǁhandle_message1__mutmut_1': xǁRMAPǁhandle_message1__mutmut_1, 
        'xǁRMAPǁhandle_message1__mutmut_2': xǁRMAPǁhandle_message1__mutmut_2, 
        'xǁRMAPǁhandle_message1__mutmut_3': xǁRMAPǁhandle_message1__mutmut_3, 
        'xǁRMAPǁhandle_message1__mutmut_4': xǁRMAPǁhandle_message1__mutmut_4, 
        'xǁRMAPǁhandle_message1__mutmut_5': xǁRMAPǁhandle_message1__mutmut_5, 
        'xǁRMAPǁhandle_message1__mutmut_6': xǁRMAPǁhandle_message1__mutmut_6, 
        'xǁRMAPǁhandle_message1__mutmut_7': xǁRMAPǁhandle_message1__mutmut_7, 
        'xǁRMAPǁhandle_message1__mutmut_8': xǁRMAPǁhandle_message1__mutmut_8, 
        'xǁRMAPǁhandle_message1__mutmut_9': xǁRMAPǁhandle_message1__mutmut_9, 
        'xǁRMAPǁhandle_message1__mutmut_10': xǁRMAPǁhandle_message1__mutmut_10, 
        'xǁRMAPǁhandle_message1__mutmut_11': xǁRMAPǁhandle_message1__mutmut_11, 
        'xǁRMAPǁhandle_message1__mutmut_12': xǁRMAPǁhandle_message1__mutmut_12, 
        'xǁRMAPǁhandle_message1__mutmut_13': xǁRMAPǁhandle_message1__mutmut_13, 
        'xǁRMAPǁhandle_message1__mutmut_14': xǁRMAPǁhandle_message1__mutmut_14, 
        'xǁRMAPǁhandle_message1__mutmut_15': xǁRMAPǁhandle_message1__mutmut_15, 
        'xǁRMAPǁhandle_message1__mutmut_16': xǁRMAPǁhandle_message1__mutmut_16, 
        'xǁRMAPǁhandle_message1__mutmut_17': xǁRMAPǁhandle_message1__mutmut_17, 
        'xǁRMAPǁhandle_message1__mutmut_18': xǁRMAPǁhandle_message1__mutmut_18, 
        'xǁRMAPǁhandle_message1__mutmut_19': xǁRMAPǁhandle_message1__mutmut_19, 
        'xǁRMAPǁhandle_message1__mutmut_20': xǁRMAPǁhandle_message1__mutmut_20, 
        'xǁRMAPǁhandle_message1__mutmut_21': xǁRMAPǁhandle_message1__mutmut_21, 
        'xǁRMAPǁhandle_message1__mutmut_22': xǁRMAPǁhandle_message1__mutmut_22, 
        'xǁRMAPǁhandle_message1__mutmut_23': xǁRMAPǁhandle_message1__mutmut_23, 
        'xǁRMAPǁhandle_message1__mutmut_24': xǁRMAPǁhandle_message1__mutmut_24, 
        'xǁRMAPǁhandle_message1__mutmut_25': xǁRMAPǁhandle_message1__mutmut_25, 
        'xǁRMAPǁhandle_message1__mutmut_26': xǁRMAPǁhandle_message1__mutmut_26, 
        'xǁRMAPǁhandle_message1__mutmut_27': xǁRMAPǁhandle_message1__mutmut_27, 
        'xǁRMAPǁhandle_message1__mutmut_28': xǁRMAPǁhandle_message1__mutmut_28, 
        'xǁRMAPǁhandle_message1__mutmut_29': xǁRMAPǁhandle_message1__mutmut_29, 
        'xǁRMAPǁhandle_message1__mutmut_30': xǁRMAPǁhandle_message1__mutmut_30, 
        'xǁRMAPǁhandle_message1__mutmut_31': xǁRMAPǁhandle_message1__mutmut_31, 
        'xǁRMAPǁhandle_message1__mutmut_32': xǁRMAPǁhandle_message1__mutmut_32, 
        'xǁRMAPǁhandle_message1__mutmut_33': xǁRMAPǁhandle_message1__mutmut_33, 
        'xǁRMAPǁhandle_message1__mutmut_34': xǁRMAPǁhandle_message1__mutmut_34, 
        'xǁRMAPǁhandle_message1__mutmut_35': xǁRMAPǁhandle_message1__mutmut_35
    }
    
    def handle_message1(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRMAPǁhandle_message1__mutmut_orig"), object.__getattribute__(self, "xǁRMAPǁhandle_message1__mutmut_mutants"), args, kwargs, self)
        return result 
    
    handle_message1.__signature__ = _mutmut_signature(xǁRMAPǁhandle_message1__mutmut_orig)
    xǁRMAPǁhandle_message1__mutmut_orig.__name__ = 'xǁRMAPǁhandle_message1'

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_orig(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_1(self, msg2: dict) -> dict:
        try:
            plaintext = None
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_2(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(None)
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_3(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["XXpayloadXX"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_4(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["PAYLOAD"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_5(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = None
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_6(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(None)
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_7(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["XXnonceClientXX"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_8(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceclient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_9(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["NONCECLIENT"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_10(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = None

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_11(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(None)

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_12(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["XXnonceServerXX"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_13(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceserver"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_14(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["NONCESERVER"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_15(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = ""
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_16(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client or sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_17(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["XXnonceClientXX"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_18(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceclient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_19(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["NONCECLIENT"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_20(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] != nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_21(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["XXnonceServerXX"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_22(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceserver"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_23(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["NONCESERVER"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_24(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] != nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_25(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = None
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_26(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    return

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_27(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is not None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_28(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"XXerrorXX": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_29(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"ERROR": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_30(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "XXSession not found or nonce mismatchXX"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_31(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_32(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "SESSION NOT FOUND OR NONCE MISMATCH"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_33(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = None
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_34(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) & nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_35(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client >> 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_36(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 65) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_37(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = None

            return {"result": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_38(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"XXresultXX": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_39(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"RESULT": result_hex}

        except Exception as e:
            return {"error": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_40(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"XXerrorXX": f"handle_message2 failed: {e}"}

    # Step 3 + Step 4
    def xǁRMAPǁhandle_message2__mutmut_41(self, msg2: dict) -> dict:
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            nonce_client = int(plaintext["nonceClient"])
            nonce_server = int(plaintext["nonceServer"])

            matched_identity = None
            for ident, sess in self.session.items():
                if sess["nonceClient"] == nonce_client and sess["nonceServer"] == nonce_server:
                    matched_identity = ident
                    break

            if matched_identity is None:
                return {"error": "Session not found or nonce mismatch"}

            # 拼接生成 128-bit → 32 hex
            combined = (nonce_client << 64) | nonce_server
            result_hex = f"{combined:032x}"

            return {"result": result_hex}

        except Exception as e:
            return {"ERROR": f"handle_message2 failed: {e}"}
    
    xǁRMAPǁhandle_message2__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRMAPǁhandle_message2__mutmut_1': xǁRMAPǁhandle_message2__mutmut_1, 
        'xǁRMAPǁhandle_message2__mutmut_2': xǁRMAPǁhandle_message2__mutmut_2, 
        'xǁRMAPǁhandle_message2__mutmut_3': xǁRMAPǁhandle_message2__mutmut_3, 
        'xǁRMAPǁhandle_message2__mutmut_4': xǁRMAPǁhandle_message2__mutmut_4, 
        'xǁRMAPǁhandle_message2__mutmut_5': xǁRMAPǁhandle_message2__mutmut_5, 
        'xǁRMAPǁhandle_message2__mutmut_6': xǁRMAPǁhandle_message2__mutmut_6, 
        'xǁRMAPǁhandle_message2__mutmut_7': xǁRMAPǁhandle_message2__mutmut_7, 
        'xǁRMAPǁhandle_message2__mutmut_8': xǁRMAPǁhandle_message2__mutmut_8, 
        'xǁRMAPǁhandle_message2__mutmut_9': xǁRMAPǁhandle_message2__mutmut_9, 
        'xǁRMAPǁhandle_message2__mutmut_10': xǁRMAPǁhandle_message2__mutmut_10, 
        'xǁRMAPǁhandle_message2__mutmut_11': xǁRMAPǁhandle_message2__mutmut_11, 
        'xǁRMAPǁhandle_message2__mutmut_12': xǁRMAPǁhandle_message2__mutmut_12, 
        'xǁRMAPǁhandle_message2__mutmut_13': xǁRMAPǁhandle_message2__mutmut_13, 
        'xǁRMAPǁhandle_message2__mutmut_14': xǁRMAPǁhandle_message2__mutmut_14, 
        'xǁRMAPǁhandle_message2__mutmut_15': xǁRMAPǁhandle_message2__mutmut_15, 
        'xǁRMAPǁhandle_message2__mutmut_16': xǁRMAPǁhandle_message2__mutmut_16, 
        'xǁRMAPǁhandle_message2__mutmut_17': xǁRMAPǁhandle_message2__mutmut_17, 
        'xǁRMAPǁhandle_message2__mutmut_18': xǁRMAPǁhandle_message2__mutmut_18, 
        'xǁRMAPǁhandle_message2__mutmut_19': xǁRMAPǁhandle_message2__mutmut_19, 
        'xǁRMAPǁhandle_message2__mutmut_20': xǁRMAPǁhandle_message2__mutmut_20, 
        'xǁRMAPǁhandle_message2__mutmut_21': xǁRMAPǁhandle_message2__mutmut_21, 
        'xǁRMAPǁhandle_message2__mutmut_22': xǁRMAPǁhandle_message2__mutmut_22, 
        'xǁRMAPǁhandle_message2__mutmut_23': xǁRMAPǁhandle_message2__mutmut_23, 
        'xǁRMAPǁhandle_message2__mutmut_24': xǁRMAPǁhandle_message2__mutmut_24, 
        'xǁRMAPǁhandle_message2__mutmut_25': xǁRMAPǁhandle_message2__mutmut_25, 
        'xǁRMAPǁhandle_message2__mutmut_26': xǁRMAPǁhandle_message2__mutmut_26, 
        'xǁRMAPǁhandle_message2__mutmut_27': xǁRMAPǁhandle_message2__mutmut_27, 
        'xǁRMAPǁhandle_message2__mutmut_28': xǁRMAPǁhandle_message2__mutmut_28, 
        'xǁRMAPǁhandle_message2__mutmut_29': xǁRMAPǁhandle_message2__mutmut_29, 
        'xǁRMAPǁhandle_message2__mutmut_30': xǁRMAPǁhandle_message2__mutmut_30, 
        'xǁRMAPǁhandle_message2__mutmut_31': xǁRMAPǁhandle_message2__mutmut_31, 
        'xǁRMAPǁhandle_message2__mutmut_32': xǁRMAPǁhandle_message2__mutmut_32, 
        'xǁRMAPǁhandle_message2__mutmut_33': xǁRMAPǁhandle_message2__mutmut_33, 
        'xǁRMAPǁhandle_message2__mutmut_34': xǁRMAPǁhandle_message2__mutmut_34, 
        'xǁRMAPǁhandle_message2__mutmut_35': xǁRMAPǁhandle_message2__mutmut_35, 
        'xǁRMAPǁhandle_message2__mutmut_36': xǁRMAPǁhandle_message2__mutmut_36, 
        'xǁRMAPǁhandle_message2__mutmut_37': xǁRMAPǁhandle_message2__mutmut_37, 
        'xǁRMAPǁhandle_message2__mutmut_38': xǁRMAPǁhandle_message2__mutmut_38, 
        'xǁRMAPǁhandle_message2__mutmut_39': xǁRMAPǁhandle_message2__mutmut_39, 
        'xǁRMAPǁhandle_message2__mutmut_40': xǁRMAPǁhandle_message2__mutmut_40, 
        'xǁRMAPǁhandle_message2__mutmut_41': xǁRMAPǁhandle_message2__mutmut_41
    }
    
    def handle_message2(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRMAPǁhandle_message2__mutmut_orig"), object.__getattribute__(self, "xǁRMAPǁhandle_message2__mutmut_mutants"), args, kwargs, self)
        return result 
    
    handle_message2.__signature__ = _mutmut_signature(xǁRMAPǁhandle_message2__mutmut_orig)
    xǁRMAPǁhandle_message2__mutmut_orig.__name__ = 'xǁRMAPǁhandle_message2'
