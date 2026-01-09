"""
Gestor de historial de operaciones
"""
import json
import os
from datetime import datetime
from config.settings import settings

class HistoryManager:
    
    @staticmethod
    def get_history_file():
        return settings.BASE_DIR / "history.json"
        
    @classmethod
    def load_history(cls):
        path = cls.get_history_file()
        if not path.exists():
            return []
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
            
    @classmethod
    def add_entry(cls, operation, input_file, output_file):
        history = cls.load_history()
        
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operation": operation,
            "input": str(input_file) if input_file else "N/A",
            "output": str(output_file) if output_file else "N/A"
        }
        
        # Insertar al inicio
        history.insert(0, entry)
        
        # Limitar a 50 entradas
        history = history[:50]
        
        try:
            with open(cls.get_history_file(), 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando historial: {e}")
            
    @classmethod
    def clear_history(cls):
        try:
            with open(cls.get_history_file(), 'w', encoding='utf-8') as f:
                json.dump([], f)
        except:
            pass
