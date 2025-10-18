# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Optional
import io
import base64

from watermarking_method import (
    PdfSource,
    WatermarkingError,
    SecretNotFoundError,
    load_pdf_bytes,
    WatermarkingMethod,
)

# 第三方
try:
    import pikepdf
except Exception:  # pragma: no cover
    pikepdf = None

# ------------ 常量 ------------
SUBTYPE = "/XML"
ALG_NAME = "/Filter"
VERSION = "PDF-1.4"
HIDDEN_KEY_NAME = pikepdf.Name("/ColorSpace")
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

def x__require_deps__mutmut_orig():
    if pikepdf is None:
        raise WatermarkingError("需要安装 pikepdf：pip install pikepdf")

def x__require_deps__mutmut_1():
    if pikepdf is not None:
        raise WatermarkingError("需要安装 pikepdf：pip install pikepdf")

def x__require_deps__mutmut_2():
    if pikepdf is None:
        raise WatermarkingError(None)

def x__require_deps__mutmut_3():
    if pikepdf is None:
        raise WatermarkingError("XX需要安装 pikepdf：pip install pikepdfXX")

def x__require_deps__mutmut_4():
    if pikepdf is None:
        raise WatermarkingError("需要安装 PIKEPDF：PIP INSTALL PIKEPDF")

x__require_deps__mutmut_mutants : ClassVar[MutantDict] = {
'x__require_deps__mutmut_1': x__require_deps__mutmut_1, 
    'x__require_deps__mutmut_2': x__require_deps__mutmut_2, 
    'x__require_deps__mutmut_3': x__require_deps__mutmut_3, 
    'x__require_deps__mutmut_4': x__require_deps__mutmut_4
}

def _require_deps(*args, **kwargs):
    result = _mutmut_trampoline(x__require_deps__mutmut_orig, x__require_deps__mutmut_mutants, args, kwargs)
    return result 

_require_deps.__signature__ = _mutmut_signature(x__require_deps__mutmut_orig)
x__require_deps__mutmut_orig.__name__ = 'x__require_deps'


