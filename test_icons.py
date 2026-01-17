#!/usr/bin/env python3
"""Test script to verify icon loading"""

from icons.icons import get_icon_qicon, get_icon_svg, list_available_icons

print("Testing Icon System")
print("=" * 50)

# List available icons
print("\nAvailable icons:")
icons = list_available_icons()
for icon in icons:
    print(f"  - {icon}")

print(f"\nTotal: {len(icons)} icons")

# Test specific icons
test_icons = ['combine', 'scissors', 'archive', 'wand-2']
print("\n\nTesting specific icons:")
print("=" * 50)

for icon_name in test_icons:
    print(f"\nIcon: {icon_name}")
    
    # Test SVG loading
    svg = get_icon_svg(icon_name)
    print(f"  SVG loaded: {len(svg)} bytes")
    print(f"  SVG starts with: {svg[:50]}...")
    
    # Test QIcon creation
    icon = get_icon_qicon(icon_name, color="#FFFFFF")
    print(f"  QIcon created: {not icon.isNull()}")
    if not icon.isNull():
        print(f"  Icon sizes available: {icon.availableSizes()}")
    
    # Test with different color
    icon_black = get_icon_qicon(icon_name, color="#000000")
    print(f"  QIcon (black) created: {not icon_black.isNull()}")

print("\n" + "=" * 50)
print("Icon system test completed!")
