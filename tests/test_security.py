import sys
import os
import pikepdf
from pathlib import Path

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from backend.services.pdf_security import PDFSecurity
except ImportError as e:
    print(f"Error importing PDFSecurity: {e}")
    sys.exit(1)

def create_dummy_pdf(filename):
    """Create a dummy PDF"""
    pdf = pikepdf.new()
    pdf.add_blank_page()
    pdf.save(filename)
    print(f"Created dummy PDF: {filename}")

def main():
    print("==================================================")
    print("TESTING PDF SECURITY")
    print("==================================================")
    
    input_file = "dummy_for_security.pdf"
    encrypted_file = "encrypted_test.pdf"
    decrypted_file = "decrypted_test.pdf"
    password = "MySecreTPassword123!"
    
    # Cleanup
    for f in [input_file, encrypted_file, decrypted_file]:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

    try:
        # Setup
        create_dummy_pdf(input_file)
        
        security = PDFSecurity()
        print("PDFSecurity initialized.")
        
        # 1. Test Encryption
        print(f"\n[1] Encrypting {input_file} -> {encrypted_file}")
        enc_result = security.encrypt_pdf(input_file, encrypted_file, password)
        
        if enc_result['success'] and os.path.exists(encrypted_file):
            print("Encryption reported success.")
            # Verify it is actually encrypted
            try:
                pikepdf.open(encrypted_file)
                print("FAILURE: Opened encrypted file WITHOUT password!")
            except pikepdf.PasswordError:
                print("SUCCESS: File requires password to open.")
        else:
            print("FAILURE: Encryption step failed.")
            return

        # 2. Test Decryption
        print(f"\n[2] Decrypting {encrypted_file} -> {decrypted_file}")
        dec_result = security.decrypt_pdf(encrypted_file, decrypted_file, password)
        
        if dec_result['success'] and os.path.exists(decrypted_file):
            print("Decryption reported success.")
            # Verify it opens without password
            try:
                pikepdf.open(decrypted_file)
                print("SUCCESS: Decrypted file opens without password.")
            except pikepdf.PasswordError:
                print("FAILURE: Decrypted file STILL requires password!")
        else:
             print("FAILURE: Decryption step failed.")

    except Exception as e:
         print(f"\nEXCEPTION: {e}")
         import traceback
         traceback.print_exc()
        
    finally:
        # Cleanup
        # We might want to keep files if they failed for inspection
        if os.path.exists(input_file):
             try: os.remove(input_file)
             except: pass
        pass

if __name__ == "__main__":
    main()
