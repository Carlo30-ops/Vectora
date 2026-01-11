@echo off
echo Cleaning up legacy test files...

del tests\test_merger.py 2>nul
del tests\test_splitter.py 2>nul
del tests\test_compressor.py 2>nul
del tests\test_converter.py 2>nul
del tests\test_security.py 2>nul
del tests\test_batch.py 2>nul
del tests\test_ocr.py 2>nul

echo Cleanup complete.
