"""
Servicio de seguridad para PDFs
Encriptación, desencriptación y configuración de permisos
"""
import pikepdf
from pathlib import Path
from typing import Optional, Dict, Any
from logging import Logger
from utils.logger import get_logger

class PDFSecurity:
    """Servicio para gestión de seguridad de PDFs"""
    
    def __init__(self, logger: Optional[Logger] = None):
        """
        Inicializa el servicio de seguridad
        Args:
            logger: Logger personalizado (opcional)
        """
        self.logger = logger or get_logger(__name__)

    def encrypt_pdf(
        self,
        input_path: str,
        output_path: str,
        password: str,
        permissions: Optional[Dict[str, bool]] = None
    ) -> dict:
        """Encripta un PDF con contraseña y permisos opcionales"""
        # Validaciones
        if not password:
            raise ValueError("La contraseña no puede estar vacía")
        
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"El archivo no existe: {input_path}")
        
        if not input_file.suffix.lower() == '.pdf':
            raise ValueError(f"El archivo debe ser un PDF: {input_path}")
        
        # Validar directorio de salida
        output_file = Path(output_path)
        output_dir = output_file.parent
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            test_file = output_dir / '.write_test'
            test_file.write_text('test')
            test_file.unlink()
        except (PermissionError, OSError) as e:
            raise PermissionError(f"No se puede escribir en el directorio de salida: {output_dir}") from e
        
        self.logger.info(f"Encriptando PDF: {input_path}")
        try:
            with pikepdf.open(input_path) as pdf:
                # Configurar permisos
                if permissions:
                    encryption_dict = pikepdf.Encryption(
                        owner=password,  # Contraseña del propietario
                        user=password,   # Contraseña del usuario
                        R=6,  # Versión de encriptación (AES-256)
                        allow=pikepdf.Permissions(
                            print_=permissions.get('allow_print', True),
                            modify=permissions.get('allow_modify', False),
                            extract=permissions.get('allow_copy', True),
                            annotate=permissions.get('allow_annotations', True)
                        )
                    )
                else:
                    # Encriptación simple (todos los permisos)
                    encryption_dict = pikepdf.Encryption(
                        owner=password,
                        user=password,
                        R=6
                    )
                
                pdf.save(output_path, encryption=encryption_dict)
            
            return {
                'success': True,
                'output_path': output_path,
                'message': 'PDF encriptado exitosamente'
            }
            
        except Exception as e:
            self.logger.error(f"Error encriptando PDF: {e}", exc_info=True)
            raise Exception(f"Error al encriptar PDF: {str(e)}")
    
    def decrypt_pdf(
        self,
        input_path: str,
        output_path: str,
        password: str
    ) -> dict:
        """Remueve la encriptación de un PDF"""
        # Validaciones
        if not password:
            raise ValueError("La contraseña no puede estar vacía")
        
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"El archivo no existe: {input_path}")
        
        if not input_file.suffix.lower() == '.pdf':
            raise ValueError(f"El archivo debe ser un PDF: {input_path}")
        
        # Validar directorio de salida
        output_file = Path(output_path)
        output_dir = output_file.parent
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            test_file = output_dir / '.write_test'
            test_file.write_text('test')
            test_file.unlink()
        except (PermissionError, OSError) as e:
            raise PermissionError(f"No se puede escribir en el directorio de salida: {output_dir}") from e
        
        self.logger.info(f"Desencriptando PDF: {input_path}")
        try:
            with pikepdf.open(input_path, password=password) as pdf:
                # Guardar sin encriptación
                pdf.save(output_path)
            
            return {
                'success': True,
                'output_path': output_path,
                'message': 'PDF desencriptado exitosamente'
            }
            
        except pikepdf.PasswordError:
            self.logger.warning("Intento de desencriptación fallido: Contraseña incorrecta")
            raise Exception("Contraseña incorrecta")
        except Exception as e:
            self.logger.error(f"Error desencriptando: {e}", exc_info=True)
            raise Exception(f"Error al desencriptar PDF: {str(e)}")
    
    def set_permissions(
        self,
        input_path: str,
        output_path: str,
        permissions: Dict[str, bool],
        owner_password: Optional[str] = None
    ) -> dict:
        """Configura permisos específicos sin requerir contraseña de usuario"""
        self.logger.info(f"Configurando permisos en: {input_path}")
        try:
            with pikepdf.open(input_path) as pdf:
                # Si no se proporciona contraseña de propietario, usar una por defecto
                pwd = owner_password if owner_password else "owner_default_pwd"
                
                encryption_dict = pikepdf.Encryption(
                    owner=pwd,
                    user="",  # Sin contraseña de usuario
                    R=6,
                    allow=pikepdf.Permissions(
                        print_=permissions.get('allow_print', True),
                        modify=permissions.get('allow_modify', False),
                        extract=permissions.get('allow_copy', True),
                        annotate=permissions.get('allow_annotations', True)
                    )
                )
                
                pdf.save(output_path, encryption=encryption_dict)
            
            return {
                'success': True,
                'output_path': output_path,
                'message': 'Permisos configurados exitosamente'
            }
            
        except Exception as e:
            self.logger.error(f"Error configurando permisos: {e}", exc_info=True)
            raise Exception(f"Error al configurar permisos: {str(e)}")
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Valida la fortaleza de una contraseña"""
        recommendations = []
        
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        if length < 8:
            recommendations.append("Usa al menos 8 caracteres")
        if not has_upper:
            recommendations.append("Incluye al menos una mayúscula")
        if not has_lower:
            recommendations.append("Incluye al menos una minúscula")
        if not has_digit:
            recommendations.append("Incluye al menos un número")
        if not has_special:
            recommendations.append("Incluye al menos un carácter especial")
        
        is_strong = (
            length >= 8 and
            has_upper and
            has_lower and
            has_digit
        )
        
        return {
            'is_strong': is_strong,
            'length': length,
            'has_upper': has_upper,
            'has_lower': has_lower,
            'has_digit': has_digit,
            'has_special': has_special,
            'recommendations': recommendations
        }
