import sys
import os
import pikepdf
from pathlib import Path

# Add current directory to path to allow imports from backend
sys.path.append(os.getcwd())

try:
    from backend.services.pdf_merger import PDFMerger
except ImportError as e:
    print(f"Error importing PDFMerger: {e}")
    sys.exit(1)

def create_dummy_pdf(filename, content_text):
    """Create a simple PDF with one page using pikepdf"""
    pdf = pikepdf.new()
    pdf.add_blank_page()
    pdf.save(filename)
    print(f"Created dummy PDF: {filename}")

def main():
    print("==================================================")
    print("TESTING PDF MERGER")
    print("==================================================")
    
    # Setup
    input_files = ["dummy1.pdf", "dummy2.pdf"]
    output_file = "merged_output_test.pdf"
    
    # Cleanup previous run
    if os.path.join(output_file):
        try:
            if os.path.exists(output_file):
                os.remove(output_file)
        except:
            pass

    try:
        # Create dummy PDF files
        for f in input_files:
            create_dummy_pdf(f, f"Content for {f}")
        
        # Initialize Merger
        merger = PDFMerger()
        print("PDFMerger initialized.")
        
        # Execute Merge
        print(f"Merging {input_files} into {output_file}...")
        result = merger.merge_pdfs(input_files, output_file)
        
        # Verify
        if result['success'] and os.path.exists(output_file):
            with pikepdf.open(output_file) as pdf:
                page_count = len(pdf.pages)
                print(f"Merge successful. Output has {page_count} pages.")
                if page_count == 2:
                    print("\nSUCCESS: PDF Merger functional.")
                else:
                    print(f"\nFAILURE: Expected 2 pages, got {page_count}.")
        else:
            print(f"\nFAILURE: Merge reported failure or file not found.")

    except Exception as e:
        print(f"\nEXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        print("\nCleaning up dummy files...")
        for f in input_files:
            if os.path.exists(f): 
                try: os.remove(f) 
                except: pass
        # We assume user might want to inspect output, but for now let's keep it or delete? 
        # Let's keep output if success for user inspection, but in automated test we might delete.
        # I'll modify to keep it for user to see, but maybe just leave it be.
        pass

if __name__ == "__main__":
    main()
