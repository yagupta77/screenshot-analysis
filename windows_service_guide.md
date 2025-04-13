# Running Screenshot Security Analyzer as a Windows Service

This guide will help you set up the Screenshot Security Analyzer to run as a Windows service using NSSM (Non-Sucking Service Manager).

## Prerequisites

1. Download and install the Screenshot Security Analyzer
2. Install Python 3.6+ on your Windows system
3. Install required dependencies
4. Download NSSM from https://nssm.cc/download

## Step 1: Install Required Software

### Install Python
1. Download Python from https://www.python.org/downloads/windows/
2. Run the installer and check "Add Python to PATH"
3. Complete the installation

### Install Tesseract OCR
1. Download Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer and complete the installation
3. Note the installation path (typically `C:\Program Files\Tesseract-OCR`)

### Install NSSM
1. Download NSSM from https://nssm.cc/download
2. Extract the ZIP file to a folder (e.g., `C:\Tools\nssm`)
3. Add the NSSM folder to your system PATH or remember its location

## Step 2: Set Up the Screenshot Security Analyzer

1. Clone or download the repository:
```
git clone https://github.com/yagupta77/screenshot-analysis.git
cd screenshot-analysis
```

2. Install Python dependencies:
```
pip install -r requirements.txt
```

3. Create a batch file to run the service (create `run_service.bat` in the screenshot-analysis folder):
```batch
@echo off
cd /d %~dp0
python analyze_screenshot.py --service
```

## Step 3: Create a Windows Service with NSSM

1. Open Command Prompt as Administrator
2. Navigate to the NSSM directory or use the full path
3. Run the following command:
```
nssm install ScreenshotAnalyzer
```

4. In the NSSM service installer:
   - **Path**: Browse to the `run_service.bat` file
   - **Startup directory**: Set to the screenshot-analysis folder
   - **Service name**: ScreenshotAnalyzer
   - **Description**: Screenshot Security Analyzer Service

5. Configure service details:
   - Go to the **Details** tab
   - Display name: Screenshot Security Analyzer
   - Description: Monitors and analyzes screenshots for security issues
   - Startup type: Automatic

6. Configure I/O redirection:
   - Go to the **I/O** tab
   - Output (stdout): Browse to create a log file, e.g., `C:\Path\To\screenshot-analysis\logs\service_out.log`
   - Error (stderr): Browse to create a log file, e.g., `C:\Path\To\screenshot-analysis\logs\service_err.log`

7. Click "Install service"

## Step 4: Modify the Code to Support Service Mode

You'll need to modify the `analyze_screenshot.py` file to add service functionality. Here's a sample implementation:

```python
# Add to imports
import time
import argparse
import logging
from pathlib import Path

# Add to main function or create a new function
def run_as_service():
    """Run the analyzer in service mode, monitoring a specific folder."""
    # Set up logging
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=log_dir / "service.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Configure the watch directory
    watch_dir = Path("watch_folder")
    watch_dir.mkdir(exist_ok=True)
    processed_dir = Path("processed")
    processed_dir.mkdir(exist_ok=True)
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    logging.info("Starting Screenshot Security Analyzer Service")
    logging.info(f"Watching directory: {watch_dir.absolute()}")
    
    try:
        while True:
            # Check for new files
            for img_file in watch_dir.glob("*.png"):
                try:
                    logging.info(f"Processing file: {img_file}")
                    
                    # Extract text from image
                    text = extract_text_from_image(str(img_file))
                    
                    # Save extracted text
                    text_file = results_dir / f"{img_file.stem}.txt"
                    with open(text_file, 'w') as f:
                        f.write(text)
                    
                    # Analyze the text
                    analysis_result = analyze_text(text)
                    
                    # Save analysis results
                    result_file = results_dir / f"{img_file.stem}_analysis.txt"
                    with open(result_file, 'w') as f:
                        f.write(analysis_result)
                    
                    # Move processed file
                    img_file.rename(processed_dir / img_file.name)
                    
                    logging.info(f"Completed processing: {img_file}")
                except Exception as e:
                    logging.error(f"Error processing {img_file}: {e}")
            
            # Sleep before checking again
            time.sleep(30)
    except KeyboardInterrupt:
        logging.info("Service stopped by user")
    except Exception as e:
        logging.error(f"Service error: {e}")
        raise

# Modify main function to handle service mode
def main():
    parser = argparse.ArgumentParser(description="Screenshot Security Analyzer")
    parser.add_argument("--service", action="store_true", help="Run as a Windows service")
    parser.add_argument("--text", metavar="FILE", help="Analyze text from a file")
    parser.add_argument("image", nargs="?", help="Image file to analyze")
    
    args = parser.parse_args()
    
    if args.service:
        run_as_service()
        return
        
    # Rest of your existing main function...
```

## Step 5: Start and Test the Service

1. Open Command Prompt as Administrator
2. Start the service:
```
net start ScreenshotAnalyzer
```

3. Test the service by placing PNG files in the watch_folder directory
4. Check the results in the results directory and logs in the logs directory

## Step 6: Managing the Service

- **Start the service**: `net start ScreenshotAnalyzer`
- **Stop the service**: `net stop ScreenshotAnalyzer`
- **Remove the service**: `nssm remove ScreenshotAnalyzer`

## Troubleshooting

1. Check the service logs in the logs directory
2. Verify that Python and Tesseract OCR are correctly installed
3. Ensure all required directories exist
4. Check Windows Event Viewer for service-related errors

## Additional Configuration

You can customize the service behavior by:

1. Modifying the watch interval in the `time.sleep()` call
2. Changing the watched file types (e.g., to include JPG files)
3. Adding email notifications for critical security findings
4. Implementing custom actions for specific security issues
