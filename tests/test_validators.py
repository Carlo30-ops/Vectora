"""
Tests para el módulo validators
Prueba las funciones de validación de archivos y entradas
"""
import pytest
import os
from pathlib import Path
from utils.validators import (
    validate_file_size,
    validate_pdf_file,
    validate_batch_size,
    format_size
)


class TestValidateFileSize:
    """Tests para validate_file_size"""
    
    @pytest.mark.unit
    def test_validate_file_size_valid(self, sample_pdf):
        """Test: Archivo válido dentro del límite"""
        is_valid, message = validate_file_size(str(sample_pdf), max_mb=100)
        assert is_valid is True
        assert message == ""
    
    @pytest.mark.unit
    def test_validate_file_size_exceeds_limit(self, temp_dir):
        """Test: Archivo que excede el límite"""
        # Crear archivo grande simulado (mock del tamaño)
        large_file = temp_dir / "large.pdf"
        large_file.write_bytes(b'x' * (101 * 1024 * 1024))  # 101 MB
        
        is_valid, message = validate_file_size(str(large_file), max_mb=100)
        assert is_valid is False
        assert "excede el límite" in message.lower()
    
    @pytest.mark.unit
    def test_validate_file_size_nonexistent(self, non_existent_file):
        """Test: Archivo que no existe"""
        is_valid, message = validate_file_size(non_existent_file, max_mb=100)
        assert is_valid is False
        assert "error" in message.lower()
    
    @pytest.mark.unit
    def test_validate_file_size_custom_limit(self, sample_pdf):
        """Test: Límite personalizado"""
        is_valid, message = validate_file_size(str(sample_pdf), max_mb=1)
        # El sample_pdf es pequeño, debería pasar
        assert is_valid is True


class TestValidatePDFFile:
    """Tests para validate_pdf_file"""
    
    @pytest.mark.unit
    def test_validate_pdf_file_valid(self, sample_pdf):
        """Test: PDF válido"""
        is_valid, message = validate_pdf_file(str(sample_pdf))
        assert is_valid is True
    
    @pytest.mark.unit
    def test_validate_pdf_file_nonexistent(self, non_existent_file):
        """Test: Archivo que no existe"""
        is_valid, message = validate_pdf_file(non_existent_file)
        assert is_valid is False
        assert "no existe" in message.lower()
    
    @pytest.mark.unit
    def test_validate_pdf_file_invalid_extension(self, temp_dir):
        """Test: Archivo con extensión incorrecta"""
        txt_file = temp_dir / "test.txt"
        txt_file.write_text("Not a PDF")
        
        is_valid, message = validate_pdf_file(str(txt_file))
        assert is_valid is False
        assert "extensión" in message.lower()
    
    @pytest.mark.unit
    def test_validate_pdf_file_empty(self, temp_dir):
        """Test: PDF vacío (sin páginas)"""
        # Crear PDF vacío
        empty_pdf = temp_dir / "empty.pdf"
        empty_pdf.write_bytes(b'%PDF-1.4\n%%EOF\n')
        
        is_valid, message = validate_pdf_file(str(empty_pdf))
        # PyPDF2 puede lanzar error o considerar vacío
        assert is_valid is False or "vacío" in message.lower()


class TestValidateBatchSize:
    """Tests para validate_batch_size"""
    
    @pytest.mark.unit
    def test_validate_batch_size_valid(self):
        """Test: Tamaño de lote válido"""
        is_valid, message = validate_batch_size(10, max_count=50)
        assert is_valid is True
        assert message == ""
    
    @pytest.mark.unit
    def test_validate_batch_size_exceeds_limit(self):
        """Test: Lote que excede el límite"""
        is_valid, message = validate_batch_size(60, max_count=50)
        assert is_valid is False
        assert "demasiados archivos" in message.lower()
    
    @pytest.mark.unit
    def test_validate_batch_size_at_limit(self):
        """Test: Lote en el límite exacto"""
        is_valid, message = validate_batch_size(50, max_count=50)
        assert is_valid is True
    
    @pytest.mark.unit
    def test_validate_batch_size_custom_limit(self):
        """Test: Límite personalizado"""
        is_valid, message = validate_batch_size(25, max_count=20)
        assert is_valid is False
        assert "20" in message


class TestFormatSize:
    """Tests para format_size"""
    
    @pytest.mark.unit
    def test_format_size_bytes(self):
        """Test: Formato en bytes"""
        result = format_size(500)
        assert "B" in result
        assert "500" in result
    
    @pytest.mark.unit
    def test_format_size_kb(self):
        """Test: Formato en KB"""
        result = format_size(2048)
        assert "KB" in result
    
    @pytest.mark.unit
    def test_format_size_mb(self):
        """Test: Formato en MB"""
        result = format_size(5 * 1024 * 1024)
        assert "MB" in result
    
    @pytest.mark.unit
    def test_format_size_gb(self):
        """Test: Formato en GB"""
        result = format_size(2 * 1024 * 1024 * 1024)
        assert "GB" in result
    
    @pytest.mark.unit
    def test_format_size_zero(self):
        """Test: Tamaño cero"""
        result = format_size(0)
        assert "0.0 B" == result or "0" in result
    
    @pytest.mark.unit
    def test_format_size_rounding(self):
        """Test: Redondeo correcto"""
        # 1.5 MB
        result = format_size(int(1.5 * 1024 * 1024))
        assert "MB" in result
