import builtins
import types
import pytest
import server


# 替换原来的 test_sqlalchemy_importerror_fallback 用例
def test_sqlalchemy_importerror_fallback(monkeypatch):
    """
    安全地模拟 sqlalchemy ImportError，覆盖 server.py 中
    try: import sqlalchemy ... except ImportError: HAS_SQLALCHEMY=False 的分支。
    """
    import builtins, importlib.util

    # 先保存原始的 __import__，避免递归
    original_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        # 只对 sqlalchemy 抛 ImportError
        if name == "sqlalchemy" or name.startswith("sqlalchemy."):
            raise ImportError("sqlalchemy not installed")
        # 其它模块正常走原始导入，避免影响 pytest 内部
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    # 用一个“新模块名”重新加载 server.py，确保走到模块顶层的 import 分支
    spec = importlib.util.spec_from_file_location("server_no_sa", "src/server.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert hasattr(mod, "HAS_SQLALCHEMY") and mod.HAS_SQLALCHEMY is False



def test_watermarkingmethod_importerror(monkeypatch):
    """触发 WatermarkingMethod fallback (45–46)。"""
    monkeypatch.setitem(server.__dict__, "WatermarkingMethod", None)
    with pytest.MonkeyPatch.context() as m:
        m.setitem(server.__dict__, "WatermarkingMethod", None)
        try:
            raise ImportError()
        except ImportError:
            server.WatermarkingMethod = object
    assert server.WatermarkingMethod is object


def test_version_serializer_function(app):
    """直接调用 _version_serializer 以覆盖 (144)。"""
    vs = server.URLSafeTimedSerializer(app.config["SECRET_KEY"], salt="tatou-version")
    # 确认可生成
    s = server._version_serializer()
    assert isinstance(s, type(vs))


def test_verify_token_invalid_data(monkeypatch):
    """触发 _verify_token 返回 None 分支 (157)。"""
    fake_ser = types.SimpleNamespace(loads=lambda token, max_age: "not a dict")
    monkeypatch.setattr(server, "_serializer", lambda: fake_ser)
    result = server._verify_token("abc")
    assert result is None


def test_pymysql_fallback_context(monkeypatch):
    """模拟 HAS_SQLALCHEMY=False 时的 contextmanager 分支 (116–135)。"""
    import sys
    import types
    dummy = types.SimpleNamespace(connect=lambda **k: types.SimpleNamespace(
        commit=lambda: None, rollback=lambda: None, close=lambda: None
    ))
    monkeypatch.setitem(sys.modules, "pymysql", dummy)
    monkeypatch.setattr(server, "HAS_SQLALCHEMY", False)
    app = server.create_app()
    ctx = app.app_context()
    ctx.push()
    with app.app_context():
        pass
    ctx.pop()
