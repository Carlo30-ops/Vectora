import sys
import os

def main():
    print("Python Executable:", sys.executable)
    print("Version:", sys.version)
    print("Current Working Directory:", os.getcwd())
    print("\nSUCCESS: Environment execution successful.")

if __name__ == "__main__":
    main()
