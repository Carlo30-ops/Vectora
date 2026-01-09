"""
Validadores para diferentes tipos de entrada
"""
from typing import List, Tuple, Optional
import re


class Validators:
    """Utilidades de validación"""
    
    @staticmethod
    def validate_page_range(
        start: int,
        end: int,
        total_pages: int
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida un rango de páginas
        
        Args:
            start: Página inicial (1-indexed)
            end: Página final (1-indexed)
            total_pages: Total de páginas del PDF
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if start < 1:
            return False, "La página inicial debe ser mayor o igual a 1"
        
        if end > total_pages:
            return False, f"La página final no puede ser mayor a {total_pages}"
        
        if start > end:
            return False, "La página inicial debe ser menor o igual que la final"
        
        return True, None
    
    @staticmethod
    def parse_page_specification(spec: str) -> Tuple[bool, Optional[List[int]], Optional[str]]:
        """
        Parsea y valida especificación de páginas
        
        Args:
            spec: Especificación (ej: "1,3,5-8,12")
            
        Returns:
            Tupla (es_valido, lista_paginas, mensaje_error)
        """
        if not spec or not spec.strip():
            return False, None, "La especificación no puede estar vacía"
        
        try:
            pages = set()
            parts = spec.split(',')
            
            for part in parts:
                part = part.strip()
                
                if '-' in part:
                    # Rango
                    range_parts = part.split('-')
                    if len(range_parts) != 2:
                        return False, None, f"Rango inválido: {part}"
                    
                    start = int(range_parts[0].strip())
                    end = int(range_parts[1].strip())
                    
                    if start > end:
                        return False, None, f"Rango inválido {part}: inicio > fin"
                    
                    pages.update(range(start, end + 1))
                else:
                    # Página individual
                    pages.add(int(part))
            
            return True, sorted(list(pages)), None
            
        except ValueError as e:
            return False, None, f"Formato inválido: {str(e)}"
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
        """
        Valida la fortaleza de una contraseña
        
        Args:
            password: Contraseña a validar
            
        Returns:
            Tupla (es_fuerte, lista_recomendaciones)
        """
        recommendations = []
        
        if len(password) < 8:
            recommendations.append("Usa al menos 8 caracteres")
        
        if not any(c.isupper() for c in password):
            recommendations.append("Incluye al menos una mayúscula")
        
        if not any(c.islower() for c in password):
            recommendations.append("Incluye al menos una minúscula")
        
        if not any(c.isdigit() for c in password):
            recommendations.append("Incluye al menos un número")
        
        if not any(not c.isalnum() for c in password):
            recommendations.append("Incluye al menos un carácter especial")
        
        is_strong = len(recommendations) == 0
        
        return is_strong, recommendations
    
    @staticmethod
    def validate_compression_value(value: int) -> Tuple[bool, Optional[str]]:
        """
        Valida un valor de compresión
        
        Args:
            value: Valor del slider (0-100)
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if value < 0 or value > 100:
            return False, "El valor debe estar entre 0 y 100"
        
        return True, None
    
    @staticmethod
    def validate_dpi(dpi: int) -> Tuple[bool, Optional[str]]:
        """
        Valida un valor de DPI
        
        Args:
            dpi: Valor DPI
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if dpi < 72:
            return False, "El DPI mínimo es 72"
        
        if dpi > 1200:
            return False, "El DPI máximo es 1200"
        
        return True, None
    
    @staticmethod
    def validate_n_pages(n: int) -> Tuple[bool, Optional[str]]:
        """
        Valida el número de páginas para división
        
        Args:
            n: Número de páginas
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if n < 1:
            return False, "Debe dividir cada 1 o más páginas"
        
        return True, None
    
    @staticmethod
    def validate_file_count(
        count: int,
        min_count: Optional[int] = None,
        max_count: Optional[int] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida el número de archivos
        
        Args:
            count: Número de archivos
            min_count: Mínimo de archivos requeridos
            max_count: Máximo de archivos permitidos
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if min_count is not None and count < min_count:
            return False, f"Se requieren al menos {min_count} archivos"
        
        if max_count is not None and count > max_count:
            return False, f"Máximo {max_count} archivos permitidos"
        
        return True, None
