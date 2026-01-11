"""
Tests para el servicio PDFConverter
Prueba conversiones entre PDF, Word e Imágenes
"""
import pytest
from unittest.mock import MagicMock, patch
from backend.services.pdf_converter import PDFConverter
from tests.conftest import assert_pdf_exists


class TestPDFConverter:
    """Suite de tests para PDFConverter"""
    
    @pytest.fixture
    def converter(self):
        """Fixture para crear instancia de PDFConverter"""
        return PDFConverter()
    
    @pytest.mark.unit
    def test_pdf_to_word_success(self, converter, sample_pdf, output_path):
        """Test conversión PDF a Word (Mock pdf2docx)"""
        output_path = output_path.replace('.pdf', '.docx')
        
        with patch('pdf2docx.Converter') as MockConverter:
            mock_conv = MagicMock()
            MockConverter.return_value = mock_conv
            
            result = converter.pdf_to_word(str(sample_pdf), output_path)
            
            assert result['success'] is True
            assert 'output_path' in result
            mock_conv.convert.assert_called_once()
            mock_conv.close.assert_called_once()
    
    @pytest.mark.unit
    def test_pdf_to_images(self, converter, sample_pdf, temp_dir):
        """Test conversión PDF a imágenes (Mock pdf2image)"""
        output_dir = str(temp_dir)

        with patch('backend.services.pdf_converter.convert_from_path') as mock_convert:
            # Simular retorno de lista de imágenes PIL
            mock_img = MagicMock()
            mock_convert.return_value = [mock_img, mock_img] # 2 páginas

            result = converter.pdf_to_images(str(sample_pdf), output_dir)

            assert result['success'] is True
            assert 'output_files' in result
            assert len(result['output_files']) == 2
            assert result['total_images'] == 2
    
    @pytest.mark.unit
    def test_images_to_pdf(self, converter, temp_dir, output_path):
        """Test crear PDF desde imágenes (Mock PIL)"""
        img_list = ["img1.png", "img2.jpg"]

        with patch('PIL.Image.open') as mock_open:
            mock_img_obj = MagicMock()
            mock_img_obj.convert.return_value = mock_img_obj
            mock_open.return_value = mock_img_obj

            result = converter.images_to_pdf(img_list, output_path)

            assert result['success'] is True
            assert 'output_path' in result
            assert result['total_images'] == 2
