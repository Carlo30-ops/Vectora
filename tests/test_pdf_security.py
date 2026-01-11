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
        assert result.success is True

def test_decrypt_pdf(security, sample_pdf, output_path):
    """Test desencriptación de PDF"""
    pwd = "securepassword"
    
    with patch('pikepdf.open') as mock_open:
        mock_pdf = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_pdf
        
        result = security.decrypt_pdf(str(sample_pdf), output_path, pwd)
        
        mock_open.assert_called_with(str(sample_pdf), password=pwd)
        mock_pdf.save.assert_called_with(output_path)
        assert result.success is True

def test_password_validation(security):
    """Test validador de fortaleza de contraseña"""
    weak = "123"
    strong = "StrongPass1!"
    
    res_weak = security.validate_password_strength(weak)
    assert res_weak['is_strong'] is False
    assert len(res_weak['recommendations']) > 0
    
    res_strong = security.validate_password_strength(strong)
    assert res_strong['is_strong'] is True