class HiddenObjectB64Method(WatermarkingMethod):
    """
    将 Base64 编码后的密文放入一个不被引用的流对象中（孤立对象）。
    读取时遍历所有间接对象，匹配标记并解码。
    """
    name: str = "Hide_Watermark"

    @staticmethod
    def get_usage() -> str:
        return (
            "A method that hide watermark in the PDF."
        )

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_orig(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_1(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_2(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError(None)

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_3(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("XXSecret cannot be emptyXX")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_4(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_5(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("SECRET CANNOT BE EMPTY")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_6(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = None
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_7(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(None)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_8(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(None) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_9(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(None)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_10(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = None  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_11(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get(None)  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_12(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("XX/RootXX")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_13(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_14(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/ROOT")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_15(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = None
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_16(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary(None)
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_17(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "XX/SubtypeXX": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_18(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_19(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/SUBTYPE": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_20(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(None),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_21(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = None

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_22(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(None)

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_23(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode(None))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_24(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("XXutf-8XX"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_25(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("UTF-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_26(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(None, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_27(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, None):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_28(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr("make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_29(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, ):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_30(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "XXmake_streamXX"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_31(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "MAKE_STREAM"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_32(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = None
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_33(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(None, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_34(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, None)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_35(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_36(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, )
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_37(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = None
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_38(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(None, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_39(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, None, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_40(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, None)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_41(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_42(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_43(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, )
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_44(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(None, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_45(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, None):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_46(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr("make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_47(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, ):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_48(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "XXmake_indirectXX"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_49(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "MAKE_INDIRECT"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_50(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = None
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_51(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(None)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_52(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            None
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_53(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "XX当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；XX"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_54(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 PIKEPDF 过旧，既无 MAKE_STREAM 也无 MAKE_INDIRECT；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_55(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "XX请运行 `pip install -U pikepdf` 升级XX"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_56(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -u pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_57(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `PIP INSTALL -U PIKEPDF` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_58(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is not None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_59(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError(None)
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_60(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("XXPDF 缺少 /Root 对象，无法挂接隐藏对象XX")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_61(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("pdf 缺少 /root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_62(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /ROOT 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_63(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = None

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_64(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = None
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_65(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(None)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(f"failed to write watermark: {e}") from e

    def xǁHiddenObjectB64Methodǁadd_watermark__mutmut_66(
        self,
        pdf: PdfSource,
        secret: str,
        position: Optional[str] = None # 未使用
    ) -> bytes:
        _require_deps()
        if not secret:
            raise ValueError("Secret cannot be empty")

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                root = doc.trailer.get("/Root")  # PDF Catalog
                meta = pikepdf.Dictionary({
                    "/Subtype": pikepdf.Name(SUBTYPE),
                })
                # 无引用对象
                payload = base64.urlsafe_b64encode(secret.encode("utf-8"))

                # --- 兼容多版本 pikepdf 的“新增孤立流对象” ---
                if hasattr(doc, "make_stream"):
                    # 新版 pikepdf：直接创建并登记为间接流对象
                    _ref = doc.make_stream(payload, meta)
                else:
                    # 老版本：先构造 Stream，再用 make_indirect 挂进 xref（不建立任何引用）
                    stream = pikepdf.Stream(doc, payload, meta)
                    if hasattr(doc, "make_indirect"):
                        _ref = doc.make_indirect(stream)
                    else:
                        raise WatermarkingError(
                            "当前 pikepdf 过旧，既无 make_stream 也无 make_indirect；"
                            "请运行 `pip install -U pikepdf` 升级"
                        )
                if root is None:
                    raise WatermarkingError("PDF 缺少 /Root 对象，无法挂接隐藏对象")
                root[HIDDEN_KEY_NAME] = _ref

                out = io.BytesIO()
                doc.save(out)
                return out.getvalue()

        except Exception as e:
            raise WatermarkingError(None) from e
    
    xǁHiddenObjectB64Methodǁadd_watermark__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_1': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_1, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_2': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_2, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_3': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_3, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_4': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_4, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_5': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_5, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_6': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_6, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_7': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_7, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_8': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_8, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_9': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_9, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_10': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_10, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_11': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_11, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_12': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_12, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_13': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_13, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_14': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_14, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_15': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_15, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_16': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_16, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_17': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_17, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_18': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_18, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_19': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_19, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_20': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_20, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_21': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_21, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_22': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_22, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_23': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_23, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_24': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_24, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_25': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_25, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_26': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_26, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_27': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_27, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_28': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_28, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_29': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_29, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_30': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_30, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_31': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_31, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_32': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_32, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_33': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_33, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_34': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_34, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_35': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_35, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_36': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_36, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_37': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_37, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_38': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_38, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_39': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_39, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_40': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_40, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_41': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_41, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_42': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_42, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_43': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_43, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_44': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_44, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_45': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_45, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_46': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_46, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_47': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_47, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_48': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_48, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_49': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_49, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_50': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_50, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_51': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_51, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_52': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_52, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_53': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_53, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_54': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_54, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_55': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_55, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_56': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_56, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_57': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_57, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_58': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_58, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_59': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_59, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_60': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_60, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_61': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_61, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_62': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_62, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_63': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_63, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_64': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_64, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_65': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_65, 
        'xǁHiddenObjectB64Methodǁadd_watermark__mutmut_66': xǁHiddenObjectB64Methodǁadd_watermark__mutmut_66
    }
    
    def add_watermark(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHiddenObjectB64Methodǁadd_watermark__mutmut_orig"), object.__getattribute__(self, "xǁHiddenObjectB64Methodǁadd_watermark__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_watermark.__signature__ = _mutmut_signature(xǁHiddenObjectB64Methodǁadd_watermark__mutmut_orig)
    xǁHiddenObjectB64Methodǁadd_watermark__mutmut_orig.__name__ = 'xǁHiddenObjectB64Methodǁadd_watermark'

    def xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_orig(
        self,
        pdf: PdfSource,
        position: Optional[str] = None,
    ) -> bool:
        if pikepdf is None:
            return False
        try:
            data = load_pdf_bytes(pdf)
            with pikepdf.open(io.BytesIO(data)):
                return True
        except Exception:
            return False

    def xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_1(
        self,
        pdf: PdfSource,
        position: Optional[str] = None,
    ) -> bool:
        if pikepdf is not None:
            return False
        try:
            data = load_pdf_bytes(pdf)
            with pikepdf.open(io.BytesIO(data)):
                return True
        except Exception:
            return False

    def xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_2(
        self,
        pdf: PdfSource,
        position: Optional[str] = None,
    ) -> bool:
        if pikepdf is None:
            return True
        try:
            data = load_pdf_bytes(pdf)
            with pikepdf.open(io.BytesIO(data)):
                return True
        except Exception:
            return False

    def xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_3(
        self,
        pdf: PdfSource,
        position: Optional[str] = None,
    ) -> bool:
        if pikepdf is None:
            return False
        try:
            data = None
            with pikepdf.open(io.BytesIO(data)):
                return True
        except Exception:
            return False

    def xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_4(
        self,
        pdf: PdfSource,
        position: Optional[str] = None,
    ) -> bool:
        if pikepdf is None:
            return False
        try:
            data = load_pdf_bytes(None)
            with pikepdf.open(io.BytesIO(data)):
                return True
        except Exception:
            return False

    def xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_5(
        self,
        pdf: PdfSource,
        position: Optional[str] = None,
    ) -> bool:
        if pikepdf is None:
            return False
        try:
            data = load_pdf_bytes(pdf)
            with pikepdf.open(None):
                return True
        except Exception:
            return False

    def xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_6(
        self,
        pdf: PdfSource,
        position: Optional[str] = None,
    ) -> bool:
        if pikepdf is None:
            return False
        try:
            data = load_pdf_bytes(pdf)
            with pikepdf.open(io.BytesIO(None)):
                return True
        except Exception:
            return False

    def xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_7(
        self,
        pdf: PdfSource,
        position: Optional[str] = None,
    ) -> bool:
        if pikepdf is None:
            return False
        try:
            data = load_pdf_bytes(pdf)
            with pikepdf.open(io.BytesIO(data)):
                return False
        except Exception:
            return False

    def xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_8(
        self,
        pdf: PdfSource,
        position: Optional[str] = None,
    ) -> bool:
        if pikepdf is None:
            return False
        try:
            data = load_pdf_bytes(pdf)
            with pikepdf.open(io.BytesIO(data)):
                return True
        except Exception:
            return True
    
    xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_1': xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_1, 
        'xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_2': xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_2, 
        'xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_3': xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_3, 
        'xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_4': xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_4, 
        'xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_5': xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_5, 
        'xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_6': xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_6, 
        'xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_7': xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_7, 
        'xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_8': xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_8
    }
    
    def is_watermark_applicable(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_orig"), object.__getattribute__(self, "xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_watermark_applicable.__signature__ = _mutmut_signature(xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_orig)
    xǁHiddenObjectB64Methodǁis_watermark_applicable__mutmut_orig.__name__ = 'xǁHiddenObjectB64Methodǁis_watermark_applicable'

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_orig(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_1(self, pdf: PdfSource) -> str:
        _require_deps()

        data = None
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_2(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(None)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_3(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(None) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_4(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(None)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_5(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = None
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_6(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get(None)
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_7(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("XX/RootXX")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_8(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_9(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/ROOT")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_10(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_11(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = None

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_12(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(None, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_13(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_14(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, )

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_15(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = None
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_16(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode(None)

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_17(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(None).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_18(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("XXutf-8XX")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_19(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("UTF-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_20(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_21(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = None
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_22(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(None, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_23(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, None)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_24(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_25(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, )
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_26(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = None
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_27(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode(None)
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_28(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(None).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_29(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("XXutf-8XX")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_30(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("UTF-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_31(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = None
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_32(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = True
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_33(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = ""

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_34(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_35(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        break
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_36(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = None
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_37(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get(None, None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_38(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get(None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_39(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", )
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_40(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("XX/SubtypeXX", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_41(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_42(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/SUBTYPE", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_43(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = None
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_44(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get(None, None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_45(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get(None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_46(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", )
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_47(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("XX/AlgXX", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_48(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_49(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/ALG", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_50(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) and alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_51(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype == pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_52(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(None) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_53(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg == pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_54(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(None):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_55(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            break

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_56(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = None
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_57(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = False
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_58(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = None
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_59(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = None
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_60(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode(None)
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_61(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(None).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_62(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("XXutf-8XX")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_63(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("UTF-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_64(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = None
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_65(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            break
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_66(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = None
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_67(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        break

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_68(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any or last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_69(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_70(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(None)
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_71(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError(None)
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_72(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("XXNo watermark foundXX")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_73(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("no watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_74(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("NO WATERMARK FOUND")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(f"Read watermark failed: {e}")

    def xǁHiddenObjectB64Methodǁread_secret__mutmut_75(self, pdf: PdfSource) -> str:
        _require_deps()

        data = load_pdf_bytes(pdf)
        try:
            with pikepdf.open(io.BytesIO(data)) as doc:
                # 先尝试从 /Root 的隐蔽引用直接读取（若存在）
                try:
                    root = doc.trailer.get("/Root")
                    if root is not None:
                        ref = root.get(HIDDEN_KEY_NAME, None)

                        if isinstance(ref, pikepdf.Stream):
                            encoded = ref.read_bytes()
                            return base64.urlsafe_b64decode(encoded).decode("utf-8")

                        # 某些版本返回的是一个“间接引用”，再解引用一次
                        if ref is not None:
                            try:
                                stream_obj = pikepdf.Stream(doc, ref)
                                encoded = stream_obj.read_bytes()
                                return base64.urlsafe_b64decode(encoded).decode("utf-8")
                            except Exception:
                                pass
                except Exception:
                    # 忽略 Root 路径的错误，退回到全量扫描
                    pass

                # 兜底：遍历所有对象（包含无引用对象）
                found_any = False
                last_err: Optional[Exception] = None

                for obj in doc.objects:
                    if not isinstance(obj, pikepdf.Stream):
                        continue
                    try:
                        subtype = obj.get("/Subtype", None)
                        alg = obj.get("/Alg", None)
                        if subtype != pikepdf.Name(SUBTYPE) or alg != pikepdf.Name(ALG_NAME):
                            continue

                        found_any = True
                        encoded = obj.read_bytes()
                        try:
                            text = base64.urlsafe_b64decode(encoded).decode("utf-8")
                            return text
                        except Exception as e:
                            last_err = e
                            continue
                    except Exception as e:
                        last_err = e
                        continue

            if found_any and last_err is not None:
                raise SecretNotFoundError(f"failed to decode: {last_err}")
            raise SecretNotFoundError("No watermark found")
        except SecretNotFoundError:
            raise
        except Exception as e:
            raise SecretNotFoundError(None)
    
    xǁHiddenObjectB64Methodǁread_secret__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHiddenObjectB64Methodǁread_secret__mutmut_1': xǁHiddenObjectB64Methodǁread_secret__mutmut_1, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_2': xǁHiddenObjectB64Methodǁread_secret__mutmut_2, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_3': xǁHiddenObjectB64Methodǁread_secret__mutmut_3, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_4': xǁHiddenObjectB64Methodǁread_secret__mutmut_4, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_5': xǁHiddenObjectB64Methodǁread_secret__mutmut_5, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_6': xǁHiddenObjectB64Methodǁread_secret__mutmut_6, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_7': xǁHiddenObjectB64Methodǁread_secret__mutmut_7, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_8': xǁHiddenObjectB64Methodǁread_secret__mutmut_8, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_9': xǁHiddenObjectB64Methodǁread_secret__mutmut_9, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_10': xǁHiddenObjectB64Methodǁread_secret__mutmut_10, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_11': xǁHiddenObjectB64Methodǁread_secret__mutmut_11, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_12': xǁHiddenObjectB64Methodǁread_secret__mutmut_12, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_13': xǁHiddenObjectB64Methodǁread_secret__mutmut_13, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_14': xǁHiddenObjectB64Methodǁread_secret__mutmut_14, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_15': xǁHiddenObjectB64Methodǁread_secret__mutmut_15, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_16': xǁHiddenObjectB64Methodǁread_secret__mutmut_16, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_17': xǁHiddenObjectB64Methodǁread_secret__mutmut_17, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_18': xǁHiddenObjectB64Methodǁread_secret__mutmut_18, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_19': xǁHiddenObjectB64Methodǁread_secret__mutmut_19, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_20': xǁHiddenObjectB64Methodǁread_secret__mutmut_20, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_21': xǁHiddenObjectB64Methodǁread_secret__mutmut_21, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_22': xǁHiddenObjectB64Methodǁread_secret__mutmut_22, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_23': xǁHiddenObjectB64Methodǁread_secret__mutmut_23, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_24': xǁHiddenObjectB64Methodǁread_secret__mutmut_24, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_25': xǁHiddenObjectB64Methodǁread_secret__mutmut_25, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_26': xǁHiddenObjectB64Methodǁread_secret__mutmut_26, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_27': xǁHiddenObjectB64Methodǁread_secret__mutmut_27, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_28': xǁHiddenObjectB64Methodǁread_secret__mutmut_28, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_29': xǁHiddenObjectB64Methodǁread_secret__mutmut_29, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_30': xǁHiddenObjectB64Methodǁread_secret__mutmut_30, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_31': xǁHiddenObjectB64Methodǁread_secret__mutmut_31, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_32': xǁHiddenObjectB64Methodǁread_secret__mutmut_32, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_33': xǁHiddenObjectB64Methodǁread_secret__mutmut_33, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_34': xǁHiddenObjectB64Methodǁread_secret__mutmut_34, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_35': xǁHiddenObjectB64Methodǁread_secret__mutmut_35, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_36': xǁHiddenObjectB64Methodǁread_secret__mutmut_36, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_37': xǁHiddenObjectB64Methodǁread_secret__mutmut_37, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_38': xǁHiddenObjectB64Methodǁread_secret__mutmut_38, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_39': xǁHiddenObjectB64Methodǁread_secret__mutmut_39, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_40': xǁHiddenObjectB64Methodǁread_secret__mutmut_40, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_41': xǁHiddenObjectB64Methodǁread_secret__mutmut_41, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_42': xǁHiddenObjectB64Methodǁread_secret__mutmut_42, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_43': xǁHiddenObjectB64Methodǁread_secret__mutmut_43, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_44': xǁHiddenObjectB64Methodǁread_secret__mutmut_44, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_45': xǁHiddenObjectB64Methodǁread_secret__mutmut_45, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_46': xǁHiddenObjectB64Methodǁread_secret__mutmut_46, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_47': xǁHiddenObjectB64Methodǁread_secret__mutmut_47, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_48': xǁHiddenObjectB64Methodǁread_secret__mutmut_48, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_49': xǁHiddenObjectB64Methodǁread_secret__mutmut_49, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_50': xǁHiddenObjectB64Methodǁread_secret__mutmut_50, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_51': xǁHiddenObjectB64Methodǁread_secret__mutmut_51, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_52': xǁHiddenObjectB64Methodǁread_secret__mutmut_52, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_53': xǁHiddenObjectB64Methodǁread_secret__mutmut_53, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_54': xǁHiddenObjectB64Methodǁread_secret__mutmut_54, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_55': xǁHiddenObjectB64Methodǁread_secret__mutmut_55, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_56': xǁHiddenObjectB64Methodǁread_secret__mutmut_56, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_57': xǁHiddenObjectB64Methodǁread_secret__mutmut_57, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_58': xǁHiddenObjectB64Methodǁread_secret__mutmut_58, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_59': xǁHiddenObjectB64Methodǁread_secret__mutmut_59, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_60': xǁHiddenObjectB64Methodǁread_secret__mutmut_60, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_61': xǁHiddenObjectB64Methodǁread_secret__mutmut_61, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_62': xǁHiddenObjectB64Methodǁread_secret__mutmut_62, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_63': xǁHiddenObjectB64Methodǁread_secret__mutmut_63, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_64': xǁHiddenObjectB64Methodǁread_secret__mutmut_64, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_65': xǁHiddenObjectB64Methodǁread_secret__mutmut_65, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_66': xǁHiddenObjectB64Methodǁread_secret__mutmut_66, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_67': xǁHiddenObjectB64Methodǁread_secret__mutmut_67, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_68': xǁHiddenObjectB64Methodǁread_secret__mutmut_68, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_69': xǁHiddenObjectB64Methodǁread_secret__mutmut_69, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_70': xǁHiddenObjectB64Methodǁread_secret__mutmut_70, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_71': xǁHiddenObjectB64Methodǁread_secret__mutmut_71, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_72': xǁHiddenObjectB64Methodǁread_secret__mutmut_72, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_73': xǁHiddenObjectB64Methodǁread_secret__mutmut_73, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_74': xǁHiddenObjectB64Methodǁread_secret__mutmut_74, 
        'xǁHiddenObjectB64Methodǁread_secret__mutmut_75': xǁHiddenObjectB64Methodǁread_secret__mutmut_75
    }
    
    def read_secret(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHiddenObjectB64Methodǁread_secret__mutmut_orig"), object.__getattribute__(self, "xǁHiddenObjectB64Methodǁread_secret__mutmut_mutants"), args, kwargs, self)
        return result 
    
    read_secret.__signature__ = _mutmut_signature(xǁHiddenObjectB64Methodǁread_secret__mutmut_orig)
    xǁHiddenObjectB64Methodǁread_secret__mutmut_orig.__name__ = 'xǁHiddenObjectB64Methodǁread_secret'



# 工厂实例（供注册表使用）
METHOD_INSTANCE = HiddenObjectB64Method()
