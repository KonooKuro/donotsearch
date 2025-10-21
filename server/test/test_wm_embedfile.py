import io, json, base64, time, hashlib, hmac, types
import pytest

from src.watermark_JunyiShen import wm_embedfile_v1 as wm

EmbedFileV1 = wm.EmbedFileV1
WatermarkingError = wm.WatermarkingError
SecretNotFoundError = wm.SecretNotFoundError


def make_frame(payload: dict, mac: str = "abcd"):
    b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    return (wm.MAGIC + b64 + "|" + mac).encode()


# ----------------- 基础函数覆盖 -----------------

def test_hmac_hex_both_paths():
    data = b"abc"
    assert wm._hmac_hex(None, data) == ""  # 无 key
    assert wm._hmac_hex("key", data) == hmac.new(b"key", data, hashlib.sha256).hexdigest()


def test_is_watermark_applicable_and_exception(monkeypatch):
    e = EmbedFileV1()
    assert e.is_watermark_applicable(b"%PDF-1.4 something")
    assert not e.is_watermark_applicable(b"not a pdf")

    # load_pdf_bytes 抛异常 -> False 分支
    def bad_loader(_):
        raise RuntimeError("boom")
    monkeypatch.setattr(wm, "load_pdf_bytes", bad_loader)
    assert e.is_watermark_applicable(b"%PDF-1.4") is False


# ----------------- add_watermark 覆盖 -----------------

def test_add_watermark_with_key_and_capture_attachment(monkeypatch):
    """
    覆盖：PyPDF2 正常路径 + 有 key（HMAC）+ 捕获 writer.add_attachment 的内容
    """
    e = EmbedFileV1()

    class DummyReader:
        def __init__(self, *a, **kw):
            self.pages = [object(), object()]

    captured = {}
    class DummyWriter:
        def __init__(self): self.pages=[]
        def add_page(self, p): self.pages.append(p)
        def add_attachment(self, name, data):
            captured["name"] = name
            captured["data"] = data
        def write(self, out): out.write(b"%PDF-1.4 with attach")

    monkeypatch.setattr(wm, "PdfReader", DummyReader)
    monkeypatch.setattr(wm, "PdfWriter", DummyWriter)

    pdf = b"%PDF-1.4 test content"
    out = e.add_watermark(pdf, secret="HELLO", key="k123")
    assert out.startswith(b"%PDF")
    # 附件内容应包含 MAGIC 帧
    assert captured["name"].startswith("wm_")
    assert isinstance(captured["data"], (bytes, bytearray))
    assert wm.MAGIC.encode() in captured["data"]


def test_add_watermark_without_key_uses_sha1(monkeypatch):
    """
    覆盖：无 key 情况，文件名 short 落到 sha1 路径
    """
    e = EmbedFileV1()

    class DummyReader:
        def __init__(self, *a, **kw): self.pages=[1]
    class DummyWriter:
        def __init__(self): self.pages=[]
        def add_page(self, p): self.pages.append(p)
        def add_attachment(self, name, data):
            # short = sha1(body)[:8]，无法直接预测，但至少应以 wm_ 开头
            assert name.startswith("wm_") and name.endswith(".dat")
            assert isinstance(data, (bytes, bytearray))
        def write(self, out): out.write(b"%PDF-1.4 ok")

    monkeypatch.setattr(wm, "PdfReader", DummyReader)
    monkeypatch.setattr(wm, "PdfWriter", DummyWriter)
    out = e.add_watermark(b"%PDF-1.4 data", secret="ABC")
    assert out.startswith(b"%PDF")


def test_add_watermark_no_pypdf2(monkeypatch):
    e = EmbedFileV1()
    monkeypatch.setattr(wm, "PdfReader", None)
    monkeypatch.setattr(wm, "PdfWriter", None)
    with pytest.raises(WatermarkingError):
        e.add_watermark(b"%PDF-1.4", secret="X")


def test_add_watermark_invalid_secret(monkeypatch):
    e = EmbedFileV1()
    monkeypatch.setattr(wm, "PdfReader", object)
    monkeypatch.setattr(wm, "PdfWriter", object)
    with pytest.raises(WatermarkingError):
        e.add_watermark(b"%PDF-1.4", secret="")


def test_add_watermark_runtime_fail(monkeypatch):
    e = EmbedFileV1()
    class BadReader:
        def __init__(self,*a,**kw): raise RuntimeError("bad read")
    monkeypatch.setattr(wm, "PdfReader", BadReader)
    monkeypatch.setattr(wm, "PdfWriter", object)
    with pytest.raises(WatermarkingError):
        e.add_watermark(b"%PDF-1.4", secret="s")


# ----------------- _try_parse_frame 覆盖 -----------------

