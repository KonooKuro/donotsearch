from __future__ import annotations

import base64
import json

from watermarking_method import (
    WatermarkingMethod,
    load_pdf_bytes,
    is_pdf_bytes,
    SecretNotFoundError,
    WatermarkingError,
)


class WJJWatermarkMethod(WatermarkingMethod):
    """Simple, deterministic inline watermark. Ignores 'key' and 'position'."""

    # 稳定注册名
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
        pdf,
        secret: str,
        key: str,
        position: str | None = None,
    ) -> bytes:
        # 读取 PDF 字节
        data = load_pdf_bytes(pdf)

        # secret 可能已是 JSON；否则包一层
        try:
            parsed = json.loads(secret)
            payload = parsed if isinstance(parsed, dict) else {"secret": secret, "intended_for": None}
        except Exception:
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

        return new_data

    def is_watermark_applicable(self, pdf, position: str | None = None) -> bool:
        try:
            data = load_pdf_bytes(pdf)
            return is_pdf_bytes(data)
        except Exception:
            return False

    def read_secret(self, pdf, key: str) -> str:
        """Find marker and return the JSON string payload."""
        data = load_pdf_bytes(pdf)

        start_idx = data.rfind(self._START)
        if start_idx == -1:
            raise SecretNotFoundError("WJJ watermark start marker not found")

        end_idx = data.find(self._END, start_idx + len(self._START))
        if end_idx == -1:
            raise SecretNotFoundError("WJJ watermark end marker not found")

        b64 = data[start_idx + len(self._START) : end_idx]
        try:
            payload_bytes = base64.b64decode(b64, validate=True)
        except Exception as e:
            raise WatermarkingError(f"Failed to base64-decode WJJ watermark payload: {e}")

        try:
            payload_str = payload_bytes.decode("utf-8")
        except Exception as e:
            raise WatermarkingError(f"Failed to decode WJJ payload utf-8: {e}")

        # 尝试验证 JSON，但即便失败也直接返回字符串
        try:
            json.loads(payload_str)
        except Exception:
            pass

        return payload_str
