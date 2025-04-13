"""
Environment variable utilities for the screenshot analysis tool.
"""
import os
import logging
from typing import Any, Dict, Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_env_variables() -> Dict[str, str]:
    """
    Load environment variables from .env file.
    
    Returns:
        Dictionary of environment variables
    """
    # Try to load from .env file
    env_loaded = load_dotenv()
    
    if env_loaded:
        logger.info("Environment variables loaded from .env file")
    else:
        logger.warning("No .env file found, using default values")
    
    return dict(os.environ)

def get_env_var(key: str, default: Any = None) -> Any:
    """
    Get environment variable with fallback to default value.
    
    Args:
        key: Environment variable name
        default: Default value if environment variable is not set
        
    Returns:
        Environment variable value or default
    """
    return os.environ.get(key, default)

def get_api_key(service_name: str) -> Optional[str]:
    """
    Get API key for a specific service.
    
    Args:
        service_name: Name of the service (e.g., 'VIRUSTOTAL', 'ABUSEIPDB')
        
    Returns:
        API key if available, None otherwise
    """
    key_name = f"{service_name.upper()}_KEY"
    api_key = get_env_var(key_name)
    
    if not api_key:
        logger.warning(f"No API key found for {service_name}")
        return None
        
    return api_key

def get_alert_settings() -> Dict[str, Any]:
    """
    Get alert configuration settings.
    
    Returns:
        Dictionary of alert settings
    """
    return {
        "slack_enabled": get_env_var("ENABLE_SLACK_ALERTS", "false").lower() == "true",
        "telegram_enabled": get_env_var("ENABLE_TELEGRAM_ALERTS", "false").lower() == "true",
        "email_enabled": get_env_var("ENABLE_EMAIL_ALERTS", "false").lower() == "true",
        "cooldown_minutes": int(get_env_var("ALERT_COOLDOWN_MINUTES", "15")),
        "max_alerts_per_hour": int(get_env_var("MAX_ALERTS_PER_HOUR", "10")),
    }

def get_threshold_settings() -> Dict[str, int]:
    """
    Get threshold configuration settings.
    
    Returns:
        Dictionary of threshold settings
    """
    return {
        "critical": int(get_env_var("CRITICAL_ALERT_THRESHOLD", "80")),
        "high": int(get_env_var("HIGH_ALERT_THRESHOLD", "60")),
        "medium": int(get_env_var("MEDIUM_ALERT_THRESHOLD", "40")),
        "low": int(get_env_var("LOW_ALERT_THRESHOLD", "20")),
    }
