import sys
import os
import pikepdf
from pathlib import Path

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from backend.services.pdf_compressor import PDFCompressor
except ImportError as e:
    print(f"Error importing PDFCompressor: {e}")
    sys.exit(1)

def create_dummy_pdf_with_content(filename):
    """Create a PDF with some content to have something to 'compress'"""
    # Just a simple PDF, pikepdf creates minimal PDFs by default
    pdf = pikepdf.new()
    pdf.add_blank_page()
    # We add some metadata or repetitive content if we could, but for now a blank page 
    # is enough to verify the Class executes the save command without crashing.
    pdf.save(filename)
    print(f"Created dummy PDF: {filename}")

def main():
    print("==================================================")
    print("TESTING PDF COMPRESSOR")
    print("==================================================")
    
    input_file = "dummy_to_compress.pdf"
    output_file = "compressed_output_test.pdf"
    
    # Cleanup
    for f in [input_file, output_file]:
        if os.path.join(f):
             if os.path.exists(f): 
                try: os.remove(f)
                except: pass

    try:
        # Setup
        create_dummy_pdf_with_content(input_file)
        
        compressor = PDFCompressor()
        print("PDFCompressor initialized.")
        
        # Test compression
        # Note: The current implementation seems to ignore quality_level in logic, but we pass it anyway.
        print(f"Compressing {input_file} to {output_file}...")
        
        result = compressor.compress_pdf(input_file, output_file, quality_level='medium')
        
        if result['success'] and os.path.exists(output_file):
            print("Compression reported success.")
            print(f"Original size: {result['original_size_mb']} MB")
            print(f"Compressed size: {result['compressed_size_mb']} MB")
            print(f"Savings: {result['savings_percent']}%")
            
            # Verify output is valid PDF
            try:
                with pikepdf.open(output_file) as pdf:
                    print(f"\nSUCCESS: Output is a valid PDF with {len(pdf.pages)} pages.")
            except Exception as e:
                print(f"\nFAILURE: Output file exists but is invalid: {e}")
                
        else:
            print("\nFAILURE: Compression reported failure or output missing.")

    except Exception as e:
         print(f"\nEXCEPTION: {e}")
         import traceback
         traceback.print_exc()
        
    finally:
        # Cleanup input
        if os.path.exists(input_file):
            try: os.remove(input_file)
            except: pass
        pass

if __name__ == "__main__":
    main()
