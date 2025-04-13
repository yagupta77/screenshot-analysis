"""
Utility functions for color formatting and text cleaning
"""

# ANSI color codes for output formatting
COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'cyan': '\033[96m',
    'blue': '\033[94m',
    'reset': '\033[0m'
}

def colorize(text: str, color: str) -> str:
    """Add color to console output."""
    return f"{COLORS[color]}{text}{COLORS['reset']}"

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    import re
    # Process each line separately to maintain structure
    lines = []
    for line in text.split('\n'):
        # Remove log level tags
        line = re.sub(r'\[.*?\]\s*', '', line)
        if line.strip():
            lines.append(line.strip())
    return '\n'.join(lines)
