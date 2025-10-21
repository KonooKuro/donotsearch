
# -*- coding: utf-8 -*-
import base64
import io
import json
import types
import pytest

import sys, pathlib
BASE = pathlib.Path(__file__).resolve().parents[1]
SRC = BASE / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
try:
    import wm_embedfile_v1 as mod
    from wm_embedfile_v1 import EmbedFileV1, MAGIC
except ModuleNotFoundError:
    import watermark_JunyiShen.wm_embedfile_v1 as mod
    from watermark_JunyiShen.wm_embedfile_v1 import EmbedFileV1, MAGIC


PDF_MIN = (
    b"%PDF-1.4\n"
    b"1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    b"trailer\n"
    b"%%EOF\n"
)
NOT_PDF = b"hello world"


# -------- helpers for fakes --------
class FakeReaderForWrite:
    """Minimal PdfReader for add_watermark: just expose pages iterable."""
    def __init__(self, stream, strict=False):
        self.pages = []

class FakeWriter:
    def __init__(self):
        self.attach_name = None
        self.attach_content = None
        self.pages = []

    def add_page(self, p):
        self.pages.append(p)

    def add_attachment(self, filename, content):
        self.attach_name = filename
        self.attach_content = content

    def write(self, out_io):
        # Write a valid-looking PDF that contains the framed payload so raw fallback can find it.
        if not isinstance(out_io, io.BytesIO):
            raise TypeError("expected BytesIO")
        body = b"%PDF-1.4\n" + (self.attach_content or b"") + b"\n%%EOF"
        out_io.write(body)


# ---- structural readers for read_secret ----
class FakeReaderWithAttachments:
    """Expose .attachments mapping as in some PyPDF2 versions."""
    def __init__(self, stream, strict=False):
        self.attachments = {}  # name -> data
        # We'll let tests inject content afterwards by monkeypatching attribute


class _FakeStream:
    def __init__(self, data: bytes):
        self._data = data
    def get_data(self):
        return self._data

class _FakeFS(dict):
    """FileSpec-like dictionary node with /EF -> /F stream"""
    def __init__(self, data: bytes, name="af_item"):
        super().__init__({"/EF": {"/F": _FakeStream(data)}, "/F": name})
    def get_object(self):
        return self

class FakeReaderWithNamesTree:
    """Expose trailer /Root/Names/EmbeddedFiles/Names array format"""
    def __init__(self, stream, strict=False):
        payload = stream.getvalue() if hasattr(stream, "getvalue") else (stream.read() if hasattr(stream, "read") else bytes(stream))
        # we don't actually parse payload; tests will set framed bytes below
        self.trailer = {
            "/Root": {
                "/Names": {
                    "/EmbeddedFiles": {
                        "/Names": []  # [name, FileSpec, name, FileSpec, ...]
                    }
                }
            }
        }

class FakeReaderWithAF:
    """Expose /Root/AF array of FileSpec objects"""
    def __init__(self, stream, strict=False):
        self.trailer = {"/Root": {"/AF": []}}


def _frame_bytes(secret: str) -> bytes:
    # Build a framed payload compatible with _try_parse_frame (no HMAC required)
    obj = {"v":1,"algo":"embedfile-v1","doc_sha256":"d"*64,"secret":secret,"ts":0}
    body = json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    b64 = base64.urlsafe_b64encode(body).decode("ascii").rstrip("=")
    content = (MAGIC + b64 + "|").encode("utf-8")
    return content


# ---------------- tests ----------------
def test_is_watermark_applicable_true_false(monkeypatch):
    wm = EmbedFileV1()
    assert wm.is_watermark_applicable(PDF_MIN) is True
    assert wm.is_watermark_applicable(NOT_PDF) is False

    # When load_pdf_bytes raises -> False
    orig = mod.load_pdf_bytes
    monkeypatch.setattr(mod, "load_pdf_bytes", lambda _x: (_ for _ in ()).throw(ValueError("boom")))
    try:
        assert wm.is_watermark_applicable(PDF_MIN) is False
    finally:
        monkeypatch.setattr(mod, "load_pdf_bytes", orig)


def test_add_and_read_roundtrip_raw_fallback(monkeypatch):
    wm = EmbedFileV1()

    # Ensure PyPDF2 classes exist for add_watermark, but use our fakes
    monkeypatch.setattr(mod, "PdfReader", FakeReaderForWrite)
    monkeypatch.setattr(mod, "PdfWriter", FakeWriter)

    out = wm.add_watermark(PDF_MIN, secret="s3cret")
    assert out.startswith(b"%PDF-")

    # For read_secret, disable structural path to exercise raw fallback
    monkeypatch.setattr(mod, "PdfReader", None)
    got = wm.read_secret(out)
    assert got == "s3cret"


