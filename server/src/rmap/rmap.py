# -*- coding: utf-8 -*-
"""
rmap.py
-------
RMAP 四步握手核心逻辑（仅做“解/封装”与加解密，不持久化会话）
"""

import secrets


class RMAP:
    def __init__(self, identity_manager):
        self.im = identity_manager

    # Step 1 + Step 2
    def handle_message1(self, msg1: dict) -> dict:
        """
        输入:
          msg1 = {"payload": "<base64(ASCII-armored PGP)>"}
        明文应解出:
          {"nonceClient": <u64>, "identity": "<GroupName>"}

        返回:
          {
            "payload": "<base64(...)>",             # 发给客户端的 Response1（加密）
            "identity": "<GroupName>",              # 给路由层保存会话
            "nonceClient": <int>,                   # 给路由层保存会话
            "nonceServer": <int>                    # 给路由层保存会话
          }
        """
        try:
            # 解密客户端消息（由服务器私钥解开）
            plaintext = self.im.decrypt_for_server(msg1["payload"])
            nonce_client = int(plaintext["nonceClient"])
            identity = plaintext["identity"]

            # 生成服务器随机数
            nonce_server = secrets.randbits(64)

            # ⭐ 按协议，响应需要“回显” nonceClient，并附带 nonceServer
            response_plain = {
                "nonceClient": nonce_client,
                "nonceServer": nonce_server,
            }
            # 加密给“该 identity 的公钥”
            encrypted = self.im.encrypt_for_client(identity, response_plain)

            # ⭐ 关键：把三元组带回给路由层保存会话（不是发给客户端）
            return {
                "payload": encrypted,
                "identity": identity,              # 给路由层保存会话
                "nonceClient": nonce_client,                   # 给路由层保存会话
                "nonceServer": nonce_server 
            }

        except Exception as e:
            # 让上层直接返回错误信息
            raise RuntimeError(f"handle_message1 failed: {e}") from e

    # Step 3 + Step 4
    def handle_message2(self, msg2: dict) -> dict:
        """
        输入:
          msg2 = {"payload": "<base64(ASCII-armored PGP)>"}
        明文应解出（作业表3）:
          {"nonceServer": <u64>}

        返回:
          {"nonceServer": <int>}   # 交由路由层用会话表比对 Nc/Ns 并生成 sid/link
        """
        try:
            plaintext = self.im.decrypt_for_server(msg2["payload"])
            # ⭐ 作业要求第二条消息只带 nonceServer
            nonce_server = int(plaintext["nonceServer"])
            return {"nonceServer": nonce_server}

        except Exception as e:
            raise RuntimeError(f"handle_message2 failed: {e}") from e
