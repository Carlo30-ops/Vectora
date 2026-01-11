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
    
    @pytest.fixture
    def splitter(self):
        """Fixture para crear instancia de PDFSplitter"""
        return PDFSplitter()
    
    @pytest.mark.unit
    def test_parse_single_page(self, splitter):
        """Test: Parsear página individual"""
        result = splitter.parse_page_specification("5")
        assert result == [5]
    
    @pytest.mark.unit
    def test_parse_multiple_single_pages(self, splitter):
        """Test: Parsear múltiples páginas individuales"""
        result = splitter.parse_page_specification("1, 3, 5")
        assert result == [1, 3, 5]
    
    @pytest.mark.unit
    def test_parse_range(self, splitter):
        """Test: Parsear rango de páginas"""
        result = splitter.parse_page_specification("5-8")
        assert result == [5, 6, 7, 8]
    
    @pytest.mark.unit
    def test_parse_mixed_specification(self, splitter):
        """Test: Parsear especificación mixta"""
        result = splitter.parse_page_specification("1, 3, 5-8, 12")
        assert result == [1, 3, 5, 6, 7, 8, 12]
    
    @pytest.mark.unit
    def test_parse_removes_duplicates(self, splitter):
        """Test: Elimina duplicados y ordena"""
        result = splitter.parse_page_specification("3, 1, 3, 2")
        assert result == [1, 2, 3]
    
    @pytest.mark.unit
    def test_parse_invalid_range_raises_error(self, splitter):
        """Test: Error si el rango es inválido (inicio > fin)"""
        with pytest.raises(ValueError):
            splitter.parse_page_specification("10-5")
    
    @pytest.mark.unit
    def test_parse_invalid_format_raises_error(self, splitter):
        """Test: Error si el formato es inválido"""
        with pytest.raises(ValueError):
            splitter.parse_page_specification("abc")


class TestPDFSplitterByRange:
    """Tests para división por rango"""
    
    @pytest.fixture
    def splitter(self):
        """Fixture para crear instancia de PDFSplitter"""
        return PDFSplitter()
    
    @pytest.mark.unit
    def test_split_by_range_middle_pages(self, splitter, sample_pdf_multipage, output_path):
        """Test: Dividir rango de páginas del medio"""
        # Arrange - PDF tiene 10 páginas
        
        # Act - Extraer páginas 3-7
        result = splitter.split_by_range(
            str(sample_pdf_multipage),
            output_path,
            start_page=3,
            end_page=7
        )
        
        # Assert
        assert result['success'] is True
        assert_pdf_exists(output_path)
        assert_pdf_pages(output_path, 5)  # 5 páginas (3, 4, 5, 6, 7)
    
    @pytest.mark.unit
    def test_split_by_range_first_pages(self, splitter, sample_pdf_multipage, output_path):
        """Test: Dividir primeras páginas"""
        # Act
        result = splitter.split_by_range(
            str(sample_pdf_multipage),
            output_path,
            start_page=1,
            end_page=3
        )
        
        # Assert
        assert result['success'] is True
        assert_pdf_exists(output_path)
        assert_pdf_pages(output_path, 3)
    
    @pytest.mark.unit
    def test_split_by_range_out_of_bounds_raises_error(self, splitter, sample_pdf_multipage, output_path):
        """Test: Error si el rango está fuera de límites"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            splitter.split_by_range(
                str(sample_pdf_multipage),
                output_path,
                start_page=1,
                end_page=20  # PDF solo tiene 10 páginas
            )
        assert "rango" in str(exc_info.value).lower() or "entre" in str(exc_info.value).lower()
    
    @pytest.mark.unit
    def test_split_by_range_invalid_order_raises_error(self, splitter, sample_pdf_multipage, output_path):
        """Test: Error si inicio > fin"""
        with pytest.raises(ValueError):
            splitter.split_by_range(
                str(sample_pdf_multipage),
                output_path,
                start_page=5,
                end_page=2
            )


class TestPDFSplitterByPages:
    """Tests para división por páginas específicas"""
    
    @pytest.fixture
    def splitter(self):
        """Fixture para crear instancia de PDFSplitter"""
        return PDFSplitter()
    
    @pytest.mark.unit
    def test_split_by_specific_pages(self, splitter, sample_pdf_multipage, output_path):
        """Test: Dividir por páginas específicas"""
        # Act
        result = splitter.split_by_pages(
            str(sample_pdf_multipage),
            output_path,
            page_specification="1, 3, 5-7, 10"
        )
        
        # Assert
        assert result['success'] is True
        assert_pdf_exists(output_path)
        # Páginas: 1, 3, 5, 6, 7, 10 = 6 páginas
        assert_pdf_pages(output_path, 6)
    
    @pytest.mark.unit
    def test_split_by_pages_out_of_bounds_raises_error(self, splitter, sample_pdf_multipage, output_path):
        """Test: Error si alguna página está fuera de límites"""
        with pytest.raises(ValueError):
            splitter.split_by_pages(
                str(sample_pdf_multipage),
                output_path,
                page_specification="1, 15"  # 15 > 10
            )


class TestPDFSplitterEveryN:
    """Tests para división cada N páginas"""
    
    @pytest.fixture
    def splitter(self):
        """Fixture para crear instancia de PDFSplitter"""
        return PDFSplitter()
    
    @pytest.mark.unit
    def test_split_every_n_pages(self, splitter, sample_pdf_multipage, temp_dir):
        """Test: Dividir cada 3 páginas"""
        # Act - PDF tiene 10 páginas, dividir cada 3
        result = splitter.split_every_n_pages(
            str(sample_pdf_multipage),
            str(temp_dir),
            n_pages=3
        )
        
        # Assert
        assert result['success'] is True
        # Debe crear 4 archivos: 3+3+3+1 = 10 páginas
        assert result['data']['total_parts'] == 4
        assert len(result['data']['output_files']) == 4
    
    @pytest.mark.unit
    def test_split_every_1_page(self, splitter, sample_pdfs_multiple, temp_dir):
        """Test: Dividir cada página (1 archivo por página)"""
        # Arrange - Usar PDF con 3 páginas
        pdf_path = sample_pdfs_multiple[2]  # El tercero tiene 3 páginas
        
        # Act
        result = splitter.split_every_n_pages(pdf_path, str(temp_dir), n_pages=1)
        
        # Assert
        assert result['success'] is True
        assert result['data']['total_parts'] == 3
        assert len(result['data']['output_files']) == 3
    
    @pytest.mark.unit
    def test_split_every_n_invalid_number_raises_error(self, splitter, sample_pdf_multipage, temp_dir):
        """Test: Error si N es menor a 1"""
        with pytest.raises(ValueError):
            splitter.split_every_n_pages(
                str(sample_pdf_multipage),
                str(temp_dir),
                n_pages=0
            )
