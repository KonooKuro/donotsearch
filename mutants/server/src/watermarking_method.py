# -*- coding: utf-8 -*-
"""
watermarking_method.py

Abstract base classes and common utilities for PDF watermarking methods.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import IO, TypeAlias, Union
import os

# ----------------------------
# Public type aliases & errors
# ----------------------------

PdfSource: TypeAlias = Union[bytes, str, os.PathLike[str], IO[bytes]]
"""Accepted input type for a PDF document.

Implementations should *not* assume the input is a file path; always call
:func:`load_pdf_bytes` to normalize a :class:`PdfSource` into
``bytes`` before processing.
"""
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


class WatermarkingError(Exception):
    """Base class for all watermarking-related errors."""


class SecretNotFoundError(WatermarkingError):
    """Raised when a watermark/secret cannot be found in the PDF."""


class InvalidKeyError(WatermarkingError):
    """Raised when the provided key does not validate/decrypt correctly."""


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_orig(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_1(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = None
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_2(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(None)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_3(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(None, "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_4(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), None) as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_5(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open("rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_6(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), ) as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_7(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(None), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_8(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "XXrbXX") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_9(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "RB") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_10(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = None
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_11(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(None, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_12(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, None):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_13(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr("read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_14(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, ):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_15(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "XXreadXX"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_16(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "READ"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_17(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = None  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_18(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError(None)

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_19(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("XXUnsupported PdfSource; expected bytes, path, or binary IOXX")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_20(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("unsupported pdfsource; expected bytes, path, or binary io")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_21(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("UNSUPPORTED PDFSOURCE; EXPECTED BYTES, PATH, OR BINARY IO")

    if not is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_22(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if is_pdf_bytes(data):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_23(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(None):
        raise ValueError("Input does not look like a valid PDF (missing %PDF header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_24(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError(None)
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_25(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("XXInput does not look like a valid PDF (missing %PDF header)XX")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_26(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("input does not look like a valid pdf (missing %pdf header)")
    return data


# ----------------------------
# Helper functions
# ----------------------------

def x_load_pdf_bytes__mutmut_27(src: PdfSource) -> bytes:
    """Normalize a :class:`PdfSource` into raw ``bytes``."""
    if isinstance(src, (bytes, bytearray)):
        data = bytes(src)
    elif isinstance(src, (str, os.PathLike)):
        with open(os.fspath(src), "rb") as fh:
            data = fh.read()
    elif hasattr(src, "read"):
        data = src.read()  # type: ignore[attr-defined]
    else:
        raise TypeError("Unsupported PdfSource; expected bytes, path, or binary IO")

    if not is_pdf_bytes(data):
        raise ValueError("INPUT DOES NOT LOOK LIKE A VALID PDF (MISSING %PDF HEADER)")
    return data

x_load_pdf_bytes__mutmut_mutants : ClassVar[MutantDict] = {
'x_load_pdf_bytes__mutmut_1': x_load_pdf_bytes__mutmut_1, 
    'x_load_pdf_bytes__mutmut_2': x_load_pdf_bytes__mutmut_2, 
    'x_load_pdf_bytes__mutmut_3': x_load_pdf_bytes__mutmut_3, 
    'x_load_pdf_bytes__mutmut_4': x_load_pdf_bytes__mutmut_4, 
    'x_load_pdf_bytes__mutmut_5': x_load_pdf_bytes__mutmut_5, 
    'x_load_pdf_bytes__mutmut_6': x_load_pdf_bytes__mutmut_6, 
    'x_load_pdf_bytes__mutmut_7': x_load_pdf_bytes__mutmut_7, 
    'x_load_pdf_bytes__mutmut_8': x_load_pdf_bytes__mutmut_8, 
    'x_load_pdf_bytes__mutmut_9': x_load_pdf_bytes__mutmut_9, 
    'x_load_pdf_bytes__mutmut_10': x_load_pdf_bytes__mutmut_10, 
    'x_load_pdf_bytes__mutmut_11': x_load_pdf_bytes__mutmut_11, 
    'x_load_pdf_bytes__mutmut_12': x_load_pdf_bytes__mutmut_12, 
    'x_load_pdf_bytes__mutmut_13': x_load_pdf_bytes__mutmut_13, 
    'x_load_pdf_bytes__mutmut_14': x_load_pdf_bytes__mutmut_14, 
    'x_load_pdf_bytes__mutmut_15': x_load_pdf_bytes__mutmut_15, 
    'x_load_pdf_bytes__mutmut_16': x_load_pdf_bytes__mutmut_16, 
    'x_load_pdf_bytes__mutmut_17': x_load_pdf_bytes__mutmut_17, 
    'x_load_pdf_bytes__mutmut_18': x_load_pdf_bytes__mutmut_18, 
    'x_load_pdf_bytes__mutmut_19': x_load_pdf_bytes__mutmut_19, 
    'x_load_pdf_bytes__mutmut_20': x_load_pdf_bytes__mutmut_20, 
    'x_load_pdf_bytes__mutmut_21': x_load_pdf_bytes__mutmut_21, 
    'x_load_pdf_bytes__mutmut_22': x_load_pdf_bytes__mutmut_22, 
    'x_load_pdf_bytes__mutmut_23': x_load_pdf_bytes__mutmut_23, 
    'x_load_pdf_bytes__mutmut_24': x_load_pdf_bytes__mutmut_24, 
    'x_load_pdf_bytes__mutmut_25': x_load_pdf_bytes__mutmut_25, 
    'x_load_pdf_bytes__mutmut_26': x_load_pdf_bytes__mutmut_26, 
    'x_load_pdf_bytes__mutmut_27': x_load_pdf_bytes__mutmut_27
}

def load_pdf_bytes(*args, **kwargs):
    result = _mutmut_trampoline(x_load_pdf_bytes__mutmut_orig, x_load_pdf_bytes__mutmut_mutants, args, kwargs)
    return result 

load_pdf_bytes.__signature__ = _mutmut_signature(x_load_pdf_bytes__mutmut_orig)
x_load_pdf_bytes__mutmut_orig.__name__ = 'x_load_pdf_bytes'


def x_is_pdf_bytes__mutmut_orig(data: bytes) -> bool:
    """Lightweight check that the data looks like a PDF file."""
    return data.startswith(b"%PDF-")


def x_is_pdf_bytes__mutmut_1(data: bytes) -> bool:
    """Lightweight check that the data looks like a PDF file."""
    return data.startswith(None)


def x_is_pdf_bytes__mutmut_2(data: bytes) -> bool:
    """Lightweight check that the data looks like a PDF file."""
    return data.startswith(b"XX%PDF-XX")


def x_is_pdf_bytes__mutmut_3(data: bytes) -> bool:
    """Lightweight check that the data looks like a PDF file."""
    return data.startswith(b"%pdf-")


def x_is_pdf_bytes__mutmut_4(data: bytes) -> bool:
    """Lightweight check that the data looks like a PDF file."""
    return data.startswith(b"%PDF-")

x_is_pdf_bytes__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_pdf_bytes__mutmut_1': x_is_pdf_bytes__mutmut_1, 
    'x_is_pdf_bytes__mutmut_2': x_is_pdf_bytes__mutmut_2, 
    'x_is_pdf_bytes__mutmut_3': x_is_pdf_bytes__mutmut_3, 
    'x_is_pdf_bytes__mutmut_4': x_is_pdf_bytes__mutmut_4
}

def is_pdf_bytes(*args, **kwargs):
    result = _mutmut_trampoline(x_is_pdf_bytes__mutmut_orig, x_is_pdf_bytes__mutmut_mutants, args, kwargs)
    return result 

is_pdf_bytes.__signature__ = _mutmut_signature(x_is_pdf_bytes__mutmut_orig)
x_is_pdf_bytes__mutmut_orig.__name__ = 'x_is_pdf_bytes'


# ---------------------------------
# Abstract base class (the contract)
# ---------------------------------

class WatermarkingMethod(ABC):
    """Stable contract that concrete methods must implement."""

    # user-visible identifier for CLI (e.g., "hidden-object-b64")
    name: str = "abstract"

    @staticmethod
    @abstractmethod
    def get_usage() -> str:
        """Return a short human-readable usage string."""
        raise NotImplementedError

    @abstractmethod
    def add_watermark(
        self,
        pdf: PdfSource,
        secret: str,
        position: str | None = None,
    ) -> bytes:
        """Embed `secret` into `pdf` and return a new PDF as bytes."""
        raise NotImplementedError

    @abstractmethod
    def is_watermark_applicable(
        self,
        pdf: PdfSource,
        position: str | None = None,
    ) -> bool:
        """Return whether the method is applicable to the given PDF."""
        raise NotImplementedError

    @abstractmethod
    def read_secret(self, pdf: PdfSource) -> str:
        """Extract and return the embedded secret from `pdf`."""
        raise NotImplementedError


__all__ = [
    "PdfSource",
    "WatermarkingError",
    "SecretNotFoundError",
    "InvalidKeyError",
    "load_pdf_bytes",
    "is_pdf_bytes",
    "WatermarkingMethod",
]
