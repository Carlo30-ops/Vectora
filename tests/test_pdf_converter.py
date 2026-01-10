import pytest
from unittest.mock import MagicMock, patch
from backend.services.pdf_converter import PDFConverter

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def converter(mock_logger):
    return PDFConverter(logger=mock_logger)

def test_pdf_to_images(converter, sample_pdf, temp_dir):
    """Test conversión PDF a imágenes (Mock pdf2image)"""
    output_dir = str(temp_dir)
    
    with patch('backend.services.pdf_converter.convert_from_path') as mock_convert:
        # Simular retorno de lista de imágenes PIL
        mock_img = MagicMock()
        mock_convert.return_value = [mock_img, mock_img] # 2 páginas
        
        result = converter.pdf_to_images(str(sample_pdf), output_dir)
        
        assert result['success'] is True
        assert result['page_count'] == 2
        # Verifica que se guardaron 2 imágenes
        assert mock_img.save.call_count == 2

def test_images_to_pdf(converter, temp_dir, output_path):
    """Test crear PDF desde imágenes (Mock PIL)"""
    img_list = ["img1.png", "img2.jpg"]
    
    with patch('PIL.Image.open') as mock_open:
        mock_img_obj = MagicMock()
        mock_img_obj.convert.return_value = mock_img_obj 
        mock_open.return_value = mock_img_obj
        
        result = converter.images_to_pdf(img_list, output_path)
        
        assert result['success'] is True
        assert result['image_count'] == 2
        assert mock_img_obj.save.called

def test_pdf_to_word_success(converter, sample_pdf, temp_dir):
    """Test conversión PDF a Word (Mock Converter)"""
    output_docx = str(temp_dir / "output.docx")
    
    # Mockear la clase Converter de pdf2docx que se instancia dentro
    with patch('backend.services.pdf_converter.Converter') as MockDocxConverter:
        mock_instance = MockDocxConverter.return_value
        
        result = converter.pdf_to_word(str(sample_pdf), output_docx)
        
        # Verificar flujo
        MockDocxConverter.assert_called_with(str(sample_pdf))
        mock_instance.convert.assert_called_with(output_docx, start=0, end=None)
        mock_instance.close.assert_called()
        
        assert result['success'] is True
