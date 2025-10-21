import io
import json
import builtins
import types
import pytest
import sys
from src import watermarking_cli as cli

# -------- 基础读写函数 --------

def test_read_text_from_file(tmp_path):
    f = tmp_path / "x.txt"
    f.write_text("hello\n")
    assert cli._read_text_from_file(str(f)) == "hello\n"


def test_read_text_from_stdin(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("data"))
    assert cli._read_text_from_stdin() == "data"

def test_read_text_from_stdin_empty(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    with pytest.raises(ValueError):
        cli._read_text_from_stdin()


# -------- secret/key 解析逻辑 --------

def test_resolve_secret_variants(tmp_path, monkeypatch):
    f = tmp_path / "s.txt"
    f.write_text("abc")
    ns = types.SimpleNamespace(secret=None, secret_file=str(f), secret_stdin=False)
    assert cli._resolve_secret(ns) == "abc"

    ns2 = types.SimpleNamespace(secret="xyz", secret_file=None, secret_stdin=False)
    assert cli._resolve_secret(ns2) == "xyz"

    ns3 = types.SimpleNamespace(secret=None, secret_file=None, secret_stdin=True)
    monkeypatch.setattr(sys, "stdin", io.StringIO("stdinsec"))
    assert cli._resolve_secret(ns3) == "stdinsec"

    ns4 = types.SimpleNamespace(secret=None, secret_file=None, secret_stdin=False)
    monkeypatch.setattr(cli.getpass, "getpass", lambda prompt="": "askpass")
    assert cli._resolve_secret(ns4) == "askpass"


def test_resolve_key_variants(tmp_path, monkeypatch):
    f = tmp_path / "k.txt"
    f.write_text("keyfile")
    ns = types.SimpleNamespace(key=None, key_file=str(f), key_stdin=False, key_prompt=False)
    assert cli._resolve_key(ns) == "keyfile"

    ns2 = types.SimpleNamespace(key="direct", key_file=None, key_stdin=False, key_prompt=False)
    assert cli._resolve_key(ns2) == "direct"

    ns3 = types.SimpleNamespace(key=None, key_file=None, key_stdin=True, key_prompt=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO("stdin-key\n"))
    assert cli._resolve_key(ns3) == "stdin-key"

    ns4 = types.SimpleNamespace(key=None, key_file=None, key_stdin=False, key_prompt=True)
    monkeypatch.setattr(cli.getpass, "getpass", lambda prompt="": "promptkey")
    assert cli._resolve_key(ns4) == "promptkey"

    ns5 = types.SimpleNamespace(key=None, key_file=None, key_stdin=False, key_prompt=False)
    assert cli._resolve_key(ns5) == ""


# -------- 各命令 --------

def test_cmd_methods(monkeypatch, capsys):
    monkeypatch.setattr(cli, "METHODS", {"m1": object(), "m2": object()})
    assert cli.cmd_methods(types.SimpleNamespace()) == 0
    out = capsys.readouterr().out
    assert "m1" in out and "m2" in out


def test_cmd_explore_write_file(tmp_path):
    out_json = tmp_path / "out.json"
    def fake_explore(path): return {"ok": True}
    cli.explore_pdf = fake_explore
    ns = types.SimpleNamespace(input="in.pdf", out=str(out_json))
    assert cli.cmd_explore(ns) == 0
    assert json.loads(out_json.read_text()) == {"ok": True}

def test_cmd_explore_stdout(monkeypatch, capsys):
    cli.explore_pdf = lambda path: {"pdf": path}
    ns = types.SimpleNamespace(input="in.pdf", out=None)
    assert cli.cmd_explore(ns) == 0
    out = capsys.readouterr().out
    assert "in.pdf" in out


def test_cmd_embed_success(tmp_path, monkeypatch, capsys):
    fake_pdf = tmp_path / "fake.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4")

    def fake_apply(**kw): return b"%PDF-1.4 watermarked"
    monkeypatch.setattr(cli, "apply_watermark", fake_apply)
    monkeypatch.setattr(cli, "is_watermarking_applicable", lambda **kw: True)
    ns = types.SimpleNamespace(
        input=str(fake_pdf),
        output=str(tmp_path / "out.pdf"),
        method="stub",
        position=None,
        secret="S",
        secret_file=None,
        secret_stdin=False,
        key=None,
        key_file=None,
        key_stdin=False,
        key_prompt=False
    )
    assert cli.cmd_embed(ns) == 0
    assert "Wrote" in capsys.readouterr().out
    assert (tmp_path / "out.pdf").exists()

def test_cmd_embed_not_applicable(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(cli, "is_watermarking_applicable", lambda **kw: False)
    ns = types.SimpleNamespace(
        input="i.pdf", output="o.pdf", method="m", position="p",
        secret="S", secret_file=None, secret_stdin=False,
        key=None, key_file=None, key_stdin=False, key_prompt=False
    )
    assert cli.cmd_embed(ns) == 5
    assert "not applicable" in capsys.readouterr().out


def test_cmd_extract_write_file(tmp_path, monkeypatch, capsys):
    fake_pdf = tmp_path / "w.pdf"
    fake_pdf.write_bytes(b"data")
    monkeypatch.setattr(cli, "read_watermark", lambda **kw: "SECRET")
    ns = types.SimpleNamespace(input=str(fake_pdf), method="m", out=str(tmp_path / "secret.txt"),
                               key=None, key_file=None, key_prompt=False, key_stdin=False)
    assert cli.cmd_extract(ns) == 0
    out = capsys.readouterr().out
    assert "Wrote secret" in out
    assert "SECRET" in (tmp_path / "secret.txt").read_text()

def test_cmd_extract_stdout(monkeypatch, capsys):
    monkeypatch.setattr(cli, "read_watermark", lambda **kw: "HELLO")
    ns = types.SimpleNamespace(input="i.pdf", method="m", out=None,
                               key=None, key_file=None, key_prompt=False, key_stdin=False)
    assert cli.cmd_extract(ns) == 0
    assert "HELLO" in capsys.readouterr().out


# -------- main() 错误捕获分支 --------

@pytest.mark.parametrize(
    "exc,code,msg",
    [
        (FileNotFoundError("no file"), 2, "error:"),
        (ValueError("bad val"), 2, "error:"),
        (cli.SecretNotFoundError("x"), 3, "secret not found"),
        (cli.InvalidKeyError("x"), 4, "invalid key"),
        (cli.WatermarkingError("x"), 5, "watermarking error"),
    ],
)
def test_main_error_branches(monkeypatch, capsys, exc, code, msg):
    def fake_func(_args): raise exc
    parser = cli.build_parser()
    args = parser.parse_args(["methods"])
    args.func = fake_func
    monkeypatch.setattr(cli, "build_parser", lambda : parser)
    ret = cli.main(["methods"])
    out = capsys.readouterr().out + capsys.readouterr().err
    assert ret == code
    assert msg.split()[0] in out


def test_main_success(monkeypatch):
    parser = cli.build_parser()
    args = parser.parse_args(["methods"])
    monkeypatch.setattr(cli, "build_parser", lambda: parser)
    args.func = lambda _args: 0
    assert cli.main(["methods"]) == 0
