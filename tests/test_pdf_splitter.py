"""
Tests para el servicio PDFSplitter
Prueba los 3 modos de división: por rango, páginas específicas, y cada N páginas
"""
import pytest
from pathlib import Path
from backend.services.pdf_splitter import PDFSplitter
from tests.conftest import assert_pdf_exists, assert_pdf_pages


class TestPDFSplitterParsing:
    """Tests para parsing de especificación de páginas"""
    
    @pytest.mark.unit
    def test_parse_single_page(self):
        """Test: Parsear página individual"""
        result = PDFSplitter.parse_page_specification("5")
        assert result == [5]
    
    @pytest.mark.unit
    def test_parse_multiple_single_pages(self):
        """Test: Parsear múltiples páginas individuales"""
        result = PDFSplitter.parse_page_specification("1, 3, 5")
        assert result == [1, 3, 5]
    
    @pytest.mark.unit
    def test_parse_range(self):
        """Test: Parsear rango de páginas"""
        result = PDFSplitter.parse_page_specification("5-8")
        assert result == [5, 6, 7, 8]
    
    @pytest.mark.unit
    def test_parse_mixed_specification(self):
        """Test: Parsear especificación mixta"""
        result = PDFSplitter.parse_page_specification("1, 3, 5-8, 12")
        assert result == [1, 3, 5, 6, 7, 8, 12]
    
    @pytest.mark.unit
    def test_parse_removes_duplicates(self):
        """Test: Elimina duplicados y ordena"""
        result = PDFSplitter.parse_page_specification("3, 1, 3, 2")
        assert result == [1, 2, 3]
    
    @pytest.mark.unit
    def test_parse_invalid_range_raises_error(self):
        """Test: Error si el rango es inválido (inicio > fin)"""
        with pytest.raises(ValueError):
            PDFSplitter.parse_page_specification("10-5")
    
    @pytest.mark.unit
    def test_parse_invalid_format_raises_error(self):
        """Test: Error si el formato es inválido"""
        with pytest.raises(ValueError):
            PDFSplitter.parse_page_specification("abc")


class TestPDFSplitterByRange:
    """Tests para división por rango"""
    
    @pytest.mark.unit
    def test_split_by_range_middle_pages(self, sample_pdf_multipage, output_path):
        """Test: Dividir rango de páginas del medio"""
        # Arrange - PDF tiene 10 páginas
        
        # Act - Extraer páginas 3-7
        result = PDFSplitter.split_by_range(
            str(sample_pdf_multipage),
            output_path,
            start_page=3,
            end_page=7
        )
        
        # Assert
        assert result['success'] is True
        assert result['pages_extracted'] == 5  # 3, 4, 5, 6, 7
        assert_pdf_exists(output_path)
        assert_pdf_pages(output_path, 5)
    
    @pytest.mark.unit
    def test_split_by_range_first_pages(self, sample_pdf_multipage, output_path):
        """Test: Dividir primeras páginas"""
        # Act
        result = PDFSplitter.split_by_range(
            str(sample_pdf_multipage),
            output_path,
            start_page=1,
            end_page=3
        )
        
        # Assert
        assert result['pages_extracted'] == 3
        assert_pdf_pages(output_path, 3)
    
    @pytest.mark.unit
    def test_split_by_range_out_of_bounds_raises_error(self, sample_pdf_multipage, output_path):
        """Test: Error si el rango está fuera de límites"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            PDFSplitter.split_by_range(
                str(sample_pdf_multipage),
                output_path,
                start_page=1,
                end_page=20  # PDF solo tiene 10 páginas
            )
        
        assert "debe estar entre" in str(exc_info.value).lower()
    
    @pytest.mark.unit
    def test_split_by_range_invalid_order_raises_error(self, sample_pdf_multipage, output_path):
        """Test: Error si inicio > fin"""
        with pytest.raises(ValueError):
            PDFSplitter.split_by_range(
                str(sample_pdf_multipage),
                output_path,
                start_page=5,
                end_page=2
            )


class TestPDFSplitterByPages:
    """Tests para división por páginas específicas"""
    
    @pytest.mark.unit
    def test_split_by_specific_pages(self, sample_pdf_multipage, output_path):
        """Test: Dividir por páginas específicas"""
        # Act
        result = PDFSplitter.split_by_pages(
            str(sample_pdf_multipage),
            output_path,
            page_specification="1, 3, 5-7, 10"
        )
        
        # Assert
        assert result['success'] is True
        # Páginas: 1, 3, 5, 6, 7, 10 = 6 páginas
        assert result['pages_extracted'] == 6
        assert_pdf_pages(output_path, 6)
    
    @pytest.mark.unit
    def test_split_by_pages_out_of_bounds_raises_error(self, sample_pdf_multipage, output_path):
        """Test: Error si alguna página está fuera de límites"""
        with pytest.raises(ValueError):
            PDFSplitter.split_by_pages(
                str(sample_pdf_multipage),
                output_path,
                page_specification="1, 15"  # 15 > 10
            )


class TestPDFSplitterEveryN:
    """Tests para división cada N páginas"""
    
    @pytest.mark.unit
    def test_split_every_n_pages(self, sample_pdf_multipage, temp_dir):
        """Test: Dividir cada 3 páginas"""
        # Act - PDF tiene 10 páginas, dividir cada 3
        result = PDFSplitter.split_every_n_pages(
            str(sample_pdf_multipage),
            str(temp_dir),
            n_pages=3
        )
        
        # Assert
        assert result['success'] is True
        assert result['total_parts'] == 4  # 3+3+3+1 = 4 archivos
        assert len(result['output_files']) == 4
        
        # Verificar cada archivo
        assert_pdf_pages(result['output_files'][0], 3)  # Páginas 1-3
        assert_pdf_pages(result['output_files'][1], 3)  # Páginas 4-6
        assert_pdf_pages(result['output_files'][2], 3)  # Páginas 7-9
        assert_pdf_pages(result['output_files'][3], 1)  # Página 10
    
    @pytest.mark.unit
    def test_split_every_1_page(self, sample_pdfs_multiple, temp_dir):
        """Test: Dividir cada página (1 archivo por página)"""
        # Arrange - Usar PDF con 3 páginas
        pdf_path = sample_pdfs_multiple[2]  # El tercero tiene 3 páginas
        
        # Act
        result = PDFSplitter.split_every_n_pages(pdf_path, str(temp_dir), n_pages=1)
        
        # Assert
        assert result['total_parts'] == 3
        for file in result['output_files']:
            assert_pdf_pages(file, 1)
    
    @pytest.mark.unit
    def test_split_every_n_invalid_number_raises_error(self, sample_pdf_multipage, temp_dir):
        """Test: Error si N es menor a 1"""
        with pytest.raises(ValueError):
            PDFSplitter.split_every_n_pages(
                str(sample_pdf_multipage),
                str(temp_dir),
                n_pages=0
            )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
