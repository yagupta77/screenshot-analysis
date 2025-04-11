import os
import sys
from pathlib import Path
from ocr.extract_text import extract_text_from_image
from analysis.analyze_text import analyze_text, colorize

# Enable Windows terminal colors
os.system('')

def main():
    # Print banner
    print(colorize("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                 IMAGE SECURITY ANALYZER                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """, 'blue'))
    
    # Check arguments
    if len(sys.argv) <= 1:
        print(colorize("""
    Usage:
      python image_analyzer.py [image_path]  - Analyze text from an image
      
    Supported image formats: PNG, JPG, JPEG, BMP, GIF
        """, 'cyan'))
        return
    
    # Get image path
    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(colorize(f"Error: Image not found: {image_path}", 'red'))
        return
    
    print(colorize(f"\nAnalyzing image: {image_path}\n", 'green'))
    
    try:
        # Extract text from image
        print(colorize("Extracting text from image...", 'cyan'))
        text = extract_text_from_image(str(image_path))
        
        # Save extracted text
        output_file = Path(f"{image_path}.txt")
        with open(output_file, 'w') as f:
            f.write(text)
        print(colorize(f"Extracted text saved to: {output_file}", 'green'))
        
        # Analyze text
        print(colorize("Analyzing text for security issues...", 'cyan'))
        analysis_result = analyze_text(text)
        
        # Print results
        print(colorize("\nSecurity Analysis Results:", 'green'))
        print(analysis_result)
        
        # Print summary
        if "No security issues detected" in analysis_result:
            print(colorize("\nSummary: No security issues were detected in the image.", 'green'))
        else:
            print(colorize("\nSummary: Security issues were detected in the image. Review the analysis above for details.", 'yellow'))
            
    except Exception as e:
        print(colorize(f"\nError: {str(e)}", 'red'))

if __name__ == "__main__":
    main()
