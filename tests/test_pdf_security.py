import pytest
from unittest.mock import MagicMock, patch
from backend.services.pdf_security import PDFSecurity

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def security(mock_logger):
    return PDFSecurity(logger=mock_logger)

def test_encrypt_pdf(security, sample_pdf, output_path):
    """Test encriptación de PDF"""
    pwd = "securepassword"
    
    with patch('pikepdf.open') as mock_open:
        mock_pdf = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_pdf
        
        result = security.encrypt_pdf(str(sample_pdf), output_path, pwd)
        
        # Verificar que se configuró encriptación y se guardó
        mock_pdf.save.assert_called()
        encryption_arg = mock_pdf.save.call_args[1]['encryption']
        assert encryption_arg.owner == pwd
        assert result['success'] is True

def test_decrypt_pdf(security, sample_pdf, output_path):
    """Test desencriptación de PDF"""
    pwd = "securepassword"
    
    with patch('pikepdf.open') as mock_open:
        mock_pdf = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_pdf
        
        result = security.decrypt_pdf(str(sample_pdf), output_path, pwd)
        
        mock_open.assert_called_with(str(sample_pdf), password=pwd)
        mock_pdf.save.assert_called_with(output_path)
        assert result['success'] is True

def test_password_validation_weak(security):
    """Test: Validación de contraseña débil"""
    weak = "123"
    result = security.validate_password_strength(weak)
    
    assert result['is_strong'] is False
    assert len(result['recommendations']) > 0
    assert result['length'] == 3
    assert '8 caracteres' in ' '.join(result['recommendations'])

def test_password_validation_strong(security):
    """Test: Validación de contraseña fuerte"""
    strong = "StrongPass1!"
    result = security.validate_password_strength(strong)
    
    assert result['is_strong'] is True
    assert result['has_upper'] is True
    assert result['has_lower'] is True
    assert result['has_digit'] is True
    assert result['length'] >= 8

def test_password_validation_medium(security):
    """Test: Validación de contraseña media"""
    medium = "Medium123"
    result = security.validate_password_strength(medium)
    
    # Tiene longitud, mayúsculas, minúsculas y dígitos pero puede faltar especial
    assert result['length'] >= 8
    assert result['has_upper'] is True
    assert result['has_lower'] is True
    assert result['has_digit'] is True
