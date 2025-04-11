# Security Analyzer Tool

A lightweight, powerful tool for analyzing text for security issues and providing actionable mitigation steps.

## Overview

The Security Analyzer Tool scans text input for potential security issues such as:

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

- **Pattern-based Detection**: Uses regex patterns to identify security issues in text
- **Severity Classification**: Categorizes findings by Critical, High, Medium, and Low severity
- **Actionable Mitigation**: Provides specific steps to address each security issue
- **Color-coded Output**: Enhances readability with color-coded terminal output
- **Multiple Input Methods**: Supports file input or interactive text entry

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/screenshot-analyzer.git
cd screenshot-analyzer

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Analyzing a File

```bash
python main.py path/to/your/file.txt
```

### Interactive Mode

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
screenshot-analyzer/
├── analysis/
│   └── analyze_text.py  # Core analysis functionality
├── ocr/
│   └── extract_text.py  # Text extraction from images (optional)
├── main.py              # Main entry point
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## Requirements

The tool has minimal dependencies:

- Python 3.6+
- Basic regex support

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
