"""
Tests para el servicio PDFMerger
Prueba la combinación de múltiples PDFs en uno solo
"""
import pytest
from pathlib import Path
from backend.services.pdf_merger import PDFMerger
from tests.conftest import assert_pdf_exists, assert_pdf_pages, assert_file_size_greater_than


class TestPDFMerger:
    """Suite de tests para PDFMerger"""
    
    @pytest.fixture
    def merger(self):
        """Fixture para crear instancia de PDFMerger"""
        return PDFMerger()
    
    @pytest.mark.unit
    def test_merge_two_pdfs(self, merger, sample_pdfs_multiple, output_path):
        """Test: Combinar 2 PDFs correctamente"""
        # Arrange
        input_files = sample_pdfs_multiple[:2]  # Tomar solo 2
        
        # Act
        result = merger.merge_pdfs(input_files, output_path)
        
        # Assert
        assert result.success is True
        assert result.data['total_files'] == 2
        assert_pdf_exists(output_path)
        # PDF 1 tiene 1 página, PDF 2 tiene 2 páginas = 3 total
        assert_pdf_pages(output_path, 3)
    
    @pytest.mark.unit
    def test_merge_three_pdfs(self, merger, sample_pdfs_multiple, output_path):
        """Test: Combinar 3 PDFs correctamente"""
        # Arrange - Los 3 PDFs tienen 1, 2, 3 páginas
        input_files = sample_pdfs_multiple
        
        # Act
        result = merger.merge_pdfs(input_files, output_path)
        
        # Assert
        assert result.success is True
        assert result.data['total_files'] == 3
        assert_pdf_exists(output_path)
        # 1 + 2 + 3 = 6 páginas total
        assert_pdf_pages(output_path, 6)
    
    @pytest.mark.unit
    def test_merge_less_than_two_files_raises_error(self, merger, sample_pdf, output_path):
        """Test: Error si hay menos de 2 archivos"""
        # Arrange
        input_files = [str(sample_pdf)]  # Solo 1 archivo
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            merger.merge_pdfs(input_files, output_path)
        assert "al menos 2 archivos" in str(exc_info.value).lower()
    
    @pytest.mark.unit
    def test_merge_with_non_existent_file_raises_error(self, merger, sample_pdf, non_existent_file, output_path):
        """Test: Error si un archivo no existe"""
        # Arrange
        input_files = [str(sample_pdf), non_existent_file]
        
        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            merger.merge_pdfs(input_files, output_path)
        assert "no existe" in str(exc_info.value).lower()
    
    @pytest.mark.unit
    def test_progress_callback_is_called(self, merger, sample_pdfs_multiple, output_path):
        """Test: Callback de progreso es llamado correctamente"""
        # Arrange
        input_files = sample_pdfs_multiple
        progress_values = []

        def capture_progress(value, message):
            progress_values.append(value)

        # Act
        merger.merge_pdfs(input_files, output_path, progress_callback=capture_progress)
        
        # Assert
        assert len(progress_values) > 0
        assert progress_values[-1] == 100  # Último debe ser 100%
    
    @pytest.mark.unit
    def test_output_file_is_created(self, merger, sample_pdfs_multiple, output_path):
        """Test: El archivo de salida se crea correctamente"""
        # Arrange
        input_files = sample_pdfs_multiple
        
        # Act
        merger.merge_pdfs(input_files, output_path)
        
        # Assert
        assert_pdf_exists(output_path)
        assert_file_size_greater_than(output_path, 0)
    
    @pytest.mark.unit
    def test_result_contains_expected_fields(self, merger, sample_pdfs_multiple, output_path):
        """Test: El resultado contiene todos los campos esperados"""
        # Arrange
        input_files = sample_pdfs_multiple
        
        # Act
        result = merger.merge_pdfs(input_files, output_path)
        
        # Assert
        # Assert
        assert hasattr(result, 'success')
        assert hasattr(result, 'message')
        assert hasattr(result, 'data')
        assert result.data is not None and 'output_path' in result.data
        assert result.data is not None and 'total_files' in result.data
        assert result.success is True
    
    @pytest.mark.integration
    def test_merge_order_is_preserved(self, merger, temp_dir, output_path):
        """Test: El orden de los archivos se preserva"""
        # Arrange - Crear PDFs con diferentes números de páginas
        from PyPDF2 import PdfWriter

        files = []
        page_counts = [1, 3, 2]  # Orden específico

        for i, count in enumerate(page_counts):
            pdf_path = temp_dir / f"ordered_{i}.pdf"
            writer = PdfWriter()
            for _ in range(count):
                writer.add_blank_page(width=612, height=792)

            with open(pdf_path, 'wb') as f:
                writer.write(f)

            files.append(str(pdf_path))

        # Act
        result = merger.merge_pdfs(files, output_path)
        
        # Assert
        # Assert
        assert result.success is True
        assert_pdf_pages(output_path, 6)  # 1 + 3 + 2 = 6 páginas
