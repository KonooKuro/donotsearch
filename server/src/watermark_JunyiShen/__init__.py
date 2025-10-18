# -*- coding: utf-8 -*-
"""
watermark package initializer
Re-exports the embedfile-based watermarking method for discovery by the framework.
"""
try:
    from .wm_embedfile_v1 import METHOD_INSTANCE as EmbedFileV1  # noqa: F401
except Exception:
    # Keep import errors silent here; the hosting app may handle optional methods.
    pass