def test_add_watermark_errors(monkeypatch):
    wm = EmbedFileV1()

    # PyPDF2 missing
    monkeypatch.setattr(mod, "PdfReader", None)
    monkeypatch.setattr(mod, "PdfWriter", None)
    with pytest.raises(Exception):
        wm.add_watermark(PDF_MIN, secret="x")

    # Invalid secret
    monkeypatch.setattr(mod, "PdfReader", FakeReaderForWrite)
    monkeypatch.setattr(mod, "PdfWriter", FakeWriter)
    with pytest.raises(Exception):
        wm.add_watermark(PDF_MIN, secret="")  # empty

    # Writer.write fails -> wrapped as error
    class BadWriter(FakeWriter):
        def write(self, out_io):
            raise RuntimeError("write failed")
    monkeypatch.setattr(mod, "PdfWriter", BadWriter)
    with pytest.raises(Exception):
        wm.add_watermark(PDF_MIN, secret="ok")


def test_read_secret_structural_via_attachments(monkeypatch):
    wm = EmbedFileV1()
    monkeypatch.setattr(mod, "PdfReader", FakeReaderWithAttachments)

    pdf = io.BytesIO(PDF_MIN)
    # Feed a framed attachment
    reader = mod.PdfReader(pdf, strict=False)
    reader.attachments["x.dat"] = _frame_bytes("via-attach")

    # Monkeypatch PdfReader to return our prepared instance regardless of input
    def _make_reader(_s, strict=False):
        return reader
    monkeypatch.setattr(mod, "PdfReader", _make_reader)

    got = wm.read_secret(PDF_MIN)
    assert got == "via-attach"


def test_read_secret_structural_via_names_tree(monkeypatch):
    wm = EmbedFileV1()
    monkeypatch.setattr(mod, "PdfReader", FakeReaderWithNamesTree)

    # Prepare reader instance with names array containing a FileSpec-like object
    r = mod.PdfReader(io.BytesIO(PDF_MIN), strict=False)
    fs = _FakeFS(_frame_bytes("via-names"), name="nm")
    r.trailer["/Root"]["/Names"]["/EmbeddedFiles"]["/Names"] = ["nm", fs]

    def _make_reader(_s, strict=False):
        return r
    monkeypatch.setattr(mod, "PdfReader", _make_reader)

    got = wm.read_secret(PDF_MIN)
    assert got == "via-names"


def test_read_secret_structural_via_AF(monkeypatch):
    wm = EmbedFileV1()
    monkeypatch.setattr(mod, "PdfReader", FakeReaderWithAF)

    r = mod.PdfReader(io.BytesIO(PDF_MIN), strict=False)
    r.trailer["/Root"]["/AF"] = [_FakeFS(_frame_bytes("via-af"), name="af_item")]

    def _make_reader(_s, strict=False):
        return r
    monkeypatch.setattr(mod, "PdfReader", _make_reader)

    got = wm.read_secret(PDF_MIN)
    assert got == "via-af"


def test__try_parse_frame_variants():
    # no magic -> None
    assert EmbedFileV1._try_parse_frame(b"abc") is None

    # invalid base64 after MAGIC -> None
    assert EmbedFileV1._try_parse_frame(MAGIC.encode("utf-8") + b"!!!|") is None

    # valid frame -> secret
    content = _frame_bytes("ok")
    assert EmbedFileV1._try_parse_frame(content) == "ok"

    # extra trailing bytes in decoded JSON -> it trims at last '}' safely
    obj = {"v":1,"algo":"embedfile-v1","doc_sha256":"x","secret":"trim","ts":1}
    body = json.dumps(obj).encode("utf-8") + b"garbage"
    b64 = base64.urlsafe_b64encode(body).decode("ascii").rstrip("=")
    blob = (MAGIC + b64 + "|").encode("utf-8")
    assert EmbedFileV1._try_parse_frame(blob) == "trim"


def test_read_secret_no_match_raises(monkeypatch):
    wm = EmbedFileV1()
    # Force structural path to miss and then raw fallback to scan but find nothing
    class NoAttachReader:
        def __init__(self, *a, **kw):
            self.attachments = {}
            self.trailer = {"/Root": {}}
    monkeypatch.setattr(mod, "PdfReader", NoAttachReader)

    with pytest.raises(Exception):
        wm.read_secret(PDF_MIN)  # no frames anywhere
