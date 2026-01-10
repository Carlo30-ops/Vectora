import sys
import os
import pikepdf
from pathlib import Path

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from backend.services.pdf_splitter import PDFSplitter
except ImportError as e:
    print(f"Error importing PDFSplitter: {e}")
    sys.exit(1)

def create_multipage_pdf(filename, pages=4):
    """Create a PDF with N blank pages"""
    with pikepdf.new() as pdf:
        for _ in range(pages):
            pdf.add_blank_page()
        pdf.save(filename)
    print(f"Created dummy PDF with {pages} pages: {filename}")

def main():
    print("==================================================")
    print("TESTING PDF SPLITTER")
    print("==================================================")
    
    input_file = "dummy_multipage.pdf"
    output_file = "split_output_test.pdf"
    
    # Cleanup
    for f in [input_file, output_file]:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

    try:
        # Setup
        create_multipage_pdf(input_file, 4)
        
        splitter = PDFSplitter()
        print("PDFSplitter initialized.")
        
        # Test split_by_range (Extract pages 2-3)
        # Note: API is 1-based indexing for start_page/end_page arguments?
        # Looking at code: 
        # split_by_range(self, input_path, output_path, start_page, end_page)
        # implementation: range(start_page - 1, end_page) -> correct for 1-based input
        
        start = 2
        end = 3
        print(f"Splitting {input_file} (Pages {start}-{end}) to {output_file}...")
        
        result = splitter.split_by_range(input_file, output_file, start, end)
        
        if result['success'] and os.path.exists(output_file):
            with pikepdf.open(output_file) as pdf:
                page_count = len(pdf.pages)
                print(f"Split successful. Output has {page_count} pages.")
                
                expected_pages = end - start + 1
                if page_count == expected_pages:
                    print("\nSUCCESS: PDF Splitter (Range) functional.")
                else:
                    print(f"\nFAILURE: Expected {expected_pages} pages, got {page_count}.")
        else:
            print("\nFAILURE: Split reported failure or output file missing.")

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
