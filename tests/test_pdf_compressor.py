"""
Tests para el servicio PDFCompressor
Prueba la compresión de archivos PDF
"""
import pytest
from unittest.mock import MagicMock, patch
from backend.services.pdf_compressor import PDFCompressor
from tests.conftest import assert_pdf_exists


class TestPDFCompressor:
    """Suite de tests para PDFCompressor"""
    
    @pytest.fixture
    def compressor(self):
        """Fixture para crear instancia de PDFCompressor"""
        return PDFCompressor()
    
    @pytest.mark.unit
    def test_compress_pdf_success(self, compressor, sample_pdf, output_path):
        """Prueba compresión exitosa (Mockeado)"""
        
        # Mockear pikepdf.open y remove_unreferenced_resources/save
        with patch('pikepdf.open') as mock_open:
            mock_pdf = MagicMock()
            mock_pdf.pages = [MagicMock()] * 3  # 3 páginas
            mock_open.return_value.__enter__.return_value = mock_pdf
            
            result = compressor.compress_pdf(
                str(sample_pdf),
                output_path,
                quality_level='medium'
            )
            
            assert result['success'] is True
            assert 'output_path' in result
            mock_pdf.save.assert_called_once()
    
    @pytest.mark.unit
    def test_compress_pdf_invalid_quality(self, compressor, sample_pdf, output_path):
        """Prueba que se lance error con nivel de compresión inválido"""
        with pytest.raises(ValueError):
            compressor.compress_pdf(
                str(sample_pdf),
                output_path,
                quality_level='invalid'
            )
    
    @pytest.mark.unit
    def test_compress_callback(self, compressor, sample_pdf, output_path):
        """Prueba que se llame al callback de progreso"""
        mock_callback = MagicMock()

        with patch('pikepdf.open') as mock_open:
            mock_pdf = MagicMock()
            mock_pdf.pages = [MagicMock()] * 2  # 2 páginas
            mock_open.return_value.__enter__.return_value = mock_pdf
            
            compressor.compress_pdf(
                str(sample_pdf),
                output_path,
                quality_level='high',
                progress_callback=mock_callback
            )
            
            # El callback debería llamarse al menos una vez
            assert mock_callback.called
