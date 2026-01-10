"""
Script de Verificación de Refactorización de Vectora (Manual Runner)
Ejecutar con: python run_refactor_verification.py
"""
import sys
import os
import shutil
from pathlib import Path

# Asegurar que el path del proyecto está en sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.services.batch_processor import BatchProcessor
from backend.services.pdf_watcher import PDFWatcherHandler
from backend.core.workflow_engine import WorkflowAssistant, Workflow, ActionType
from utils.logger import get_logger

logger = get_logger("RefactorTest")

def test_batch_processor():
    print("\n--- Testing BatchProcessor Refactor ---")
    processor = BatchProcessor(logger)
    
    # Crear archivos dummy
    test_dir = Path("temp/batch_test_input")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(parents=True, exist_ok=True)
    
    files = []
    for i in range(3):
        f = test_dir / f"test_{i}.txt"
        f.write_text(f"Dummy content {i}")
        files.append(str(f))
        
    print(f"Created {len(files)} dummy files.")
    
    # Dummy operation
    def dummy_op(input_path, output_path, **kwargs):
        Path(output_path).write_text(f"Processed: {Path(input_path).read_text()} with {kwargs}")
        return {"status": "ok"}
        
    print("Running batch process...")
    result = processor.process_batch(
        files,
        dummy_op,
        {"param": "value"},
        "temp/batch_test_output"
    )
    
    print(f"Result Type: {type(result)}")
    print(f"Success: {result.success}")
    print(f"Total: {result.total_files}")
    print(f"Successful: {result.successful_count}")
    
    if result.success and result.successful_count == 3:
        print("✅ BatchProcessor Test PASSED")
    else:
        print("❌ BatchProcessor Test FAILED")

def test_workflow_engine():
    print("\n--- Testing WorkflowEngine parsing ---")
    assistant = WorkflowAssistant()
    
    query = "Une estos archivos y luego conviértelos a Excel"
    print(f"Query: '{query}'")
    
    workflow = Workflow()
    response = assistant.handle_user_intent(query, workflow)
    
    print(f"Response: {response['message']}")
    
    steps = workflow.steps
    print(f"Steps detected: {len(steps)}")
    for s in steps:
        print(f" - Action: {s.action}, Params: {s.params}")
        
    has_merge = any(s.action == ActionType.MERGE for s in steps)
    has_convert = any(s.action == ActionType.CONVERT for s in steps)
    
    if has_merge and has_convert:
         print("✅ WorkflowEngine Parsing PASSED")
    else:
         print("❌ WorkflowEngine Parsing FAILED")
         print("Debug: Patterns checking...")
         # Debug simple
         for pat, action in assistant.patterns.items():
            import re
            print(f" Pattern '{pat}' maps to {action}")

def run_all():
    try:
        test_batch_processor()
        test_workflow_engine()
        print("\n🎉 ALL TESTS COMPLETED")
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all()
