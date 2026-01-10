import pytest
from unittest.mock import MagicMock, patch
from backend.services.pdf_compressor import PDFCompressor

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def compressor(mock_logger):
    return PDFCompressor(logger=mock_logger)

def test_compress_pdf_success(compressor, sample_pdf, output_path):
    """Prueba compresión exitosa (Mockeado)"""
    
    # Mockear pikepdf.open y remove_unreferenced_resources/save
    with patch('pikepdf.open') as mock_open:
        mock_pdf = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_pdf
        
        result = compressor.compress_pdf(
            str(sample_pdf), 
            output_path, 
            quality='medium'
        )
        
        # Verificar llamadas
        mock_open.assert_called_once_with(str(sample_pdf))
        mock_pdf.remove_unreferenced_resources.assert_called_once()
        mock_pdf.save.assert_called_once()
        
        assert result['success'] is True
        assert result['output_path'] == output_path

def test_compress_pdf_invalid_quality(compressor, sample_pdf, output_path):
    """Prueba que falle con calidad inválida"""
    with pytest.raises(Exception):
        compressor.compress_pdf(str(sample_pdf), output_path, quality='invalid_level')

def test_compress_callback(compressor, sample_pdf, output_path):
    """Prueba que se llame al callback de progreso"""
    mock_callback = MagicMock()
    
    with patch('pikepdf.open') as mock_open:
        mock_pdf = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_pdf
        
        compressor.compress_pdf(
            str(sample_pdf), 
            output_path, 
            quality='high',
            progress_callback=mock_callback
        )
        
        # Debe llamar al menos una vez al callback
        assert mock_callback.call_count > 0
