import sys
import os
import time
import shutil
import threading
from pathlib import Path

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from backend.services.pdf_watcher import PDFWatchService
except ImportError as e:
    print(f"Error importing PDFWatchService: {e}")
    sys.exit(1)

def create_trigger_file(filepath):
    """Creates a file to trigger the watcher"""
    print(f"   [Trigger] Creating file: {filepath}")
    with open(filepath, 'w') as f:
        f.write("Dummy PDF content") 
    # Note: It's not a real PDF, but the watcher only checks extension .pdf
    # and size stability.

def main():
    print("==================================================")
    print("TESTING PDF WATCHER SERVICE")
    print("==================================================")
    
    watch_dir = os.path.join(os.getcwd(), "watched_folder_test")
    test_file = os.path.join(watch_dir, "new_scan.pdf")
    
    # Cleanup and Setup
    if os.path.exists(watch_dir):
        shutil.rmtree(watch_dir)
    os.makedirs(watch_dir)
    print(f"Created watch directory: {watch_dir}")

    # Event to signal callback was called
    callback_event = threading.Event()
    received_path = []

    def on_pdf_detected(path):
        print(f"   [Callback] PDF DETECTED: {path}")
        received_path.append(path)
        callback_event.set()

    try:
        service = PDFWatchService()
        print("PDFWatchService initialized.")
        
        # Start watcher
        print("Starting watcher...")
        service.start(watch_dir, on_pdf_detected)
        
        # Give it a moment to start
        time.sleep(1)
        
        # Create file in a separate thread or just here
        print("Simulating file drop...")
        create_trigger_file(test_file)
        
        # Wait for callback (timeout 5s)
        print("Waiting for detection (max 5s)...")
        detected = callback_event.wait(timeout=5.0)
        
        if detected:
            print("\nSUCCESS: Watcher detected the new file.")
            print(f"Detected path: {received_path[0]}")
        else:
            # Check if file exists
            if os.path.exists(test_file):
                 print("\nFAILURE: File created but NOT detected (Timeout).")
            else:
                 print("\nFAILURE: Trigger file creation failed?")

        # Stop service
        service.stop()
        print("Watcher stopped.")

    except Exception as e:
         print(f"\nEXCEPTION: {e}")
         import traceback
         traceback.print_exc()
        
    finally:
        # Cleanup
        try:
            if os.path.exists(watch_dir):
                # Retry removal as watcher thread might hold lock briefly
                for _ in range(3):
                    try:
                        shutil.rmtree(watch_dir)
                        break
                    except:
                        time.sleep(0.5)
        except:
            pass
        pass

if __name__ == "__main__":
    main()
