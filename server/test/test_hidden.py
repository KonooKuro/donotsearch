import io, base64, types, pytest
from src import hidden as h

WatermarkingError = h.WatermarkingError
SecretNotFoundError = h.SecretNotFoundError


# ---------- _require_deps ----------

def test_require_deps(monkeypatch):
    monkeypatch.setattr(h, "pikepdf", object())
    h._require_deps()  # 正常不抛错
    monkeypatch.setattr(h, "pikepdf", None)
    with pytest.raises(WatermarkingError):
        h._require_deps()


# ---------- add_watermark ----------

def test_add_watermark_empty_secret(monkeypatch):
    m = h.HiddenObjectB64Method()
    monkeypatch.setattr(h, "pikepdf", object())
    with pytest.raises(ValueError):
        m.add_watermark(b"%PDF-1.4", secret="")


def test_add_watermark_root_missing(monkeypatch):
    """Root 为 None 应抛 WatermarkingError"""
    m = h.HiddenObjectB64Method()

    class DummyDoc:
        def __init__(self, *a, **kw):
            self.trailer = {"/Root": None}
        def save(self, out): out.write(b"%PDF-1.4 saved")
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def make_stream(self, payload, meta): return b"stream"

    class DummyStream:
        def __init__(self, *a, **kw): pass

    # 关键：既提供 Pdf.open，也提供模块级 open
    class DummyPdfCls:
        @staticmethod
        def open(buf): return DummyDoc()

    dummy = types.SimpleNamespace(
        Name=lambda s: s,
        Dictionary=dict,
        Stream=DummyStream,
        Pdf=DummyPdfCls,
        open=DummyPdfCls.open,
    )

    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF-1.4")

    with pytest.raises(WatermarkingError):
        m.add_watermark(b"%PDF", secret="x")


def test_add_watermark_old_make_indirect(monkeypatch):
    """模拟无 make_stream 但有 make_indirect 的旧版"""
    m = h.HiddenObjectB64Method()

    class DummyDoc:
        def __init__(self, *a, **kw):
            self.trailer = {"/Root": {}}
        def save(self, out): out.write(b"%PDF done")
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def make_indirect(self, obj): return b"ref"

    class DummyStream:
        def __init__(self, doc, payload, meta): pass

    class DummyPdfCls:
        @staticmethod
        def open(buf): return DummyDoc()

    dummy = types.SimpleNamespace(
        Name=lambda s: s,
        Dictionary=dict,
        Stream=DummyStream,   # 旧版路径会用到 Stream(doc, payload, meta)
        Pdf=DummyPdfCls,
        open=DummyPdfCls.open,
    )

    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF-1.4 data")
    out = m.add_watermark(b"%PDF-1.4", secret="HELLO")
    assert b"%PDF" in out


def test_add_watermark_make_stream(monkeypatch):
    """新版 make_stream 路径"""
    m = h.HiddenObjectB64Method()

    class DummyDoc:
        def __init__(self, *a, **kw):
            self.trailer = {"/Root": {}}
        def save(self, out): out.write(b"ok")
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def make_stream(self, payload, meta): return b"ref"

    class DummyStream:
        def __init__(self, *a, **kw): pass

    class DummyPdfCls:
        @staticmethod
        def open(buf): return DummyDoc()

    dummy = types.SimpleNamespace(
        Name=lambda s: s,
        Dictionary=dict,
        Stream=DummyStream,
        Pdf=DummyPdfCls,
        open=DummyPdfCls.open,
    )

    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF")
    out = m.add_watermark(b"%PDF", secret="abc")
    assert b"ok" in out


def test_add_watermark_old_no_make(monkeypatch):
    """既无 make_stream 又无 make_indirect"""
    m = h.HiddenObjectB64Method()

    class DummyDoc:
        def __init__(self, *a, **kw):
            self.trailer = {"/Root": {}}
        def __enter__(self): return self
        def __exit__(self, *a): pass
        # 注意：不提供 make_stream / make_indirect -> 触发异常分支

    class DummyStream:
        def __init__(self, *a, **kw): pass

    class DummyPdfCls:
        @staticmethod
        def open(buf): return DummyDoc()

    dummy = types.SimpleNamespace(
        Name=lambda s: s,
        Dictionary=dict,
        Stream=DummyStream,
        Pdf=DummyPdfCls,
        open=DummyPdfCls.open,
    )

    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF")
    with pytest.raises(WatermarkingError):
        m.add_watermark(b"%PDF", secret="x")


def test_add_watermark_runtime_error(monkeypatch):
    m = h.HiddenObjectB64Method()

    class DummyStream:
        def __init__(self, *a, **kw): pass

    class DummyPdfCls:
        @staticmethod
        def open(buf):
            raise RuntimeError("open fail")

    dummy = types.SimpleNamespace(
        Name=lambda s: s,
        Dictionary=dict,
        Stream=DummyStream,
        Pdf=DummyPdfCls,
        open=DummyPdfCls.open,
    )

    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF")
    with pytest.raises(h.WatermarkingError):
        m.add_watermark(b"%PDF", secret="ok")



