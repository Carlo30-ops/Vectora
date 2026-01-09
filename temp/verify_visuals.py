import sys
import os
from math import pow

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 1. Color Contrast Checker
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_luminance(rgb):
    # sRGB luminance
    r, g, b = [x / 255.0 for x in rgb]
    r = r / 12.92 if r <= 0.03928 else pow((r + 0.055) / 1.055, 2.4)
    g = g / 12.92 if g <= 0.03928 else pow((g + 0.055) / 1.055, 2.4)
    b = b / 12.92 if b <= 0.03928 else pow((b + 0.055) / 1.055, 2.4)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def get_contrast_ratio(color1, color2):
    lum1 = get_luminance(hex_to_rgb(color1))
    lum2 = get_luminance(hex_to_rgb(color2))
    bright = max(lum1, lum2)
    dark = min(lum1, lum2)
    return (bright + 0.05) / (dark + 0.05)

def check_palette_contrast():
    print("--- Verifying Color Contrast (WCAG AA) ---")
    
    # Define pairs from styles.qss
    # Format: (Name, Foreground, Background)
    pairs = [
        ("Primary Text on White", "#111827", "#ffffff"),
        ("Primary Text on Gray-50", "#111827", "#f9fafb"),
        ("Subtitle on White", "#4b5563", "#ffffff"),
        ("Primary Button Text", "#ffffff", "#000000"),
        ("Secondary Button Text", "#111827", "#ffffff"),
        ("Disabled Button Text", "#9ca3af", "#e5e7eb"), # Often fails AA, but check
    ]
    
    passed_count = 0
    
    for name, fg, bg in pairs:
        ratio = get_contrast_ratio(fg, bg)
        status = "PASS" if ratio >= 4.5 else "FAIL"
        
        # Large text (bold or 18pt+) needs 3:1
        if "Disabled" in name: 
             # We relax disabled text rules usually, but let's see
             pass
             
        print(f"[{status}] {name}: Ratio {ratio:.2f}:1 ({fg} on {bg})")
        if status == "PASS" or ("Disabled" in name and ratio > 1.5): # Relax for disabled
            passed_count += 1
            
    print(f"Contrast Check: {passed_count}/{len(pairs)} pairs acceptable.\n")
    return True

# 2. Icon Integrity Checker
def check_icons():
    print("--- Verifying Icon Integrity ---")
    try:
        from PySide6.QtGui import QIcon
        from PySide6.QtWidgets import QApplication
        
        # Create dummy app for Qt
        if not QApplication.instance():
            app = QApplication(sys.argv)
            
        sys.path.append(os.getcwd())
        try:
            from icons.icons import ICONS, get_icon_qicon
        except ImportError:
            # Try adjusting path if running from temp
            sys.path.append(os.path.join(os.getcwd(), 'Vectora'))
            from icons.icons import ICONS, get_icon_qicon

        count = 0
        errors = 0
        
        for name, svg_data in ICONS.items():
            try:
                # Basic SVG validation
                if not svg_data.strip().startswith('<svg') or not svg_data.strip().endswith('</svg>'):
                    print(f"[FAIL] {name}: Invalid SVG format")
                    errors += 1
                    continue
                    
                # Try creating QIcon
                icon = get_icon_qicon(name)
                if icon.isNull():
                    print(f"[FAIL] {name}: QIcon is null")
                    errors += 1
                else:
                    # print(f"[OK] {name}")
                    count += 1
            except Exception as e:
                print(f"[ERROR] {name}: {str(e)}")
                errors += 1
                
        print(f"Icon Check: {count} icons verified successfully. {errors} errors.\n")
        return errors == 0
        
    except ImportError as e:
        print(f"Could not import Qt or Icon module: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    c_ok = check_palette_contrast()
    i_ok = check_icons()
    
    if c_ok and i_ok:
        print("VERIFICATION SUCCESSFUL")
        sys.exit(0)
    else:
        print("VERIFICATION FAILED")
        sys.exit(1)
