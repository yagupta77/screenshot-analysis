#!/usr/bin/env python3
"""
Main entry point for the Screenshot Security Analyzer.
This script consolidates the functionality of analyze_image.py and image_analyzer.py.
"""
import os
import sys
from pathlib import Path
import logging
from ocr.extract_text import extract_text_from_image
from analysis.analyze_text import analyze_text
from analysis.utils.formatting import colorize
from analysis.utils.env_config import load_env_variables

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Enable Windows terminal colors
os.system('')

def print_banner():
    """Print the application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                 SCREENSHOT SECURITY ANALYZER              ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(colorize(banner, 'blue'))

def print_usage():
    """Print usage instructions."""
    usage = """
    Usage:
      python analyze_screenshot.py [image_path]  - Analyze text from an image
      python analyze_screenshot.py --text [file_path]  - Analyze text from a file
      python analyze_screenshot.py --help        - Show this help message
      
    Supported image formats: PNG, JPG, JPEG, BMP, GIF
    """
    print(colorize(usage, 'cyan'))

def save_extracted_text(text, output_path):
    """
    Save extracted text to a file for reference.
    
    Args:
        text: The text to save
        output_path: Path to save the text to
        
    Returns:
        Path to the saved file
    """
    with open(output_path, 'w') as f:
        f.write(text)
    logger.info(f"Extracted text saved to: {output_path}")
    return output_path

def analyze_image_file(image_path):
    """
    Analyze text from an image file.
    
    Args:
        image_path: Path to the image file
    """
    print(colorize(f"\nAnalyzing image: {image_path}\n", 'green'))
    
    try:
        # Extract text from image
        print(colorize("Extracting text from image...", 'cyan'))
        text = extract_text_from_image(str(image_path))
        
        # If text was extracted successfully
        if text:
            # Save extracted text to file
            output_file = save_extracted_text(text, f"{image_path}.txt")
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
        logger.error(f"Error analyzing image: {e}")
        print(colorize(f"\nError analyzing image: {e}", 'red'))
        print(colorize("\nTroubleshooting:", 'cyan'))
        print(colorize(" • Verify that OpenCV and Tesseract are properly installed", 'cyan'))
        print(colorize(" • Check that the image file is not corrupted", 'cyan'))
        print(colorize(" • Ensure you have sufficient permissions to read the file", 'cyan'))

def analyze_text_file(file_path):
    """
    Analyze text from a text file.
    
    Args:
        file_path: Path to the text file
    """
    print(colorize(f"\nAnalyzing file: {file_path}\n", 'green'))
    
    try:
        with open(file_path, 'r') as f:
            text = f.read()
        
        print(colorize("Analyzing text for security issues...", 'cyan'))
        print(colorize("\nSecurity Analysis Results:", 'green'))
        analysis_result = analyze_text(text)
        print(analysis_result)
        
        # Provide summary
        if "No security issues detected" in analysis_result:
            print(colorize("\nSummary: No security issues were detected in the file.", 'green'))
        else:
            print(colorize("\nSummary: Security issues were detected in the file. Review the analysis above for details.", 'yellow'))
    except Exception as e:
        logger.error(f"Error analyzing text file: {e}")
        print(colorize(f"\nError analyzing file: {e}", 'red'))

def analyze_interactive_text():
    """Analyze text entered interactively by the user."""
    print(colorize("\nEnter text to analyze (Ctrl+D or Ctrl+Z to finish):\n", 'green'))
    
    try:
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        
        if lines:
            text = '\n'.join(lines)
            print(colorize("\nAnalyzing text for security issues...", 'cyan'))
            print(colorize("\nSecurity Analysis Results:", 'green'))
            analysis_result = analyze_text(text)
            print(analysis_result)
            
            # Provide summary
            if "No security issues detected" in analysis_result:
                print(colorize("\nSummary: No security issues were detected.", 'green'))
            else:
                print(colorize("\nSummary: Security issues were detected. Review the analysis above for details.", 'yellow'))
        else:
            print(colorize("\nNo input provided.", 'yellow'))
    except KeyboardInterrupt:
        print(colorize("\nAnalysis canceled.", 'yellow'))

def main():
    """Main entry point for the application."""
    # Load environment variables
    load_env_variables()
    
    print_banner()
    
    if len(sys.argv) <= 1:
        print_usage()
        analyze_interactive_text()
        return
    
    if sys.argv[1] in ['-h', '--help']:
        print_usage()
        return
    
    if sys.argv[1] == '--text':
        if len(sys.argv) <= 2:
            print(colorize("Error: No text file specified", 'red'))
            print_usage()
            return
            
        file_path = Path(sys.argv[2])
        if not file_path.exists():
            print(colorize(f"Error: File not found: {file_path}", 'red'))
            print_usage()
            return
            
        analyze_text_file(file_path)
        return
    
    # Assume it's an image path
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
    
    analyze_image_file(image_path)

if __name__ == "__main__":
    main()
