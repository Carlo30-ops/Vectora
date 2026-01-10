import sys
import os
import shutil
from pathlib import Path

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from backend.services.batch_processor import BatchProcessor
except ImportError as e:
    print(f"Error importing BatchProcessor: {e}")
    sys.exit(1)

def create_dummy_file(filename):
    """Create a dummy file"""
    with open(filename, 'w') as f:
        f.write("Dummy content")
    print(f"Created file: {filename}")

def mock_operation(input_path, output_path, **kwargs):
    """
    A mock operation that simulates processing by copying the file 
    and appending '_processed' to content if it were text, 
    but here just copy is enough to prove the batch loop works.
    BatchProcessor expects the operation to handle saving to output_path.
    """
    print(f"   [MockOp] Processing {input_path} -> {output_path}")
    shutil.copy(input_path, output_path)
    return {"status": "mock_success", "extra": kwargs.get('prefix', '')}

def main():
    print("==================================================")
    print("TESTING BATCH PROCESSOR")
    print("==================================================")
    
    input_files = ["batch_file_1.txt", "batch_file_2.txt"]
    output_dir = "batch_output_test"
    
    # Cleanup previous run
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Cleaned up {output_dir}")
        
    for f in input_files:
        if os.path.exists(f): os.remove(f)

    try:
        # Setup
        for f in input_files:
            create_dummy_file(f)
            
        processor = BatchProcessor()
        print("BatchProcessor initialized.")
        
        # Test Validation
        print("\n[1] Testing Validation Logic...")
        file_paths = [os.path.abspath(f) for f in input_files]
        validation = processor.validate_batch_files(file_paths, required_extension='.txt')
        
        if validation['valid']:
            print("Validation Success.")
        else:
            print(f"Validation Failed: {validation['errors']}")
            
        # Test Execution
        print("\n[2] Execution Batch...")
        
        # We pass our mock_operation
        # config can contain anything our mock expects
        config = {'prefix': 'TEST_MODE'}
        
        result = processor.process_batch(
            file_paths=file_paths,
            operation_func=mock_operation,
            operation_config=config,
            output_dir=output_dir,
            progress_callback=lambda p, m, r: print(f"   [Progress {p}%] {m}")
        )
        
        if result['success']:
            print("\nBatch execution reported SUCCESS.")
            print(f"Processed: {result['successful']}/{result['total_files']}")
            
            # Verify outputs exist
            out_files = list(Path(output_dir).glob("*"))
            if len(out_files) == len(input_files):
                print(f"Verified {len(out_files)} output files exist.")
                print("SUCCESS: Batch Processor functional.")
            else:
                 print(f"FAILURE: Expected {len(input_files)} outputs, found {len(out_files)}.")
        else:
            print("\nFAILURE: Batch execution reported failure.")
            print(result)

    except Exception as e:
         print(f"\nEXCEPTION: {e}")
         import traceback
         traceback.print_exc()
        
    finally:
        # Cleanup input
        for f in input_files:
             try: os.remove(f)
             except: pass
        # Cleanup output? Maybe keep for inspection if failed.
        pass

if __name__ == "__main__":
    main()
