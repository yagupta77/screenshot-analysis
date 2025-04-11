@echo off
echo ========================================
echo    IMAGE SECURITY ANALYZER
echo ========================================
echo.

if "%~1"=="" (
    echo Usage: analyze_image.bat [image_path]
    echo.
    echo Supported image formats: PNG, JPG, JPEG, BMP, GIF
    exit /b 1
)

if not exist "%~1" (
    echo Error: Image not found: %~1
    exit /b 1
)

echo Analyzing image: %~1
echo.

echo Extracting text from image...
python -c "import sys; sys.path.append('.'); from ocr.extract_text import extract_text_from_image; text = extract_text_from_image(r'%~1'); print(text); open(r'%~1.txt', 'w').write(text)"

echo.
echo Analyzing extracted text for security issues...
echo.
echo SECURITY ANALYSIS RESULTS:
python -c "import sys; sys.path.append('.'); from analysis.analyze_text import analyze_text; text = open(r'%~1.txt', 'r').read(); print(analyze_text(text))"

echo.
echo Analysis complete. Extracted text saved to: %~1.txt
echo.
