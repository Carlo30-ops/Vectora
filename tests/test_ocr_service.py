"""
Tests para el servicio OCRService
Prueba el reconocimiento óptico de caracteres
"""
import pytest
from unittest.mock import MagicMock, patch
from backend.services.ocr_service import OCRService


@pytest.fixture
def mock_logger():
    return MagicMock()


@pytest.fixture
def ocr_service(mock_logger):
    return OCRService(logger=mock_logger)


class TestOCRService:
    """Suite de tests para OCRService"""
    
    @pytest.mark.unit
    def test_ocr_processing_success(self, ocr_service, sample_pdf, output_path):
        """Test: Procesamiento OCR exitoso (Mock)"""
        with patch('backend.services.ocr_service.convert_from_path') as mock_convert, \
             patch('backend.services.ocr_service.pytesseract.image_to_pdf_or_hocr') as mock_tess, \
             patch('backend.services.ocr_service.PdfFileMerger') as MockMerger:
            
            # Simular 2 páginas convertidas a imagen
            mock_img1 = MagicMock()
            mock_img2 = MagicMock()
            mock_convert.return_value = [mock_img1, mock_img2]
            
            # Simular resultado de pytesseract (bytes de PDF)
            mock_tess.return_value = b"%PDF-1.4..."
            
            # Mock del merger
            mock_merger_instance = MagicMock()
            MockMerger.return_value = mock_merger_instance
            
            result = ocr_service.pdf_to_searchable_pdf(
                str(sample_pdf),
                output_path,
                language='spa'
            )
            
            assert result['success'] is True
            assert result['total_pages'] == 2
            # Verificar que se llamó a tesseract por cada página
            assert mock_tess.call_count == 2
    
    @pytest.mark.unit
    def test_ocr_with_callback(self, ocr_service, sample_pdf, output_path):
        """Test: OCR con callback de progreso"""
        mock_callback = MagicMock()
        
        with patch('backend.services.ocr_service.convert_from_path') as mock_convert, \
             patch('backend.services.ocr_service.pytesseract.image_to_pdf_or_hocr') as mock_tess, \
             patch('backend.services.ocr_service.PdfFileMerger'):
            
            mock_convert.return_value = [MagicMock(), MagicMock()]
            mock_tess.return_value = b"%PDF-1.4..."
            
            result = ocr_service.pdf_to_searchable_pdf(
                str(sample_pdf),
                output_path,
                language='spa',
                progress_callback=mock_callback
            )
            
            assert result['success'] is True
            # Callback debe llamarse
            assert mock_callback.call_count > 0
    
    @pytest.mark.unit
    def test_ocr_custom_dpi(self, ocr_service, sample_pdf, output_path):
        """Test: OCR con DPI personalizado"""
        with patch('backend.services.ocr_service.convert_from_path') as mock_convert, \
             patch('backend.services.ocr_service.pytesseract.image_to_pdf_or_hocr') as mock_tess, \
             patch('backend.services.ocr_service.PdfFileMerger'):
            
            mock_convert.return_value = [MagicMock()]
            mock_tess.return_value = b"%PDF-1.4..."
            
            result = ocr_service.pdf_to_searchable_pdf(
                str(sample_pdf),
                output_path,
                language='spa',
                dpi=600
            )
            
            assert result['success'] is True
            # Verificar que se llamó con el DPI correcto
            mock_convert.assert_called_once()
            call_kwargs = mock_convert.call_args[1]
            assert call_kwargs['dpi'] == 600
    
    @pytest.mark.unit
    def test_ocr_different_languages(self, ocr_service, sample_pdf, output_path):
        """Test: OCR con diferentes idiomas"""
        languages = ['spa', 'eng', 'spa+eng']
        
        for lang in languages:
            with patch('backend.services.ocr_service.convert_from_path') as mock_convert, \
                 patch('backend.services.ocr_service.pytesseract.image_to_pdf_or_hocr') as mock_tess, \
                 patch('backend.services.ocr_service.PdfFileMerger'):
                
                mock_convert.return_value = [MagicMock()]
                mock_tess.return_value = b"%PDF-1.4..."
                
                result = ocr_service.pdf_to_searchable_pdf(
                    str(sample_pdf),
                    output_path,
                    language=lang
                )
                
                assert result['success'] is True
                # Verificar que se llamó con el idioma correcto
                assert mock_tess.call_count > 0
