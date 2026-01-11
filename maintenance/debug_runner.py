import sys
from PySide6.QtWidgets import QApplication

def launch_widget(widget_name):
    print(f"[INFO] Initializing Application for {widget_name}...")
    app = QApplication(sys.argv)
    
    widget = None
    
    try:
        if widget_name == "security":
            from ui.components.operation_widgets.security_widget import SecurityWidget
            widget = SecurityWidget()
        elif widget_name == "merge":
            from ui.components.operation_widgets.merge_widget import MergeWidget
            widget = MergeWidget()
        elif widget_name == "split":
            from ui.components.operation_widgets.split_widget import SplitWidget
            widget = SplitWidget()
        elif widget_name == "ocr":
            from ui.components.operation_widgets.ocr_widget import OCRWidget
            widget = OCRWidget()
        elif widget_name == "compress":
            from ui.components.operation_widgets.compress_widget import CompressWidget
            widget = CompressWidget()
        # Add other widgets here as needed
        else:
            print(f"[ERROR] Unknown widget: {widget_name}")
            return
            
        print(f"[INFO] Launching {widget_name} widget...")
        widget.resize(900, 700)
        widget.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"[ERROR] Failed to launch widget: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_runner.py <widget_name>")
        print("Available: security, merge, split, ocr, compress")
    else:
        launch_widget(sys.argv[1])
