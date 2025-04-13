# Windows Service Configuration for Screenshot Security Analyzer

This guide provides detailed configuration options for running the Screenshot Security Analyzer as a Windows service.

## Service Configuration Options with NSSM

NSSM (Non-Sucking Service Manager) provides many configuration options to fine-tune your Windows service. Here are the key settings you can adjust:

### Application Tab
- **Path**: The full path to your batch file or Python script
- **Startup directory**: The working directory for the service
- **Arguments**: Any command-line arguments to pass to your script
- **Service name**: The name used to identify the service in Windows

### Details Tab
- **Display name**: The name shown in the Windows Services manager
- **Description**: A description of what the service does
- **Startup type**: 
  - **Automatic**: Starts when Windows boots
  - **Automatic (Delayed Start)**: Starts shortly after Windows boots
  - **Manual**: Only starts when explicitly requested
  - **Disabled**: Cannot be started

### Log On Tab
- **Log on as**: Choose whether to run as Local System or a specific user account
- **Dependencies**: Make this service dependent on other services

### Process Tab
- **Priority**: Set the CPU priority for the service
- **Process model**: Configure process isolation
- **Console window options**: Hide or show console window
- **CPU affinity**: Restrict the service to specific CPU cores

### I/O Tab
- **Standard output**: Redirect stdout to a file
- **Standard error**: Redirect stderr to a file
- **Standard input**: Specify an input file

### File Rotation Tab
- Configure log file rotation settings to prevent logs from growing too large

## Advanced Service Configuration

### Environment Variables

You can set environment variables for your service in NSSM:

1. In the NSSM service editor, go to the **Environment** tab
2. Add environment variables in the format: `VARIABLE=value`
3. For multiple variables, add one per line

Example environment variables for the Screenshot Security Analyzer:
```
PYTHONPATH=C:\Path\To\screenshot-analysis
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
WATCH_INTERVAL=60
DEBUG_MODE=False
```

### Service Recovery Options

Configure how Windows should respond if the service fails:

1. Open Windows Services manager (services.msc)
2. Right-click on your service and select "Properties"
3. Go to the "Recovery" tab
4. Configure actions for first, second, and subsequent failures:
   - Take no action
   - Restart the service
   - Run a program
   - Restart the computer
5. Set the reset fail count after X days
6. Enable "Restart service after" option with a delay if needed

### Service Security Settings

Configure service security settings:

1. Open Windows Services manager
2. Right-click on your service and select "Properties"
3. Go to the "Log On" tab
4. Choose "Local System account" or a specific user account
5. If using a specific account, ensure it has:
   - Access to the Screenshot Security Analyzer files
   - Permission to read/write to the watch and output directories
   - Sufficient privileges to run as a service

## Customizing the Service Behavior

### Watch Directory Configuration

You can customize which directories the service monitors by modifying the code or using environment variables:

```python
# Using environment variables for configuration
watch_dir = Path(os.getenv("WATCH_DIR", "watch_folder"))
processed_dir = Path(os.getenv("PROCESSED_DIR", "processed"))
results_dir = Path(os.getenv("RESULTS_DIR", "results"))
```

### Monitoring Multiple Directories

To monitor multiple directories, modify the service code:

```python
watch_directories = [
    Path("C:/Screenshots/Team1"),
    Path("C:/Screenshots/Team2"),
    Path("C:/Screenshots/Team3")
]

for watch_dir in watch_directories:
    for img_file in watch_dir.glob("*.png"):
        # Process each file
```

### File Type Filtering

Configure which file types to process:

```python
# Process multiple image formats
image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.bmp"]
for ext in image_extensions:
    for img_file in watch_dir.glob(ext):
        # Process each file
```

### Processing Interval

Adjust how frequently the service checks for new files:

```python
# Check every 5 minutes (300 seconds)
time.sleep(300)
```

## Integration with Windows Event Log

For better integration with Windows monitoring systems, log to the Windows Event Log:

