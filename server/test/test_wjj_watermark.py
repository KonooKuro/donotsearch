
# -*- coding: utf-8 -*-
import base64
import json
import types
import pytest

from wjj_watermark import WJJWatermarkMethod

# A small but valid-looking PDF (has header and EOF; len > 50)
PDF_OK = (
    b"%PDF-1.4\n"
    b"1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    b"trailer\n"
    b"%%EOF\n"
)
# A shorter valid-looking PDF (<50 bytes) used for applicability=False
PDF_SHORT = b"%PDF-1.4\n%%EOF\n"
# Not a PDF at all
NOT_PDF = b"hello world"


def _insert_raw_payload(pdf: bytes, payload_bytes: bytes) -> bytes:
    """Insert raw base64-encoded payload wrapped with class markers just before %%EOF."""
    wm = WJJWatermarkMethod()
    b64 = base64.b64encode(payload_bytes)
    start, end = wm._START, wm._END
    pos = pdf.rfind(b"%%EOF")
    if pos == -1:
        return pdf + start + b64 + end + b"\n%%EOF\n"
    return pdf[:pos] + start + b64 + end + pdf[pos:]


def test_get_usage_contains_keywords():
    assert "deterministic" in WJJWatermarkMethod.get_usage().lower()
    assert "json" in WJJWatermarkMethod.get_usage().lower()


@pytest.mark.parametrize("secret", ["abc", "topsecret", json.dumps({"secret": "s1", "intended_for": "x@y"})])
def test_add_and_read_roundtrip(secret):
    wm = WJJWatermarkMethod()
    out = wm.add_watermark(PDF_OK, secret=secret, position="eof", key="ignored")
    assert out.startswith(b"%PDF-")
    # ensure markers inserted before EOF
    eof_pos = out.rfind(b"%%EOF")
    assert eof_pos != -1
    assert out.rfind(wm._END) < eof_pos

    # read back
    read = wm.read_secret(out, key="ignored")
    # when input was a dict-JSON, it should extract "secret" value; otherwise return the original string
    if isinstance(secret, str):
        if secret.startswith("{"):  # dict-json case
            assert read == json.loads(secret)["secret"]
        else:
            assert read == secret


def test_add_twice_reads_last_value():
    wm = WJJWatermarkMethod()
    pdf1 = wm.add_watermark(PDF_OK, secret="first")
    pdf2 = wm.add_watermark(pdf1, secret="second")
    # Should read the last (rfind) watermark
    assert wm.read_secret(pdf2) == "second"


def test_add_watermark_invalid_secret_and_pdf():
    wm = WJJWatermarkMethod()
    with pytest.raises(Exception):
        wm.add_watermark(PDF_OK, secret="")  # empty string not allowed
    with pytest.raises(Exception):
        wm.add_watermark(NOT_PDF, secret="x")  # not a pdf


def test_is_watermark_applicable_true_and_false(monkeypatch):
    wm = WJJWatermarkMethod()
    # true for decent PDF
    assert wm.is_watermark_applicable(PDF_OK) is True
    # false for too-short PDF
    assert wm.is_watermark_applicable(PDF_SHORT) is False
    # false if load_pdf_bytes raises
    import wjj_watermark as mod
    orig = mod.load_pdf_bytes
    monkeypatch.setattr(mod, "load_pdf_bytes", lambda _x: (_ for _ in ()).throw(ValueError("boom")))
    try:
        assert wm.is_watermark_applicable(PDF_OK) is False
    finally:
        # restore
        monkeypatch.setattr(mod, "load_pdf_bytes", orig)


def test_read_secret_error_flows():
    wm = WJJWatermarkMethod()
    # 1) no markers
    with pytest.raises(Exception):
        wm.read_secret(PDF_OK)

    # 2) start but no end
    pdf_no_end = PDF_OK.replace(b"%%EOF", wm._START + b"AAAA" + b"%%EOF")
    with pytest.raises(Exception):
        wm.read_secret(pdf_no_end)

    # 3) invalid base64 inside markers
    bad_b64_pdf = _insert_raw_payload(PDF_OK, b"!!!")  # invalid base64
    with pytest.raises(Exception) as ei:
        wm.read_secret(bad_b64_pdf)
    assert "base64" in str(ei.value).lower()

    # 4) base64 ok, but invalid utf-8
    payload = b"\xff\xfe"  # not valid utf-8
    bad_utf8_pdf = _insert_raw_payload(PDF_OK, payload)
    with pytest.raises(Exception) as ei2:
        wm.read_secret(bad_utf8_pdf)
    assert "utf-8" in str(ei2.value).lower()

    # 5) base64 ok, valid utf-8, but JSON not a dict -> return the stringified JSON
    payload_json_not_dict = json.dumps(["x", 1, True]).encode("utf-8")
    pdf_json_list = _insert_raw_payload(PDF_OK, payload_json_not_dict)
    got = wm.read_secret(pdf_json_list)
    # Should return the payload string (not parsed list)
    assert got == json.dumps(["x", 1, True])
