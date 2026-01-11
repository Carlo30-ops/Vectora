"""
Tests para el módulo history_manager
Prueba la gestión del historial de operaciones
"""
import pytest
import json
from pathlib import Path
from unittest.mock import patch, mock_open
from utils.history_manager import HistoryManager
from config.settings import settings


class TestHistoryManager:
    """Tests para HistoryManager"""
    
    @pytest.fixture
    def history_file_path(self, temp_dir):
        """Fixture que retorna ruta temporal para historial"""
        return temp_dir / "history.json"
    
    @pytest.fixture
    def mock_history_file(self, history_file_path, monkeypatch):
        """Fixture que mockea el archivo de historial"""
        def mock_get_history_file():
            return history_file_path
        
        monkeypatch.setattr(HistoryManager, 'get_history_file', staticmethod(mock_get_history_file))
        return history_file_path
    
    @pytest.mark.unit
    def test_get_history_file(self):
        """Test: Obtiene ruta correcta del archivo de historial"""
        path = HistoryManager.get_history_file()
        assert isinstance(path, Path)
        assert path.name == "history.json"
    
    @pytest.mark.unit
    def test_load_history_empty_file(self, mock_history_file):
        """Test: Cargar historial cuando el archivo no existe"""
        # Asegurar que el archivo no existe
        if mock_history_file.exists():
            mock_history_file.unlink()
        
        history = HistoryManager.load_history()
        assert history == []
    
    @pytest.mark.unit
    def test_load_history_existing_file(self, mock_history_file):
        """Test: Cargar historial desde archivo existente"""
        test_data = [
            {
                "timestamp": "2026-01-10 12:00:00",
                "operation": "Combinar PDFs",
                "input": "test1.pdf",
                "output": "merged.pdf"
            }
        ]
        
        mock_history_file.write_text(json.dumps(test_data, ensure_ascii=False), encoding='utf-8')
        
        history = HistoryManager.load_history()
        assert len(history) == 1
        assert history[0]['operation'] == "Combinar PDFs"
    
    @pytest.mark.unit
    def test_load_history_invalid_json(self, mock_history_file):
        """Test: Cargar historial con JSON inválido (debe retornar lista vacía)"""
        mock_history_file.write_text("invalid json", encoding='utf-8')
        
        history = HistoryManager.load_history()
        assert history == []
    
    @pytest.mark.unit
    def test_add_entry_new_history(self, mock_history_file):
        """Test: Agregar entrada a historial nuevo"""
        if mock_history_file.exists():
            mock_history_file.unlink()
        
        HistoryManager.add_entry("Combinar PDFs", "input1.pdf", "output1.pdf")
        
        history = HistoryManager.load_history()
        assert len(history) == 1
        assert history[0]['operation'] == "Combinar PDFs"
        assert history[0]['input'] == "input1.pdf"
        assert history[0]['output'] == "output1.pdf"
        assert 'timestamp' in history[0]
    
    @pytest.mark.unit
    def test_add_entry_existing_history(self, mock_history_file):
        """Test: Agregar entrada a historial existente"""
        initial_data = [
            {
                "timestamp": "2026-01-10 12:00:00",
                "operation": "Combinar PDFs",
                "input": "test1.pdf",
                "output": "merged.pdf"
            }
        ]
        mock_history_file.write_text(json.dumps(initial_data, ensure_ascii=False), encoding='utf-8')
        
        HistoryManager.add_entry("Dividir PDF", "test2.pdf", "split.pdf")
        
        history = HistoryManager.load_history()
        assert len(history) == 2
        # La nueva entrada debe estar al inicio
        assert history[0]['operation'] == "Dividir PDF"
        assert history[1]['operation'] == "Combinar PDFs"
    
    @pytest.mark.unit
    def test_add_entry_inserts_at_beginning(self, mock_history_file):
        """Test: Las nuevas entradas se insertan al principio"""
        # Agregar varias entradas
        HistoryManager.add_entry("Op1", "file1.pdf", "out1.pdf")
        HistoryManager.add_entry("Op2", "file2.pdf", "out2.pdf")
        HistoryManager.add_entry("Op3", "file3.pdf", "out3.pdf")
        
        history = HistoryManager.load_history()
        assert len(history) == 3
        # Última entrada agregada debe estar primero
        assert history[0]['operation'] == "Op3"
        assert history[1]['operation'] == "Op2"
        assert history[2]['operation'] == "Op1"
    
    @pytest.mark.unit
    def test_add_entry_limits_to_50(self, mock_history_file):
        """Test: Limita historial a 50 entradas"""
        # Agregar más de 50 entradas
        for i in range(60):
            HistoryManager.add_entry(f"Op{i}", f"file{i}.pdf", f"out{i}.pdf")
        
        history = HistoryManager.load_history()
        assert len(history) == 50
    
    @pytest.mark.unit
    def test_add_entry_with_none_values(self, mock_history_file):
        """Test: Maneja valores None correctamente"""
        HistoryManager.add_entry("Test Op", None, "output.pdf")
        
        history = HistoryManager.load_history()
        assert history[0]['input'] == "N/A"
        assert history[0]['output'] == "output.pdf"
        
        HistoryManager.add_entry("Test Op2", "input.pdf", None)
        history = HistoryManager.load_history()
        assert history[0]['input'] == "input.pdf"
        assert history[0]['output'] == "N/A"
    
    @pytest.mark.unit
    def test_clear_history(self, mock_history_file):
        """Test: Limpiar historial"""
        # Agregar algunas entradas
        HistoryManager.add_entry("Op1", "file1.pdf", "out1.pdf")
        HistoryManager.add_entry("Op2", "file2.pdf", "out2.pdf")
        
        # Verificar que existen
        history = HistoryManager.load_history()
        assert len(history) == 2
        
        # Limpiar
        HistoryManager.clear_history()
        
        # Verificar que está vacío
        history = HistoryManager.load_history()
        assert history == []
        
        # Verificar que el archivo existe pero está vacío
        content = mock_history_file.read_text(encoding='utf-8')
        assert content == "[]" or content.strip() == "[]"
