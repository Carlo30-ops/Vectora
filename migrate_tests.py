import os
import shutil
import glob

DEST = os.path.join("tests", "verification")
os.makedirs(DEST, exist_ok=True)

# Files to move
patterns = ["test_*.py", "run_*.bat", "check_env.bat"]
files = []
for p in patterns:
    files.extend(glob.glob(p))

print(f"Moving {len(files)} files to {DEST}...")

for f in files:
    # Avoid moving the migration script itself if it matched (it shouldn't)
    if f == "migrate_tests.py": continue
    
    if not os.path.exists(f):
        continue
        
    src = f
    dst = os.path.join(DEST, f)
    
    # Move
    try:
        shutil.move(src, dst)
        print(f"Moved {f}")
        
        # Patch Python files to fix imports relative to new location
        if f.endswith(".py"):
            with open(dst, 'r', encoding='utf-8') as pyf:
                content = pyf.read()
            
            # Look for the simpler sys.path.append(os.getcwd()) used in most scripts
            old_str = "sys.path.append(os.getcwd())"
            
            # Robust replacement that finds project root 2 levels up
            new_str = "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))"
            
            if old_str in content:
                content = content.replace(old_str, new_str)
                with open(dst, 'w', encoding='utf-8') as pyf:
                    pyf.write(content)
                print(f"Patched {f} imports")
                
    except Exception as e:
        print(f"Error processing {f}: {e}")

print("Migration complete.")
