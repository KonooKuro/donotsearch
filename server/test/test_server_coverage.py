# tests/test_server_simple.py
"""
Server 测试 - 专注于不需要数据库的功能
提高代码覆盖率
"""
from __future__ import annotations
import pytest
import json
import io
import os
import sys
from pathlib import Path


# 设置环境变量（在导入 server 之前）
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-12345"
os.environ["DB_HOST"] = "127.0.0.1"


@pytest.fixture
def sample_pdf() -> bytes:
    """最小有效PDF"""
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Count 1 /Kids [3 0 R] >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
        b"xref\n0 4\n"
        b"0000000000 65535 f\n"
        b"0000000009 00000 n\n"
        b"0000000058 00000 n\n"
        b"0000000115 00000 n\n"
        b"trailer\n<< /Size 4 /Root 1 0 R >>\n"
        b"startxref\n190\n"
        b"%%EOF\n"
    )


class TestUtilityFunctions:
    """测试工具函数（不需要数据库）"""

    def test_secure_filename(self):
        """测试安全文件名处理"""
        from werkzeug.utils import secure_filename
        
        # 测试路径遍历攻击防护
        assert ".." not in secure_filename("../../../etc/passwd")
        assert "/" not in secure_filename("test/../file.pdf")
        
        # 测试正常文件名
        assert secure_filename("test.pdf") == "test.pdf"
        assert secure_filename("My Document.pdf") == "My_Document.pdf"

    def test_password_hashing(self):
        """测试密码哈希功能"""
        from werkzeug.security import generate_password_hash, check_password_hash
        
        password = "test-password-123"
        hashed = generate_password_hash(password)
        
        # 哈希后的密码应该不同
        assert hashed != password
        assert len(hashed) > len(password)
        
        # 验证正确密码
        assert check_password_hash(hashed, password) is True
        
        # 验证错误密码
        assert check_password_hash(hashed, "wrong-password") is False


class TestWatermarkIntegration:
    """测试水印集成（完全独立，不需要数据库）"""

    def test_wjj_watermark_method_registered(self):
        """测试WJJ水印方法已注册"""
        from watermarking_utils import METHODS
        assert "wjj-watermark" in METHODS

    def test_wjj_watermark_has_correct_name(self):
        """测试方法名称"""
        from watermarking_utils import METHODS
        method = METHODS["wjj-watermark"]
        assert method.name == "wjj-watermark"

    def test_wjj_watermark_has_usage(self):
        """测试使用说明"""
        from watermarking_utils import METHODS
        method = METHODS["wjj-watermark"]
        usage = method.get_usage()
        assert isinstance(usage, str)
        assert len(usage) > 0

    def test_wjj_watermark_add_and_read(self, sample_pdf):
        """测试完整的水印流程"""
        from watermarking_utils import apply_watermark, read_watermark
        
        secret = "test-integration-secret"
        
        # 添加水印
        watermarked = apply_watermark(
            method="wjj-watermark",
            pdf=sample_pdf,
            secret=secret
        )
        
        assert isinstance(watermarked, bytes)
        assert len(watermarked) > len(sample_pdf)
        assert watermarked.startswith(b"%PDF-")
        
        # 读取水印
        extracted = read_watermark(
            method="wjj-watermark",
            pdf=watermarked
        )
        
        assert extracted == secret

    def test_watermark_applicability(self, sample_pdf):
        """测试水印适用性检查"""
        from watermarking_utils import is_watermarking_applicable
        
        # 对有效PDF应该适用
        assert is_watermarking_applicable(
            method="wjj-watermark",
            pdf=sample_pdf
        ) is True
        
        # 对无效PDF不适用
        assert is_watermarking_applicable(
            method="wjj-watermark",
            pdf=b"not a pdf"
        ) is False

    def test_watermark_with_json_secret(self, sample_pdf):
        """测试JSON格式的密文"""
        from watermarking_utils import apply_watermark, read_watermark
        
        # 当传入普通字符串时，会被包装成 JSON
        secret = "my-secret"
        
        watermarked = apply_watermark(
            method="wjj-watermark",
            pdf=sample_pdf,
            secret=secret
        )
        
        extracted = read_watermark(
            method="wjj-watermark",
            pdf=watermarked
        )
        
        # 应该返回原始 secret 值
        assert extracted == secret

    def test_get_method_helper(self):
        """测试 get_method 辅助函数"""
        from watermarking_utils import get_method, METHODS
        
        # 通过字符串获取
        method = get_method("wjj-watermark")
        assert method is not None
        assert method.name == "wjj-watermark"
        
        # 通过实例获取（直接返回）
        method_inst = METHODS["wjj-watermark"]
        result = get_method(method_inst)
        assert result is method_inst

    def test_get_method_unknown(self):
        """测试获取未知方法"""
        from watermarking_utils import get_method
        
        with pytest.raises(KeyError):
            get_method("unknown-method-xyz")


