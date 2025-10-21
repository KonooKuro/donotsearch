# -*- coding: utf-8 -*-
import sys
import types
import pathlib
import json
import importlib
import contextlib
import pytest

# --- 总是导入 src/ 下的真实模块，避免被顶层别名或全局 monkeypatch 污染 ---
BASE = pathlib.Path(__file__).resolve().parents[1]  # .../server
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

wu = importlib.import_module("src.watermarking_utils")
WatermarkingMethod = importlib.import_module("src.watermarking_method").WatermarkingMethod


# --------- 伪方法类（继承 WatermarkingMethod，补齐抽象方法） ---------
class _FakeMethodBase(WatermarkingMethod):
    name = "fake-base"

    @staticmethod
    def get_usage() -> str:
        return "fake usage"

    def add_watermark(self, *, pdf, secret, position=None, key=None):
        raise NotImplementedError

    def is_watermark_applicable(self, *, pdf, position=None):
        return True

    def read_secret(self, *, pdf, key=None):
        return "secret"


class _FakeKeyed(_FakeMethodBase):
    name = "fake-keyed"

    def add_watermark(self, *, pdf, secret, position=None, key=None):
        # 回显用于断言
        return (b"%PDF-1.4\n" + f"[{secret}|{position}|{key}]".encode("utf-8") + b"\n%%EOF")

    def read_secret(self, *, pdf, key=None):
        return f"read:{key or ''}"


class _FakeKeyless(_FakeMethodBase):
    name = "fake-keyless"
    # 故意不接受 key，触发 utils 内的回退逻辑

    def add_watermark(self, *, pdf, secret, position=None):
        return (b"%PDF-1.4\n" + f"[{secret}|{position}]".encode("utf-8") + b"\n%%EOF")

    def read_secret(self, *, pdf):
        return "read:nokey"


class _FakeRaisesTypeError(_FakeMethodBase):
    name = "fake-raises-typeerror"

    def add_watermark(self, *, pdf, secret, position=None, key=None):
        # 与 key 无关的 TypeError，应该原样冒泡
        raise TypeError("boom")


# --- 每个测试独立快照/恢复注册表，避免跨文件/跨用例串味 ---
@pytest.fixture
def _clean_registry():
    snap = dict(wu.METHODS)
    try:
        yield
    finally:
        wu.METHODS.clear()
        wu.METHODS.update(snap)


# ---------------- registry ----------------
def test_register_and_get_method_roundtrip(_clean_registry):
    m = _FakeKeyed()
    wu.register_method(m)
    got1 = wu.get_method("fake-keyed")
    assert got1 is m
    # 传入实例时应直通返回（必须是 WatermarkingMethod 子类）
    assert wu.get_method(m) is m

    with pytest.raises(KeyError) as ei:
        wu.get_method("no-such-method")
    assert "Unknown watermarking method" in str(ei.value)


# --------------- apply/read 调度 ---------------
def test_apply_watermark_calls_keyed_and_keyless(_clean_registry):
    # keyed: 传递 key
    m1 = _FakeKeyed()
    wu.register_method(m1)
    out = wu.apply_watermark("fake-keyed", pdf=b"%PDF-1.4\n%%EOF", secret="s", position="eof", key="K")
    assert out.startswith(b"%PDF-")
    assert b"[s|eof|K]" in out

    # keyless: 触发 "unexpected keyword argument 'key'" 回退
    m2 = _FakeKeyless()
    wu.register_method(m2)
    out2 = wu.apply_watermark("fake-keyless", pdf=b"%PDF-1.4\n%%EOF", secret="z", position="bof", key="IGNORED")
    assert b"[z|bof]" in out2  # 不应包含 key

    # 与 key 无关的 TypeError 应冒泡
    m3 = _FakeRaisesTypeError()
    wu.register_method(m3)
    with pytest.raises(TypeError):
        wu.apply_watermark("fake-raises-typeerror", pdf=b"%PDF-1.4\n%%EOF", secret="x")


def test_is_watermarking_applicable_and_read_watermark(_clean_registry):
    m1 = _FakeKeyed()
    wu.register_method(m1)
    assert wu.is_watermarking_applicable("fake-keyed", pdf=b"%PDF-1.4\n%%EOF") is True
    assert wu.read_watermark("fake-keyed", pdf=b"%PDF-1.4\n%%EOF", key="kk") == "read:kk"

    m2 = _FakeKeyless()
    wu.register_method(m2)
    # read 回退（方法不接受 key）
    assert wu.read_watermark("fake-keyless", pdf=b"%PDF-1.4\n%%EOF", key="ignored") == "read:nokey"

    with pytest.raises(KeyError):
        wu.read_watermark("no-such", pdf=b"%PDF-1.4\n%%EOF")


# --------------- explore_pdf ---------------
def test_explore_pdf_regex_fallback_enumerates_nodes():
    # 无 fitz 时走 regex 回退
    pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Page >>\nendobj\n"
        b"2 0 obj\n<< /Type /XObject >>\nendobj\n"
        b"%%EOF\n"
    )
    tree = wu.explore_pdf(pdf)
    assert tree["id"].startswith("pdf:")
    assert tree["size"] == len(pdf)
    ids = [c["id"] for c in tree["children"]]
    assert any(i.startswith("page:") for i in ids)
    assert any(i.startswith("obj:") for i in ids)


def test_explore_pdf_with_fake_fitz(monkeypatch):
    # 注入假的 fitz 模块以覆盖 fitz 分支
    class _FakePage:
        def bound(self):
            return (0, 0, 100, 200)

    class _FakeDoc:
        def __init__(self, stream, filetype):
            self._pages = 2

        @property
        def page_count(self):
            return 2

        def load_page(self, idx):
            return _FakePage()

        def xref_length(self):
            return 4  # 1..3

        def xref_object(self, xref, compressed=False):
            if xref == 1:
                return "/Type /XObject\n<<>>"
            elif xref == 2:
                return "/Type /Page\n<<>>"
            else:
                return "<< /Length 10 >>"

        def xref_is_stream(self, xref):
            return xref == 3

        def close(self):
            pass

    fake_fitz = types.SimpleNamespace(open=lambda stream, filetype: _FakeDoc(stream, filetype))
    monkeypatch.setitem(sys.modules, "fitz", fake_fitz)

    pdf = b"%PDF-1.4\n%%EOF\n"
    tree = wu.explore_pdf(pdf)
    ids = [c["id"] for c in tree["children"]]
    assert any(i.startswith("page:") for i in ids)
    xobjs = [c for c in tree["children"] if c["id"].startswith("obj:")]
    assert len(xobjs) >= 1
    assert "is_stream" in xobjs[0]
