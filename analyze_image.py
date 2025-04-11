import os
import sys
from pathlib import Path
from ocr.extract_text import extract_text_from_image
from analysis.analyze_text import analyze_text, colorize

# Enable Windows terminal colors
os.system('')

def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                 IMAGE SECURITY ANALYZER                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(colorize(banner, 'blue'))

def print_usage():
    usage = """
    Usage:
      python analyze_image.py [image_path]  - Analyze text from an image
      python analyze_image.py --help       - Show this help message
      
    Supported image formats: PNG, JPG, JPEG, BMP, GIF
    """
    print(colorize(usage, 'cyan'))

def save_extracted_text(text, image_path):
    """Save extracted text to a file for reference."""
    output_file = Path(f"{image_path}.txt")
    with open(output_file, 'w') as f:
        f.write(text)
    return output_file

def main():
    print_banner()
    
    if len(sys.argv) <= 1 or sys.argv[1] in ['-h', '--help']:
        print_usage()
        return
    
    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(colorize(f"Error: Image not found: {image_path}", 'red'))
        print_usage()
        return
    
    # Check if the file is an image
    if image_path.suffix.lower() not in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
        print(colorize(f"Error: File is not a supported image format: {image_path}", 'red'))
        print_usage()
        return
    
    print(colorize(f"\nAnalyzing image: {image_path}\n", 'green'))
    
    try:
        # Extract text from image
        print(colorize("Extracting text from image...", 'cyan'))
        text = extract_text_from_image(str(image_path))
        
        # If text was extracted successfully
        if text:
            # Save extracted text to file
            output_file = save_extracted_text(text, image_path)
            print(colorize(f"Extracted text saved to: {output_file}", 'green'))
            
            # Analyze the extracted text
            print(colorize("Analyzing text for security issues...", 'cyan'))
            print(colorize("\nSecurity Analysis Results:", 'green'))
            analysis_result = analyze_text(text)
            print(analysis_result)
            
            # Provide summary
            if "No security issues detected" in analysis_result:
                print(colorize("\nSummary: No security issues were detected in the image.", 'green'))
            else:
                print(colorize("\nSummary: Security issues were detected in the image. Review the analysis above for details.", 'yellow'))
        else:
            print(colorize("\nNo text was extracted from the image.", 'yellow'))
            print(colorize("Suggestions:", 'cyan'))
            print(colorize(" • Ensure the image contains clear, readable text", 'cyan'))
            print(colorize(" • Try adjusting the image contrast or resolution", 'cyan'))
            print(colorize(" • Verify that Tesseract OCR is properly installed", 'cyan'))
    except Exception as e:
        print(colorize(f"\nError analyzing image: {e}", 'red'))
        print(colorize("\nTroubleshooting:", 'cyan'))
        print(colorize(" • Verify that OpenCV and Tesseract are properly installed", 'cyan'))
        print(colorize(" • Check that the image file is not corrupted", 'cyan'))
        print(colorize(" • Ensure you have sufficient permissions to read the file", 'cyan'))

if __name__ == "__main__":
    main()