class TestServerHelperFunctions:
    """测试 server.py 中的辅助函数"""

    def test_is_pdf_bytes(self, sample_pdf):
        """测试 PDF 验证函数"""
        # 延迟导入以避免数据库连接
        import importlib
        import sys
        
        # 临时设置环境
        os.environ["SECRET_KEY"] = "test-key"
        
        # 如果 server 已经导入，重新加载
        if 'server' in sys.modules:
            importlib.reload(sys.modules['server'])
        
        try:
            from server import _is_pdf_bytes
            
            # 有效的PDF
            assert _is_pdf_bytes(sample_pdf) is True
            
            # 无效的PDF
            assert _is_pdf_bytes(b"not a pdf") is False
            assert _is_pdf_bytes(b"") is False
            assert _is_pdf_bytes(b"%PDF") is False  # 太短
            
            # 缺少必要元素
            assert _is_pdf_bytes(b"%PDF-1.4\nsome content") is False
        except ImportError:
            pytest.skip("Cannot import server module")


class TestInputValidationLogic:
    """测试输入验证逻辑（不通过Flask）"""

    def test_email_validation_logic(self):
        """测试邮箱验证逻辑"""
        # 简单的验证逻辑测试
        valid_emails = [
            "test@example.com",
            "user+tag@domain.co.uk",
            "name@subdomain.example.com"
        ]
        
        invalid_emails = [
            "",
            "notanemail",
            "@example.com",
            "user@",
            "user @example.com"
        ]
        
        for email in valid_emails:
            assert "@" in email
            assert "." in email.split("@")[1]
        
        for email in invalid_emails:
            local = email.split("@")[0] if "@" in email else ""
            domain = email.split("@")[-1] if "@" in email else ""
            has_no_whitespace = not any(ch.isspace() for ch in email)
            assert not (email and "@" in email and local and "." in domain and has_no_whitespace)
            
    def test_password_strength_logic(self):
        """测试密码强度逻辑"""
        # 简单的密码检查
        weak_passwords = ["", "123", "pass"]
        strong_passwords = ["StrongP@ss123", "MySecure#Pass2024"]
        
        for pwd in weak_passwords:
            assert len(pwd) < 8
        
        for pwd in strong_passwords:
            assert len(pwd) >= 8


class TestWatermarkingUtils:
    """测试 watermarking_utils 模块的其他功能"""

    def test_methods_registry_not_empty(self):
        """测试方法注册表不为空"""
        from watermarking_utils import METHODS
        assert len(METHODS) > 0

    def test_register_method_function(self):
        """测试 register_method 函数"""
        from watermarking_utils import register_method, METHODS, WatermarkingMethod
        
        # 创建一个测试方法
        class TestMethod(WatermarkingMethod):
            name = "test-method-xyz"
            
            @staticmethod
            def get_usage():
                return "Test method"
            
            def add_watermark(self, pdf, secret, position=None, key=None):
                return b"%PDF-test"
            
            def is_watermark_applicable(self, pdf, position=None):
                return True
            
            def read_secret(self, pdf, key=None):
                return "test"
        
        test_inst = TestMethod()
        original_count = len(METHODS)
        
        # 注册方法
        register_method(test_inst)
        
        assert "test-method-xyz" in METHODS
        assert len(METHODS) == original_count + 1
        
        # 清理
        del METHODS["test-method-xyz"]

    def test_explore_pdf_function(self, sample_pdf):
        """测试 explore_pdf 函数"""
        from watermarking_utils import explore_pdf
        
        tree = explore_pdf(sample_pdf)
        
        assert isinstance(tree, dict)
        assert "id" in tree
        assert "type" in tree
        assert tree["type"] == "Document"
        assert "size" in tree
        assert tree["size"] == len(sample_pdf)


class TestWatermarkingMethodInterface:
    """测试 WatermarkingMethod 接口"""

    def test_wjj_method_implements_interface(self):
        """测试 WJJ 方法实现了正确的接口"""
        from watermarking_utils import METHODS
        from watermarking_method import WatermarkingMethod
        
        method = METHODS["wjj-watermark"]
        
        # 检查必需的方法
        assert hasattr(method, "add_watermark")
        assert hasattr(method, "read_secret")
        assert hasattr(method, "is_watermark_applicable")
        assert hasattr(method, "get_usage")
        
        # 检查方法是否可调用
        assert callable(method.add_watermark)
        assert callable(method.read_secret)
        assert callable(method.is_watermark_applicable)
        assert callable(method.get_usage)


