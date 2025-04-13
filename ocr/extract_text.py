import cv2
import pytesseract
import os
import platform
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_tesseract_installation() -> bool:
    """
    Check if Tesseract OCR is installed and available.
    Returns True if available, False otherwise.
    """
    try:
        # Try to get tesseract version
        pytesseract.get_tesseract_version()
        return True
    except pytesseract.TesseractNotFoundError:
        return False
    except Exception as e:
        logger.error(f"Error checking Tesseract installation: {e}")
        return False

def configure_tesseract_path() -> None:
    """
    Configure Tesseract path based on operating system.
    """
    system = platform.system()
    
    if system == "Windows":
        # Common installation paths on Windows
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                logger.info(f"Tesseract path set to: {path}")
                return
    
    # For other systems, rely on PATH environment variable
    # which pytesseract does by default

def extract_text_from_image(image_path: str) -> Optional[str]:
    """
    Extract text from an image using OCR.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted text as string or None if extraction failed
        
    Raises:
        FileNotFoundError: If the image file doesn't exist
        RuntimeError: If Tesseract is not installed
    """
    # Check if image exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No image found at path: {image_path}")
    
    # Configure Tesseract path if needed
    configure_tesseract_path()
    
    # Check if Tesseract is installed
    if not check_tesseract_installation():
        raise RuntimeError(
            "Tesseract OCR is not installed or not found in PATH. "
            "Please install Tesseract OCR and ensure it's in your PATH, "
            "or set the correct path in the code."
        )
    
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Thresholding (optional)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # OCR
        text = pytesseract.image_to_string(thresh)
        
        # Log success
        logger.info(f"Successfully extracted text from image: {image_path}")
        
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from image: {e}")
        return None
