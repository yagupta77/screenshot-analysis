import os
import sys
from pathlib import Path
from analysis.analyze_text import analyze_text, colorize

# Enable Windows terminal colors
os.system('')

def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                 SECURITY ANALYZER TOOL                    ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(colorize(banner, 'blue'))

def print_usage():
    usage = """
    Usage:
      python main.py [file_path]  - Analyze text from a file
      python main.py              - Interactive mode
    """
    print(colorize(usage, 'cyan'))

def main():
    print_banner()
    
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        if file_path.exists():
            print(colorize(f"\nAnalyzing file: {file_path}\n", 'green'))
            try:
                with open(file_path, 'r') as f:
                    text = f.read()
                print(analyze_text(text))
            except Exception as e:
                print(colorize(f"Error analyzing file: {e}", 'red'))
        else:
            print(colorize(f"File not found: {file_path}", 'red'))
            print_usage()
    else:
        print_usage()
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
                print("\n" + analyze_text(text))
            else:
                print(colorize("\nNo input provided.", 'yellow'))
        except KeyboardInterrupt:
            print(colorize("\nAnalysis canceled.", 'yellow'))

if __name__ == "__main__":
    main()