```python
import win32evtlogutil
import win32evtlog

def log_to_event_log(message, event_type=win32evtlog.EVENTLOG_INFORMATION_TYPE):
    """Log a message to the Windows Event Log."""
    win32evtlogutil.ReportEvent(
        "Screenshot Security Analyzer",  # App name
        1,                              # Event ID
        eventType=event_type,           # Event type
        strings=[message]               # Message
    )

# Usage examples
log_to_event_log("Service started successfully")
log_to_event_log("Critical security issue detected", win32evtlog.EVENTLOG_ERROR_TYPE)
```

## Email Notifications

Add email notifications for critical security findings:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(subject, body, recipients):
    """Send an email alert."""
    # Load email configuration from environment variables
    smtp_server = os.getenv("SMTP_SERVER", "smtp.example.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "alerts@example.com")
    smtp_password = os.getenv("SMTP_PASSWORD", "password")
    sender = os.getenv("ALERT_SENDER", "security-alerts@example.com")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        logging.info(f"Email alert sent to {recipients}")
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

# Usage example
if "Critical" in analysis_result:
    send_email_alert(
        "Critical Security Issue Detected",
        f"Critical security issue found in {img_file.name}:\n\n{analysis_result}",
        ["security-team@example.com"]
    )
```

## Automatic Actions Based on Findings

Implement automatic actions for specific security issues:

```python
def take_action_based_on_findings(analysis_result, file_path):
    """Take automated actions based on security findings."""
    if "DDoS Attack" in analysis_result:
        # Log to event log
        log_to_event_log(f"DDoS Attack detected in {file_path}", win32evtlog.EVENTLOG_ERROR_TYPE)
        
        # Send urgent notification
        send_email_alert(
            "URGENT: DDoS Attack Detected",
            f"DDoS Attack detected in {file_path}. Immediate action required.",
            ["security-team@example.com", "network-admin@example.com"]
        )
        
        # Execute mitigation script
        subprocess.run(["C:/Scripts/ddos_mitigation.bat"], check=True)
    
    elif "Data Breach" in analysis_result:
        # Different actions for data breach
        pass
```

## Service Health Monitoring

Add a health check endpoint to monitor service status:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Service is running')
        else:
            self.send_response(404)
            self.end_headers()

def start_health_server():
    """Start a simple HTTP server for health checks."""
    server = HTTPServer(('localhost', 8080), HealthCheckHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    logging.info("Health check server started on port 8080")

# Add to service startup
start_health_server()
```

## Creating a Windows Service Directly with Python

As an alternative to NSSM, you can create a Windows service directly with Python using the `win32service` module:

```python
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import time
from pathlib import Path

class ScreenshotAnalyzerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ScreenshotAnalyzer"
    _svc_display_name_ = "Screenshot Security Analyzer"
    _svc_description_ = "Monitors and analyzes screenshots for security issues"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        # Set up paths
        base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        watch_dir = base_dir / "watch_folder"
        watch_dir.mkdir(exist_ok=True)
        processed_dir = base_dir / "processed"
        processed_dir.mkdir(exist_ok=True)
        results_dir = base_dir / "results"
        results_dir.mkdir(exist_ok=True)
        
        # Import analyzer functions
        sys.path.append(str(base_dir))
        from ocr.extract_text import extract_text_from_image
        from analysis.analyze_text import analyze_text
        
        # Main service loop
        while self.is_running:
            # Check for new files
            for img_file in watch_dir.glob("*.png"):
                try:
                    # Process file
                    text = extract_text_from_image(str(img_file))
                    analysis_result = analyze_text(text)
                    
                    # Save results
                    with open(results_dir / f"{img_file.stem}_analysis.txt", 'w') as f:
                        f.write(analysis_result)
                    
                    # Move processed file
                    img_file.rename(processed_dir / img_file.name)
                    
                except Exception as e:
                    servicemanager.LogErrorMsg(f"Error processing {img_file}: {e}")
            
            # Wait before checking again
            time.sleep(30)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ScreenshotAnalyzerService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ScreenshotAnalyzerService)
```

To install this service:
```
python screenshot_analyzer_service.py install
```

To start the service:
```
python screenshot_analyzer_service.py start
```

To stop the service:
```
python screenshot_analyzer_service.py stop
```

To remove the service:
```
python screenshot_analyzer_service.py remove
```
