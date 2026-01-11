"""
Tests para el servicio OCR
Prueba el reconocimiento óptico de caracteres
"""
import pytest
from unittest.mock import MagicMock, patch
from backend.services.ocr_service import OCRService
from tests.conftest import assert_pdf_exists


@pytest.fixture
def ocr_service():
    """Fixture para crear instancia de OCRService"""
    return OCRService()


def test_extract_text_from_image(ocr_service, temp_dir):
    """Test extracción de texto de imagen"""
    image_path = str(temp_dir / "test.png")
    
    # Crear imagen mock
    with patch('PIL.Image.open') as mock_open, \
         patch('pytesseract.image_to_string') as mock_tess:
        mock_img = MagicMock()
        mock_open.return_value = mock_img
        mock_tess.return_value = "Texto extraído"
        
        result = ocr_service.extract_text_from_image(image_path)
        
        assert result == "Texto extraído"
        mock_tess.assert_called_once()


def test_ocr_processing(ocr_service, sample_pdf, output_path):
    """Test flujo OCR (Mock de pytesseract y pdf2image)"""
    
    # Mockear métodos internos o librerías externas
    with patch('backend.services.ocr_service.convert_from_path') as mock_convert, \
         patch('backend.services.ocr_service.pytesseract.image_to_pdf_or_hocr') as mock_tess:
        
        # Simular imágenes convertidas
        mock_img1 = MagicMock()
        mock_img2 = MagicMock()
        mock_convert.return_value = [mock_img1, mock_img2]
        
        # Simular retorno de PDF bytes
        mock_tess.return_value = b'%PDF-1.4 fake pdf content'
        
        result = ocr_service.pdf_to_searchable_pdf(
            str(sample_pdf),
            output_path,
            language='spa+eng',
            dpi=300
        )
        
        assert result['success'] is True
        assert 'output_path' in result
        assert result['total_pages'] == 2
        assert 'total_characters' in result


def test_ocr_with_callback(ocr_service, sample_pdf, output_path):
    """Test que el callback de progreso se llame"""
    mock_callback = MagicMock()
    
    with patch('backend.services.ocr_service.convert_from_path') as mock_convert, \
         patch('backend.services.ocr_service.pytesseract.image_to_pdf_or_hocr') as mock_tess:
        
        mock_img = MagicMock()
        mock_convert.return_value = [mock_img]
        mock_tess.return_value = b'%PDF-1.4 fake pdf content'
        
        ocr_service.pdf_to_searchable_pdf(
            str(sample_pdf),
            output_path,
            progress_callback=mock_callback
        )
        
        # El callback debería llamarse
        assert mock_callback.called
