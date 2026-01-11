"""
Tests para el servicio PDFConverter
Prueba las conversiones entre formatos
"""
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from backend.services.pdf_converter import PDFConverter


@pytest.fixture
def mock_logger():
    return MagicMock()


@pytest.fixture
def converter(mock_logger):
    return PDFConverter(logger=mock_logger)


class TestPDFConverter:
    """Suite de tests para PDFConverter"""
    
    @pytest.mark.unit
    def test_pdf_to_word_success(self, converter, sample_pdf, temp_dir):
        """Test: Conversión PDF a Word exitosa (Mock)"""
        output_docx = str(temp_dir / "output.docx")
        
        # Mockear la clase Converter de pdf2docx
        with patch('backend.services.pdf_converter.Converter') as MockConverter:
            mock_instance = MagicMock()
            MockConverter.return_value = mock_instance
            
            result = converter.pdf_to_word(str(sample_pdf), output_docx)
            
            # Verificar flujo
            MockConverter.assert_called_once_with(str(sample_pdf))
            mock_instance.convert.assert_called_once_with(output_docx, start=0, end=None)
            mock_instance.close.assert_called_once()
            
            assert result['success'] is True
            assert result['output_path'] == output_docx
    
    @pytest.mark.unit
    def test_pdf_to_word_with_callback(self, converter, sample_pdf, temp_dir):
        """Test: Conversión PDF a Word con callback de progreso"""
        output_docx = str(temp_dir / "output.docx")
        mock_callback = MagicMock()
        
        with patch('backend.services.pdf_converter.Converter') as MockConverter:
            mock_instance = MagicMock()
            MockConverter.return_value = mock_instance
            
            result = converter.pdf_to_word(
                str(sample_pdf),
                output_docx,
                progress_callback=mock_callback
            )
            
            assert result['success'] is True
            # Callback debe llamarse al final con 100
            assert mock_callback.call_count > 0
    
    @pytest.mark.unit
    def test_pdf_to_images_success(self, converter, sample_pdf, temp_dir):
        """Test: Conversión PDF a imágenes exitosa (Mock)"""
        output_dir = str(temp_dir)
        
        with patch('backend.services.pdf_converter.convert_from_path') as mock_convert:
            # Simular 2 imágenes
            mock_img = MagicMock()
            mock_convert.return_value = [mock_img, mock_img]
            
            result = converter.pdf_to_images(str(sample_pdf), output_dir)
            
            assert result['success'] is True
            assert result['total_images'] == 2
            assert len(result['output_files']) == 2
            # Verificar que se guardaron las imágenes
            assert mock_img.save.call_count == 2
    
    @pytest.mark.unit
    def test_pdf_to_images_with_callback(self, converter, sample_pdf, temp_dir):
        """Test: Conversión PDF a imágenes con callback"""
        output_dir = str(temp_dir)
        mock_callback = MagicMock()
        
        with patch('backend.services.pdf_converter.convert_from_path') as mock_convert:
            mock_img = MagicMock()
            mock_convert.return_value = [mock_img, mock_img]
            
            result = converter.pdf_to_images(
                str(sample_pdf),
                output_dir,
                progress_callback=mock_callback
            )
            
            assert result['success'] is True
            assert mock_callback.call_count == 2  # Una vez por página
    
    @pytest.mark.unit
    def test_pdf_to_images_custom_dpi_and_format(self, converter, sample_pdf, temp_dir):
        """Test: Conversión PDF a imágenes con DPI y formato personalizados"""
        output_dir = str(temp_dir)
        
        with patch('backend.services.pdf_converter.convert_from_path') as mock_convert:
            mock_img = MagicMock()
            mock_convert.return_value = [mock_img]
            
            result = converter.pdf_to_images(
                str(sample_pdf),
                output_dir,
                dpi=600,
                image_format='JPEG'
            )
            
            assert result['success'] is True
            # Verificar que se llamó con el DPI correcto
            mock_convert.assert_called_once()
            call_kwargs = mock_convert.call_args[1]
            assert call_kwargs['dpi'] == 600
    
    @pytest.mark.unit
    def test_images_to_pdf_success(self, converter, temp_dir, output_path):
        """Test: Crear PDF desde imágenes (Mock)"""
        # Crear archivos de imagen simulados
        img_paths = [
            str(temp_dir / "img1.png"),
            str(temp_dir / "img2.jpg")
        ]
        
        with patch('PIL.Image.open') as mock_open, \
             patch('PIL.Image.new') as mock_new:
            mock_img = MagicMock()
            mock_img.size = (800, 600)
            mock_open.return_value = mock_img
            mock_pdf_img = MagicMock()
            mock_new.return_value = mock_pdf_img
            
            result = converter.images_to_pdf(img_paths, output_path)
            
            assert result['success'] is True
            assert result['image_count'] == 2
    
    @pytest.mark.unit
    def test_images_to_pdf_empty_list(self, converter, output_path):
        """Test: Error con lista vacía de imágenes"""
        with pytest.raises(Exception):
            converter.images_to_pdf([], output_path)
    
    @pytest.mark.unit
    def test_word_to_pdf_success(self, converter, temp_dir, output_path):
        """Test: Conversión Word a PDF exitosa (Mock)"""
        input_docx = str(temp_dir / "input.docx")
        
        with patch('docx2pdf.convert') as mock_convert:
            result = converter.word_to_pdf(input_docx, output_path)
            
            mock_convert.assert_called_once_with(input_docx, output_path)
            assert result['success'] is True
            assert result['output_path'] == output_path
