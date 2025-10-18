# -*- coding: utf-8 -*-
"""
wm_embedfile_v1.py
Robust & simple PDF watermark: embed a small JSON payload as an embedded file
(/Names -> /EmbeddedFiles). Read structurally (PyPDF2), fallback to raw frame scan.
"""
from __future__ import annotations
from typing import Optional, Union, Dict
import io, json, base64, hashlib, hmac, time

# Compatibility with course framework; provide fallbacks if not present.
try:
    from watermarking_method import (
        PdfSource, WatermarkingError, SecretNotFoundError, load_pdf_bytes, WatermarkingMethod
    )
except Exception:
    PdfSource = Union[bytes, bytearray, io.BufferedIOBase]
    class WatermarkingError(Exception): ...
    class SecretNotFoundError(WatermarkingError): ...
    def load_pdf_bytes(pdf: PdfSource) -> bytes:
        if isinstance(pdf, (bytes, bytearray)): return bytes(pdf)
        if hasattr(pdf, "read"): return pdf.read()
        raise TypeError("Unsupported PdfSource")
    class WatermarkingMethod(object): ...

try:
    from PyPDF2 import PdfReader, PdfWriter
except Exception:
    PdfReader = PdfWriter = None  # handled at runtime

METHOD_NAME = "embedfile-v1"
MAGIC = "WM3|"  # frame prefix inside attachment content

def _hmac_hex(key: Optional[str], data: bytes) -> str:
    return "" if not key else hmac.new(key.encode("utf-8"), data, hashlib.sha256).hexdigest()

class EmbedFileV1(WatermarkingMethod):
    name = METHOD_NAME

    @staticmethod
    def get_usage() -> str:
        return ("Embed JSON payload as an embedded file under /EmbeddedFiles. "
                "Args: secret(str), key(optional HMAC). Readout does not require key.")

    def is_watermark_applicable(self, pdf: PdfSource, position: Optional[str]=None) -> bool:
        try: return load_pdf_bytes(pdf).startswith(b"%PDF-")
        except Exception: return False

    # ---------------- write ----------------
    def add_watermark(self, pdf: PdfSource, secret: str,
                      position: Optional[str]=None, key: Optional[str]=None) -> bytes:
        if PdfReader is None or PdfWriter is None:
            raise WatermarkingError("PyPDF2 is required (add PyPDF2>=3.0.0).")
        if not isinstance(secret, str) or not secret:
            raise WatermarkingError("Secret must be a non-empty string.")

        original = load_pdf_bytes(pdf)
        doc_sha = hashlib.sha256(original).hexdigest()
        payload = {"v":1, "algo": self.name, "doc_sha256": doc_sha, "secret": secret, "ts": int(time.time())}
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        mac  = _hmac_hex(key, body)
        framed = (MAGIC + base64.urlsafe_b64encode(body).decode("ascii").rstrip("=") + "|" + mac).encode("utf-8")

        short = mac[:8] if mac else hashlib.sha1(body).hexdigest()[:8]
        filename = f"wm_{short}_{doc_sha[:10]}.dat"

        try:
            reader = PdfReader(io.BytesIO(original), strict=False)
            writer = PdfWriter()
            for p in reader.pages: writer.add_page(p)
            writer.add_attachment(filename, framed)  # creates /Names /EmbeddedFiles if missing
            out = io.BytesIO(); writer.write(out); return out.getvalue()
        except Exception as e:
            raise WatermarkingError(f"Failed to write watermark: {e}") from e

    # ---------------- read ----------------
    def read_secret(self, pdf: PdfSource) -> str:
        data = load_pdf_bytes(pdf)

        # Prefer structural read via PyPDF2 (EmbeddedFiles + Catalog /AF)
        try:
            if PdfReader is None: raise RuntimeError("PyPDF2 missing")
            reader = PdfReader(io.BytesIO(data), strict=False)
            attachments: Dict[str, bytes] = {}

            # PyPDF2 3.x: reader.attachments (if available)
            try:
                if hasattr(reader, "attachments") and reader.attachments:
                    attachments.update(reader.attachments)
            except Exception:
                pass

            # Names tree fallback
            try:
                root = reader.trailer.get("/Root", {})
                names = root.get("/Names", {})
                ef_tree = names.get("/EmbeddedFiles", {})
                if "/Names" in ef_tree:
                    arr = ef_tree["/Names"]
                    for i in range(0, len(arr), 2):
                        nm = str(arr[i])
                        fs = arr[i+1]
                        fs_obj = fs.get_object() if hasattr(fs,"get_object") else fs
                        ef = fs_obj.get("/EF", {})
                        fstream = ef.get("/F")
                        if fstream:
                            attachments[nm] = fstream.get_data()
            except Exception:
                pass

            # Catalog /AF (Associated Files)
            try:
                root = reader.trailer.get("/Root", {})
                AF = root.get("/AF")
                if AF is not None:
                    arr = AF.get_object() if hasattr(AF,"get_object") else AF
                    items = arr if isinstance(arr, list) else [arr]
                    for fs in items:
                        try:
                            fs_obj = fs.get_object() if hasattr(fs,"get_object") else fs
                            ef = fs_obj.get("/EF", {})
                            fstream = ef.get("/F")
                            if fstream:
                                attachments[str(fs_obj.get("/F","af_item"))] = fstream.get_data()
                        except Exception:
                            continue
            except Exception:
                pass

            for _, content in attachments.items():
                if isinstance(content,(bytes,bytearray)) and content:
                    s = self._try_parse_frame(bytes(content))
                    if s is not None: return s
        except Exception:
            pass

        # Raw fallback: search for frame in bytes
        mark = MAGIC.encode("utf-8"); pos = data.find(mark)
        while pos != -1:
            frag = data[pos:pos+4096]
            s = self._try_parse_frame(frag)
            if s is not None: return s
            pos = data.find(mark, pos+1)

        raise SecretNotFoundError("No watermark found (embedfile-v1).")

    @staticmethod
    def _try_parse_frame(blob: bytes) -> Optional[str]:
        try:
            mark = MAGIC.encode("utf-8")
            i = blob.find(mark)
            if i == -1: return None
            after = blob[i+len(mark):]
            b64, sep, _mac = after.partition(b"|")
            if not sep: return None
            pad = b"=" * ((4 - len(b64) % 4) % 4)
            body = base64.urlsafe_b64decode(b64 + pad)
            end = body.rfind(b"}")
            if end != -1: body = body[:end+1]
            obj = json.loads(body.decode("utf-8"))
            if isinstance(obj, dict) and "secret" in obj: return str(obj["secret"])
        except Exception:
            return None
        return None

METHOD_INSTANCE = EmbedFileV1()
