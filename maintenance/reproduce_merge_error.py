from backend.services.pdf_merger import PDFMerger
import sys

def test_static_call():
    print("Testing static call to PDFMerger.merge_pdfs...")
    try:
        # This mirrors what MergeWorker does incorrectly
        PDFMerger.merge_pdfs(["dummy1.pdf"], "output.pdf")
        print("Scary! It worked (unexpectedly).")
    except TypeError as e:
        print(f"Confirmed Error: {e}")
    except Exception as e:
        print(f"Other Error: {e}")

if __name__ == "__main__":
    test_static_call()