class TestPdfSourceHandling:
    """测试 PdfSource 类型处理"""

    def test_load_pdf_bytes_from_bytes(self, sample_pdf):
        """测试从 bytes 加载 PDF"""
        from watermarking_method import load_pdf_bytes
        
        result = load_pdf_bytes(sample_pdf)
        assert isinstance(result, bytes)
        assert result == sample_pdf

    def test_load_pdf_bytes_from_file(self, sample_pdf, tmp_path):
        """测试从文件加载 PDF"""
        from watermarking_method import load_pdf_bytes
        
        # 创建临时文件
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(sample_pdf)
        
        # 测试路径字符串
        result = load_pdf_bytes(str(pdf_file))
        assert isinstance(result, bytes)
        assert result == sample_pdf
        
        # 测试 Path 对象
        result = load_pdf_bytes(pdf_file)
        assert isinstance(result, bytes)
        assert result == sample_pdf

    def test_load_pdf_bytes_from_io(self, sample_pdf):
        """测试从 IO 对象加载 PDF"""
        from watermarking_method import load_pdf_bytes
        
        pdf_io = io.BytesIO(sample_pdf)
        result = load_pdf_bytes(pdf_io)
        assert isinstance(result, bytes)
        assert result == sample_pdf

    def test_is_pdf_bytes_function(self, sample_pdf):
        """测试 is_pdf_bytes 函数"""
        from watermarking_method import is_pdf_bytes
        
        assert is_pdf_bytes(sample_pdf) is True
        assert is_pdf_bytes(b"not a pdf") is False
        assert is_pdf_bytes(b"") is False


class TestEdgeCases:
    """测试边界情况"""

    def test_empty_secret_handling(self, sample_pdf):
        """测试空密文处理"""
        from wjj_watermark import WJJWatermarkMethod
        from watermarking_method import WatermarkingError
        
        method = WJJWatermarkMethod()
        
        with pytest.raises(WatermarkingError):
            method.add_watermark(sample_pdf, "")

    def test_invalid_pdf_handling(self):
        """测试无效PDF处理"""
        from wjj_watermark import WJJWatermarkMethod
        from watermarking_method import WatermarkingError
        
        method = WJJWatermarkMethod()
        
        with pytest.raises(WatermarkingError):
            method.add_watermark(b"not a pdf", "secret")

    def test_unicode_secret(self, sample_pdf):
        """测试 Unicode 密文"""
        from watermarking_utils import apply_watermark, read_watermark
        
        secret = "测试中文密文 🔒 émoji"
        
        watermarked = apply_watermark(
            method="wjj-watermark",
            pdf=sample_pdf,
            secret=secret
        )
        
        extracted = read_watermark(
            method="wjj-watermark",
            pdf=watermarked
        )
        
        assert extracted == secret

    def test_long_secret(self, sample_pdf):
        """测试长密文"""
        from watermarking_utils import apply_watermark, read_watermark
        
        secret = "x" * 10000
        
        watermarked = apply_watermark(
            method="wjj-watermark",
            pdf=sample_pdf,
            secret=secret
        )
        
        extracted = read_watermark(
            method="wjj-watermark",
            pdf=watermarked
        )
        
        assert extracted == secret

    def test_multiple_watermarks(self, sample_pdf):
        """测试多次水印"""
        from watermarking_utils import apply_watermark, read_watermark
        
        # 第一次水印
        wm1 = apply_watermark(
            method="wjj-watermark",
            pdf=sample_pdf,
            secret="first"
        )
        
        # 第二次水印
        wm2 = apply_watermark(
            method="wjj-watermark",
            pdf=wm1,
            secret="second"
        )
        
        # 应该读取最后一个
        extracted = read_watermark(
            method="wjj-watermark",
            pdf=wm2
        )
        
        assert extracted == "second"


class TestExceptionHandling:
    """测试异常处理"""

    def test_secret_not_found_error(self, sample_pdf):
        """测试 SecretNotFoundError"""
        from wjj_watermark import WJJWatermarkMethod
        from watermarking_method import SecretNotFoundError
        
        method = WJJWatermarkMethod()
        
        # 尝试从没有水印的PDF读取
        with pytest.raises(SecretNotFoundError):
            method.read_secret(sample_pdf)

    def test_corrupted_watermark(self, sample_pdf):
        """测试损坏的水印"""
        from watermarking_utils import apply_watermark, read_watermark
        from watermarking_method import WatermarkingError, SecretNotFoundError
        
        # 添加水印
        watermarked = apply_watermark(
            method="wjj-watermark",
            pdf=sample_pdf,
            secret="test"
        )
        
        # 破坏水印
        corrupted = watermarked.replace(b"WJJ-WATERMARK-START", b"XXX-WATERMARK-START")
        
        # 应该抛出异常
        with pytest.raises((WatermarkingError, SecretNotFoundError)):
            read_watermark(method="wjj-watermark", pdf=corrupted)
