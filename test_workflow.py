import sys
import os
import shutil
import pikepdf
from pathlib import Path

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from backend.core.workflow_engine import Workflow, WorkflowStep, ActionType
    from backend.core.workflow_executor import WorkflowExecutor
except ImportError as e:
    print(f"Error importing Core modules: {e}")
    sys.exit(1)

def create_dummy_pdf(filename):
    """Create a dummy PDF"""
    pdf = pikepdf.new()
    pdf.add_blank_page()
    pdf.save(filename)
    print(f"Created initial input: {filename}")

def progress_handler(step_id, percent):
    print(f"   [Progress] Step {step_id}: {percent}%")

def main():
    print("==================================================")
    print("TESTING CORE WORKFLOW EXECUTOR (RETRY)")
    print("==================================================")
    
    # Paths
    base_output_dir = "workflow_output_test"
    input_file = "workflow_input.pdf"
    
    # Cleanup
    if os.path.exists(base_output_dir):
        shutil.rmtree(base_output_dir)
    if os.path.exists(input_file):
        try: os.remove(input_file)
        except: pass

    try:
        # 1. Setup Input
        create_dummy_pdf(input_file)
        
        # 2. Define Workflow: Compress -> Encrypt
        # This tests passing output of Step 1 to Input of Step 2
        print("\n[Definition] Creating Workflow...")
        
        wf = Workflow()
        
        # Step 1: Compress
        step1 = WorkflowStep(ActionType.COMPRESS, {
            "input_path": os.path.abspath(input_file),
            "level": "medium"
        })
        wf.add_step(step1)
        print(f"Added Step 1: COMPRESS (ID: {step1.id})")
        
        # Step 2: Encrypt
        # Input source refers to Step 1
        step2 = WorkflowStep(ActionType.SECURITY, {
            "input_source": f"step_ref:{step1.id}",
            "mode": "encrypt",
            "password": "WorkflowPass123"
        })
        wf.add_step(step2)
        print(f"Added Step 2: SECURITY (ID: {step2.id}) -> Depends on Step 1")
        
        # 3. Initialize Executor
        executor = WorkflowExecutor()
        print("Executor initialized.")
        
        # 4. Execute
        print("\n[Execution] Running Workflow...")
        result = executor.execute_workflow(
            workflow=wf,
            base_output_dir=base_output_dir,
            progress_callback=progress_handler
        )
        
        print("\n[Result Analysis]")
        # Check overall result structure
        if result['workflow_id'] == wf.id:
            print(f"Workflow ID matches: {result['workflow_id']}")
            
            # Check results list
            steps_results = result['results']
            if len(steps_results) == 2:
                print("Correct number of steps executed (2).")
                
                # Check status
                if all(r['status'] == 'success' for r in steps_results):
                    print("All steps reported SUCCESS.")
                    
                    final_path = result['final_output']
                    print(f"Final Output Path reported: {final_path}")
                    
                    if final_path and os.path.exists(final_path):
                        print("Final output file exists.")
                        
                        # Verify encryption of final file
                        try:
                            pikepdf.open(final_path)
                            print("FAILURE: Final file opens WITHOUT password (Encryption failed?)")
                        except pikepdf.PasswordError:
                            print("SUCCESS: Final file requires password (Encryption applied).")
                            
                    else:
                        print("FAILURE: Final output file is missing.")
                else:
                    print("FAILURE: Some steps failed.")
                    print(steps_results)
            else:
                 print(f"FAILURE: Expected 2 steps in result, got {len(steps_results)}")
        
        else:
            print("FAILURE: Result Workflow ID mismatch.")

    except Exception as e:
         print(f"\nEXCEPTION: {e}")
         import traceback
         traceback.print_exc()
        
    finally:
        # Cleanup input
        if os.path.exists(input_file):
             try: os.remove(input_file)
             except: pass
        # Keep output dir for inspection
        pass

if __name__ == "__main__":
    main()
