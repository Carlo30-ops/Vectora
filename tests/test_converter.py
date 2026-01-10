import sys
import os
from pathlib import Path
from PIL import Image

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from backend.services.pdf_converter import PDFConverter
except ImportError as e:
    print(f"Error importing PDFConverter: {e}")
    sys.exit(1)

def create_dummy_image(filename):
    """Create a simple RGB image"""
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save(filename)
    print(f"Created dummy image: {filename}")

def main():
    print("==================================================")
    print("TESTING PDF CONVERTER")
    print("==================================================")
    
    input_image = "dummy_image.png"
    output_pdf = "images_to_pdf_test.pdf"
    
    # Cleanup
    for f in [input_image, output_pdf]:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

    try:
        # Setup
        create_dummy_image(input_image)
        
        converter = PDFConverter()
        print("PDFConverter initialized.")
        
        # Test Images -> PDF (Safest test without external deps like Poppler installed in system path)
        print(f"Converting [{input_image}] to {output_pdf}...")
        
        result = converter.images_to_pdf([input_image], output_pdf)
        
        if result['success'] and os.path.exists(output_pdf):
            print("Conversion reported success.")
            print(f"Message: {result['message']}")
            
            # Verify file size > 0
            if os.path.getsize(output_pdf) > 0:
                print("\nSUCCESS: PDF created from images.")
            else:
                print("\nFAILURE: Output PDF is empty.")
                
        else:
            print("\nFAILURE: Conversion reported failure or output missing.")

    except Exception as e:
         print(f"\nEXCEPTION: {e}")
         # import traceback
         # traceback.print_exc()
        
    finally:
        # Cleanup input
        if os.path.exists(input_image):
            try: os.remove(input_image)
            except: pass
        pass

if __name__ == "__main__":
    main()
