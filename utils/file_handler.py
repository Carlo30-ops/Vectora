"""
Manejo de archivos y operaciones del sistema de archivos
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional

from PyPDF2 import PdfReader


class FileHandler:
    """Utilidades para manejo de archivos"""

    @staticmethod
    def get_filename(file_path: str) -> str:
        """
        Obtiene el nombre del archivo desde la ruta
        """
        return Path(file_path).name

    @staticmethod
    def validate_pdf_file(file_path: str) -> bool:
        """
        Verifica que un archivo sea un PDF válido

        Args:
            file_path: Ruta del archivo

        Returns:
            True si es un PDF válido, False en caso contrario
        """
        try:
            with open(file_path, "rb") as f:
                # Verificar magic bytes del PDF
                header = f.read(5)
                if not header.startswith(b"%PDF-"):
                    return False

            # Intentar abrir con PyPDF2
            PdfReader(file_path)
            return True
        except:
            return False

    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """
        Obtiene el tamaño de un archivo en MB

        Args:
            file_path: Ruta del archivo

        Returns:
            Tamaño en megabytes
        """
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)

    @staticmethod
    def get_file_size_formatted(file_path: str) -> str:
        """
        Obtiene el tamaño de un archivo formateado

        Args:
            file_path: Ruta del archivo

        Returns:
            Tamaño formateado (ej: "2.5 MB", "450 KB")
        """
        size_bytes = os.path.getsize(file_path)

        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

    @staticmethod
    def create_temp_file(extension: str = ".pdf") -> str:
        """
        Crea un archivo temporal

        Args:
            extension: Extensión del archivo (incluir el punto)

        Returns:
            Ruta del archivo temporal
        """
        temp_fd, temp_path = tempfile.mkstemp(suffix=extension)
        os.close(temp_fd)
        return temp_path

    @staticmethod
    def clean_temp_files(directory: str):
        """
        Limpia archivos temporales en un directorio

        Args:
            directory: Directorio a limpiar
        """
        try:
            if Path(directory).exists():
                for item in Path(directory).iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
        except Exception as e:
            print(f"Error al limpiar archivos temporales: {e}")

    @staticmethod
    def ensure_unique_filename(file_path: str) -> str:
        """
        Asegura que el nombre de archivo sea único agregando un número si es necesario

        Args:
            file_path: Ruta del archivo

        Returns:
            Ruta única del archivo
        """
        path = Path(file_path)

        if not path.exists():
            return file_path

        base_dir = path.parent
        stem = path.stem
        extension = path.suffix

        counter = 1
        while True:
            new_name = f"{stem}_{counter}{extension}"
            new_path = base_dir / new_name
            if not new_path.exists():
                return str(new_path)
            counter += 1

    @staticmethod
    def get_pdf_page_count(file_path: str) -> int:
        """
        Obtiene el número de páginas de un PDF

        Args:
            file_path: Ruta del PDF

        Returns:
            Número de páginas
        """
        try:
            reader = PdfReader(file_path)
            return len(reader.pages)
        except:
            return 0

    @staticmethod
    def validate_file_extensions(
        file_paths: List[str], allowed_extensions: List[str]
    ) -> tuple[bool, List[str]]:
        """
        Valida que todos los archivos tengan extensiones permitidas

        Args:
            file_paths: Lista de rutas de archivos
            allowed_extensions: Lista de extensiones permitidas (ej: ['.pdf', '.docx'])

        Returns:
            Tupla (es_valido, archivos_invalidos)
        """
        invalid_files = []

        for path in file_paths:
            ext = Path(path).suffix.lower()
            if ext not in [e.lower() for e in allowed_extensions]:
                invalid_files.append(Path(path).name)

        return len(invalid_files) == 0, invalid_files

    @staticmethod
    def validate_disk_space(target_path: str, required_mb: float = 50.0) -> bool:
        """
        Verifica si hay suficiente espacio en disco

        Args:
            target_path: Ruta donde se guardará (o directorio padre)
            required_mb: Espacio requerido en MB

        Returns:
            True si hay espacio, False si no
        """
        try:
            path = Path(target_path)
            if not path.exists():
                path = path.parent

            # Si el padre tampoco existe (caso raro), usar el root del drive
            if not path.exists():
                path = Path(path.anchor)

            total, used, free = shutil.disk_usage(str(path))
            free_mb = free / (1024 * 1024)

            return free_mb >= required_mb
        except Exception as e:
            print(f"Error verificando espacio en disco: {e}")
            return True  # Asumir True en error para no bloquear
