# Screenshot Security Analyzer

A lightweight, powerful tool for extracting text from screenshots/images and analyzing it for security issues with actionable mitigation steps.

## Overview

The Screenshot Security Analyzer scans images for text content and analyzes it for potential security issues such as:

- DDoS attacks
- Data breaches
- Malware infections
- Brute force attempts
- SQL injection attacks
- Unauthorized access
- Suspicious traffic patterns
- Policy violations
- Resource abuse
- Network reconnaissance
- Weak passwords

For each detected issue, the tool provides severity classification and specific mitigation steps.

## Features

- **OCR Text Extraction**: Extracts text from screenshots and images
- **Pattern-based Detection**: Uses regex patterns to identify security issues in text
- **Severity Classification**: Categorizes findings by Critical, High, Medium, and Low severity
- **Actionable Mitigation**: Provides specific steps to address each security issue
- **Color-coded Output**: Enhances readability with color-coded terminal output
- **Multiple Input Methods**: Supports image files or text files

## Installation

```bash
# Clone the repository
git clone https://github.com/yagupta77/screenshot-analysis.git
cd screenshot-analysis

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (required for image text extraction)
# For Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
# For Ubuntu/Debian: sudo apt install tesseract-ocr
# For macOS: brew install tesseract
```

## Usage

### Analyzing an Image

```bash
python analyze_image.py path/to/your/image.png
```

### Analyzing a Text File

```bash
python main.py path/to/your/file.txt
```

### Interactive Text Mode

```bash
python main.py
```
Then enter the text you want to analyze. Press Ctrl+D (Unix) or Ctrl+Z (Windows) followed by Enter when finished.

## Example Output

```
┌──────────────────── Security Analysis ────────────────────┐
│ Critical Issues:
│   • DDoS Attack:
│     - Found: DDoS attack in progress - service unavailable
│     Mitigation Steps:
│       ▸ Enable DDoS protection
│       ▸ Scale infrastructure
│       ▸ Filter malicious traffic
│       ▸ Contact upstream providers
└────────────────────────────────────────────────────────────┘
```

## Project Structure

```
screenshot-analysis/
├── analysis/
│   └── analyze_text.py  # Core analysis functionality
├── ocr/
│   └── extract_text.py  # Text extraction from images
├── main.py              # Text analysis entry point
├── analyze_image.py     # Image analysis entry point
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## Requirements

The tool requires:

- Python 3.6+
- OpenCV (for image processing)
- Pytesseract (for OCR)
- Tesseract OCR (backend for pytesseract)
- Python-dotenv (for environment variables)

## Configuration

Copy the `.env.example` file to `.env` to configure optional features:
- Threat intelligence API integration
- Alert notifications (Slack, Telegram, Email)
- Automated response settings

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