# ---------- is_watermark_applicable ----------

def test_is_applicable_true_false(monkeypatch):
    m = h.HiddenObjectB64Method()
    class DummyDoc:
        def __enter__(self): return self
        def __exit__(self,*a): pass
    dummy = types.SimpleNamespace(open=lambda b: DummyDoc())
    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF")
    assert m.is_watermark_applicable(b"%PDF")
    # open 抛异常
    monkeypatch.setattr(dummy, "open", lambda b: (_ for _ in ()).throw(RuntimeError()))
    assert not m.is_watermark_applicable(b"%PDF")
    # pikepdf=None
    monkeypatch.setattr(h, "pikepdf", None)
    assert not m.is_watermark_applicable(b"%PDF")


# ---------- read_secret ----------

def test_read_secret_root_direct(monkeypatch):
    """Root 直接包含 Stream"""
    m = h.HiddenObjectB64Method()
    payload = base64.urlsafe_b64encode(b"SECRET")
    class DummyStream:
        def read_bytes(self): return payload
    root = {h.HIDDEN_KEY_NAME: DummyStream()}
    class DummyDoc:
        def __init__(self): self.trailer={"/Root":root}
        def __enter__(self): return self
        def __exit__(self,*a): pass
        def objects(self): return []
    dummy = types.SimpleNamespace(
        Name=lambda s:s, Stream=DummyStream, open=lambda f: DummyDoc()
    )
    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF")
    assert m.read_secret(b"%PDF") == "SECRET"


def test_read_secret_root_indirect(monkeypatch):
    """Root 间接引用情况"""
    m = h.HiddenObjectB64Method()
    payload = base64.urlsafe_b64encode(b"INDIRECT")
    class DummyStream:
        def __init__(self,doc,ref=None): pass
        def read_bytes(self): return payload
    root = {h.HIDDEN_KEY_NAME: b"refobj"}
    class DummyDoc:
        def __init__(self): self.trailer={"/Root":root}
        def __enter__(self): return self
        def __exit__(self,*a): pass
        def objects(self): return []
    dummy = types.SimpleNamespace(
        Name=lambda s:s, Stream=DummyStream, open=lambda f: DummyDoc()
    )
    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF")
    assert m.read_secret(b"%PDF") == "INDIRECT"


def test_read_secret_scan_objects(monkeypatch):
    """Root 失败，遍历 objects 找到"""
    m = h.HiddenObjectB64Method()
    payload = base64.urlsafe_b64encode(b"SCANOK")
    class DummyStream:
        def __init__(self,*a,**kw): pass
        def read_bytes(self): return payload
        def get(self,k,d=None):
            if k=="/Subtype": return "/XML"
            if k=="/Alg": return "/Filter"
    obj = DummyStream()
    class DummyDoc:
        def __init__(self):
            self.trailer={"/Root":{}}
            self.objects=[obj]
        def __enter__(self): return self
        def __exit__(self,*a): pass
    dummy = types.SimpleNamespace(
        Name=lambda s:s, Stream=DummyStream, open=lambda f: DummyDoc()
    )
    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF")
    assert m.read_secret(b"%PDF") == "SCANOK"


def test_read_secret_decode_error(monkeypatch):
    """decode 失败后抛 SecretNotFoundError"""
    m = h.HiddenObjectB64Method()
    class DummyStream:
        def read_bytes(self): return b"!!badbase64"
        def get(self,k,d=None):
            if k=="/Subtype": return "/XML"
            if k=="/Alg": return "/Filter"
    bad = DummyStream()
    class DummyDoc:
        def __init__(self):
            self.trailer={"/Root":{}}
            self.objects=[bad]
        def __enter__(self): return self
        def __exit__(self,*a): pass
    dummy = types.SimpleNamespace(
        Name=lambda s:s, Stream=DummyStream, open=lambda f: DummyDoc()
    )
    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF")
    with pytest.raises(SecretNotFoundError):
        m.read_secret(b"%PDF")


def test_read_secret_fatal_error(monkeypatch):
    """pikepdf.open 抛异常"""
    m = h.HiddenObjectB64Method()
    dummy = types.SimpleNamespace(open=lambda f: (_ for _ in ()).throw(RuntimeError("fail")))
    monkeypatch.setattr(h, "pikepdf", dummy)
    monkeypatch.setattr(h, "load_pdf_bytes", lambda x: b"%PDF")
    with pytest.raises(SecretNotFoundError):
        m.read_secret(b"%PDF")


def test_get_usage():
    assert "hide watermark" in h.HiddenObjectB64Method.get_usage().lower()
