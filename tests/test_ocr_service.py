import pytest
from unittest.mock import MagicMock, patch
from backend.services.ocr_service import OCRService

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def ocr_service(mock_logger):
    return OCRService(logger=mock_logger)

def test_ocr_processing(ocr_service, sample_pdf, output_path):
    """Test flujo OCR (Mock de pytesseract y pdf2image)"""
    
    # Mockear métodos internos o librerías externas
    with patch('backend.services.ocr_service.convert_from_path') as mock_convert, \
         patch('backend.services.ocr_service.pytesseract.image_to_pdf_or_hocr') as mock_tess, \
         patch('backend.services.ocr_service.PdfMerger') as MockMerger:
             
        # Simular 2 páginas convertidas a imagen
        mock_convert.return_value = [MagicMock(), MagicMock()] 
        
        # Simular resultado de pytesseract (bytes de PDF)
        mock_tess.return_value = b"%PDF-1.4..."
        
        result = ocr_service.pdf_to_searchable_pdf(
            str(sample_pdf), 
            output_path, 
            language='spa'
        )
        
        assert result['success'] is True
        assert result['total_pages'] == 2
        # Verificar que se llamó a tesseract por cada página
        assert mock_tess.call_count == 2