def test_try_parse_frame_valid_and_invalid_variants():
    e = EmbedFileV1()
    # 正常
    frame = make_frame({"secret":"wow"})
    assert e._try_parse_frame(frame) == "wow"
    # 无分隔符 |
    assert e._try_parse_frame(wm.MAGIC.encode() + b"abcd") is None
    # base64 非法
    bad = (wm.MAGIC + "!!!" + "|" + "xx").encode()
    assert e._try_parse_frame(bad) is None
    # 体内含多余内容，触发 "按最后一个 } 截断"
    raw = json.dumps({"secret":"CUT"}) + "\x00\x00garbage"
    b64 = base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")
    cut = (wm.MAGIC + b64 + "|mac").encode()
    assert e._try_parse_frame(cut) == "CUT"


# ----------------- read_secret 结构化读取三路径 + 回退 -----------------

def test_read_secret_via_attachments_property(monkeypatch):
    e = EmbedFileV1()
    # 模拟 PyPDF2.Reader，使用 attachments 属性
    class DummyReader:
        def __init__(self, *a, **kw):
            payload = {"secret": "ATTACH"}
            b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
            self.attachments = {"wm.bin": (wm.MAGIC + b64 + "|h").encode()}
            self.trailer = {}  # 不走 Names/AF
    monkeypatch.setattr(wm, "PdfReader", DummyReader)
    pdf_bytes = b"%PDF-1.4 dummy"
    assert e.read_secret(pdf_bytes) == "ATTACH"


def _mk_obj(mapping):
    """
    构造一个既像 dict 又像 PyPDF2 的轻量对象：
    - 支持 get()
    - 支持 get_object() 返回 self（模仿间接对象）
    """
    class Obj(dict):
        def get_object(self): return self
    return Obj(mapping)


def test_read_secret_via_names_tree(monkeypatch):
    e = EmbedFileV1()
    # Names 树：/Root -> /Names -> /EmbeddedFiles -> /Names [name, FileSpec, ...]
    content = make_frame({"secret":"NAMES"})
    file_stream = _mk_obj({"/F": types.SimpleNamespace(get_data=lambda: content)})
    file_spec = _mk_obj({"/EF": file_stream})
    names_arr = ["wm1", file_spec]  # 只放一个
    embedded_files = _mk_obj({"/Names": names_arr})
    names_root = _mk_obj({"/EmbeddedFiles": embedded_files})
    root = _mk_obj({"/Names": names_root})

    class DummyReader:
        def __init__(self,*a,**kw):
            self.attachments = {}  # 不走 attachments
            self.trailer = {"/Root": root}

    monkeypatch.setattr(wm, "PdfReader", DummyReader)
    assert e.read_secret(b"%PDF-1.4 X") == "NAMES"


def test_read_secret_via_catalog_AF(monkeypatch):
    e = EmbedFileV1()
    content = make_frame({"secret":"AF"})
    file_stream = _mk_obj({"/F": types.SimpleNamespace(get_data=lambda: content)})
    file_spec = _mk_obj({"/EF": file_stream, "/F": "af_item"})
    AF_array = [file_spec]
    root = _mk_obj({"/AF": AF_array})

    class DummyReader:
        def __init__(self,*a,**kw):
            self.attachments = {}
            self.trailer = {"/Root": root}

    monkeypatch.setattr(wm, "PdfReader", DummyReader)
    assert e.read_secret(b"%PDF-1.4 Y") == "AF"


def test_read_secret_attachments_non_bytes_and_decode_error(monkeypatch):
    """
    覆盖：attachments 存在但值不是字节（被跳过）；
         然后走 raw fallback；第一次帧损坏（decode 失败），第二次帧正确。
    """
    e = EmbedFileV1()

    class DummyReader:
        def __init__(self, *a, **kw):
            self.attachments = {"bad": object()}  # 非字节 => 跳过
            self.trailer = {}
    monkeypatch.setattr(wm, "PdfReader", DummyReader)

    # 构造原始字节：先放一个坏帧（无 |），再放一个好帧
    bad_frame = wm.MAGIC.encode() + b"zzz"
    good_frame = make_frame({"secret":"RAWOK2"})
    data = b"%PDF-1.4 ----" + bad_frame + b"----" + good_frame

    assert e.read_secret(data) == "RAWOK2"


def test_read_secret_not_found(monkeypatch):
    e = EmbedFileV1()
    # 强制 raw fallback，且找不到任何 MAGIC
    monkeypatch.setattr(wm, "PdfReader", None)
    with pytest.raises(SecretNotFoundError):
        e.read_secret(b"%PDF-1.4 something else")


def test_get_usage_contains_keywords():
    txt = EmbedFileV1.get_usage()
    assert "Embedded" in txt and "Args" in txt
