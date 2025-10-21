from __future__ import annotations
from watermarking_method import WatermarkingError


import base64
import json
from typing import Optional

from watermarking_method import (
    WatermarkingMethod,
    PdfSource,
    load_pdf_bytes,
    is_pdf_bytes,
    SecretNotFoundError,
    WatermarkingError,
)


class WJJWatermarkMethod(WatermarkingMethod):
    """Simple, deterministic inline watermark."""

    name = "wjj-watermark"

    @staticmethod
    def get_usage() -> str:
        return (
            "Simple deterministic inline watermark. "
            "Server packs {secret,intended_for} into JSON and embeds it. "
            "This method ignores 'key' and 'position'."
        )

    # 明确的开始/结束标记
    _START = b"\n%WJJ-WATERMARK-START\n"
    _END = b"\n%WJJ-WATERMARK-END\n"

    def add_watermark(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None,
        key: Optional[str] = None,  # 添加 key 参数以兼容测试框架
    ) -> bytes:
        """添加水印到PDF"""
        # 验证输入
        if not isinstance(secret, str) or not secret:
            raise WatermarkingError("Secret must be a non-empty string")
        
        # 读取 PDF 字节
        try:
            data = load_pdf_bytes(pdf)
        except (ValueError, TypeError) as e:
            raise WatermarkingError("Invalid PDF input") from e
        
        # 确保是有效的PDF
        if not is_pdf_bytes(data):
            raise WatermarkingError("Input is not a valid PDF")

        # secret 可能已是 JSON；否则包一层
        try:
            parsed = json.loads(secret)
            payload = parsed if isinstance(parsed, dict) else {"secret": secret, "intended_for": None}
        except (json.JSONDecodeError, ValueError):
            payload = {"secret": secret, "intended_for": None}

        # JSON → Base64
        payload_bytes = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        b64 = base64.b64encode(payload_bytes)
        marker = self._START + b64 + self._END

        # 插入到最后一个 %%EOF 前；没有就附加并补一个 EOF
        eof_pos = data.rfind(b"%%EOF")
        if eof_pos != -1:
            new_data = data[:eof_pos] + marker + data[eof_pos:]
        else:
            new_data = data + marker + b"\n%%EOF\n"

        # 确保输出仍然是有效的PDF
        if not new_data.startswith(b"%PDF-"):
            raise WatermarkingError("Output is not a valid PDF")
            
        return new_data

    def is_watermark_applicable(
        self, 
        pdf: PdfSource, 
        position: Optional[str] = None
    ) -> bool:
        """检查水印方法是否适用于给定PDF"""
        try:
            data = load_pdf_bytes(pdf)
            # 基本的PDF验证
            if not is_pdf_bytes(data):
                return False
            # 确保PDF有最小长度
            if len(data) < 50:
                return False
            return True
        except Exception:
            return False

    def read_secret(
        self, 
        pdf: PdfSource, 
        key: Optional[str] = None  # 添加 key 参数以兼容测试框架
    ) -> str:
        """从PDF中提取水印
        
        返回值说明：
        - 如果水印是 JSON 格式且包含 'secret' 字段，返回该字段的值
        - 否则返回完整的水印内容（可能是 JSON 字符串或普通字符串）
        """
        data = load_pdf_bytes(pdf)

        # 查找最后一个水印标记（支持多次水印）
        start_idx = data.rfind(self._START)
        if start_idx == -1:
            raise SecretNotFoundError("WJJ watermark start marker not found")

        end_idx = data.find(self._END, start_idx + len(self._START))
        if end_idx == -1:
            raise SecretNotFoundError("WJJ watermark end marker not found")

        b64 = data[start_idx + len(self._START) : end_idx]
        
        # 解码 Base64
        try:
            payload_bytes = base64.b64decode(b64, validate=True)
        except Exception as e:
            raise WatermarkingError(f"Failed to base64-decode WJJ watermark payload: {e}")

        # 解码 UTF-8
        try:
            payload_str = payload_bytes.decode("utf-8")
        except Exception as e:
            raise WatermarkingError(f"Failed to decode WJJ payload utf-8: {e}")

        # 尝试解析 JSON 并提取 secret 字段
        try:
            payload = json.loads(payload_str)
            # 如果是字典且包含 secret 字段，返回该字段
            if isinstance(payload, dict) and "secret" in payload:
                return payload["secret"]
            # 如果是其他 JSON 类型，返回字符串形式
            return payload_str
        except (json.JSONDecodeError, ValueError):
            # 如果不是有效的JSON，返回原始字符串
            return payload_str
