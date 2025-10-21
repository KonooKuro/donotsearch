# -*- coding: utf-8 -*-
# conftest.py — unify imports to src/, avoid duplicate modules in coverage,
# and set sensible defaults for tests.

import os
import sys
import pathlib
import importlib
import contextlib
import types
import pytest

# ---------------------------------------------------------------------
# 1) Ensure src/ is on sys.path (before project root), so imports hit the real code
# ---------------------------------------------------------------------
ROOT = pathlib.Path(__file__).resolve().parents[1]   # e.g. .../server
SRC = ROOT / "src"

for p in (str(SRC), str(ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

# ---------------------------------------------------------------------
# 2) Alias common top-level names to the *same* module objects under src.*
#    This prevents the same file being imported twice under different names
#    (e.g. "watermarking_utils" vs "src.watermarking_utils"), which would
#    split coverage.
# ---------------------------------------------------------------------
def _alias(top_name: str, real_name: str):
    """
    Map a top-level import name to the canonical src.* module.
    Example: _alias("watermarking_utils", "src.watermarking_utils")
    """
    mod = importlib.import_module(real_name)
    sys.modules[top_name] = mod
    return mod

with contextlib.suppress(ModuleNotFoundError):
    _alias("watermarking_utils", "src.watermarking_utils")

with contextlib.suppress(ModuleNotFoundError):
    _alias("wjj_watermark", "src.wjj_watermark")

# src/watermark_JunyiShen/wm_embedfile_v1.py
with contextlib.suppress(ModuleNotFoundError):
    _alias("wm_embedfile_v1", "src.watermark_JunyiShen.wm_embedfile_v1")

# ---------------------------------------------------------------------
# 3) Set default environment variables used by the server (only if absent)
# ---------------------------------------------------------------------
os.environ.setdefault("SECRET_KEY", "test-secret")  # avoid 'SECRET_KEY required'
# A temp storage root (tests can override)
os.environ.setdefault("STORAGE_ROOT", str(ROOT / "tmp_storage"))
# Typical Flask max payload (bytes). If your server reads this, it's available.
os.environ.setdefault("MAX_CONTENT_LENGTH", "16777216")
# If your code has optional RMAP/remote dependencies, you can disable by default.
os.environ.setdefault("DISABLE_RMAP", "1")

# ---------------------------------------------------------------------
# 4) Minimal stub for optional third-party deps (only if missing)
#    Here we create a tiny stub for pikepdf to prevent ImportError in tests.
#    If your tests monkeypatch real behavior, this stub won't get in the way.
# ---------------------------------------------------------------------
try:
    import pikepdf  # noqa: F401
except Exception:
    class _PikePDFDoc:
        def __init__(self, *a, **kw): pass
        def save(self, *a, **kw): pass
        def close(self): pass
    sys.modules["pikepdf"] = types.SimpleNamespace(open=lambda *a, **k: _PikePDFDoc())

# ---------------------------------------------------------------------
# 5) Autouse fixture: keep watermark registry clean between tests
#    Prevent cross-test pollution when tests register/override methods.
# ---------------------------------------------------------------------
@pytest.fixture(autouse=True)
def _reset_watermark_registry():
    try:
        import src.watermarking_utils as wu
    except Exception:
        # Not all test suites import watermarking_utils; that's fine.
        yield
        return

    snapshot = dict(wu.METHODS)
    try:
        yield
    finally:
        wu.METHODS.clear()
        wu.METHODS.update(snapshot)
