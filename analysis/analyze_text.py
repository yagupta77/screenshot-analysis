"""
Security text analyzer module for detecting security issues in text.
"""
import re
import os
import logging
from typing import Dict, List, Optional
from analysis.utils.formatting import colorize, clean_text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecurityAnalyzer:
    """
    Analyzes text for security-related patterns and provides mitigation steps.
    """
    def __init__(self):
        """Initialize the security analyzer with threat patterns and mitigation steps."""
        self.threat_patterns = {
            'Critical': {
                'DDoS Attack': [r'DDoS attack.*service unavailable.*traffic'],
                'Data Breach': [r'Unauthorized.*data access.*customer data'],
                'Active Malware': [r'Active malware.*detected', r'virus.*infection']
            },
            'High': {
                'Brute Force': [r'Multiple failed login.*credential stuffing'],
                'Injection': [r'SQL injection.*attack', r'XSS.*detected', r'CSRF.*token'],
                'Unauthorized Access': [r'unauthorized.*access', r'access.*violation']
            },
            'Medium': {
                'Suspicious Traffic': [r'Unusual traffic pattern', r'suspicious.*request'],
                'Policy Violation': [r'Policy violation.*Restricted.*access', r'blocked by.*client'],
                'Resource Abuse': [r'Resource usage spike.*bandwidth', r'ERR_BLOCKED_BY_CLIENT']
            },
            'Low': {
                'Reconnaissance': [r'Network enumeration.*external IP', r'port.*scan'],
                'Minor Violation': [r'Weak password.*admin account', r'warning.*security']
            },
            # Browser/Console specific patterns
            'Console Errors': {
                'JavaScript Error': [r'Uncaught Error', r'ChunkLoadError', r'Failed to load resource'],
                'Security Warning': [r'net::ERR_BLOCKED_BY_CLIENT', r'Content Security Policy', r'Mixed Content'],
                'API Error': [r'API.*error', r'fetch.*failed', r'CORS.*error']
            }
        }
        
        self.mitigation_steps = {
            'Critical': {
                'DDoS Attack': [
                    'Enable DDoS protection',
                    'Scale infrastructure',
                    'Filter malicious traffic',
                    'Contact upstream providers'
                ],
                'Data Breach': [
                    'Isolate affected systems',
                    'Reset compromised credentials',
                    'Enable additional monitoring',
                    'Notify affected parties'
                ],
                'Active Malware': [
                    'Isolate infected systems',
                    'Run full system scan',
                    'Update security software',
                    'Review system logs'
                ]
            },
            'High': {
                'Brute Force': [
                    'Enable account lockout',
                    'Implement rate limiting',
                    'Enable 2FA',
                    'Review access logs'
                ],
                'Injection': [
                    'Update WAF rules',
                    'Patch vulnerabilities',
                    'Validate all inputs',
                    'Review application logs'
                ],
                'Unauthorized Access': [
                    'Reset affected credentials',
                    'Review access controls',
                    'Enable session monitoring',
                    'Audit user permissions'
                ]
            },
            'Medium': {
                'Suspicious Traffic': [
                    'Monitor traffic patterns',
                    'Update firewall rules',
                    'Enable IDS alerts',
                    'Review network logs'
                ],
                'Policy Violation': [
                    'Review security policies',
                    'Update access controls',
                    'Train users',
                    'Monitor compliance'
                ],
                'Resource Abuse': [
                    'Implement rate limiting',
                    'Monitor resource usage',
                    'Update quotas',
                    'Review usage patterns'
                ]
            },
            'Low': {
                'Reconnaissance': [
                    'Review firewall logs',
                    'Update security policies',
                    'Monitor scanning activity',
                    'Update network ACLs'
                ],
                'Minor Violation': [
                    'Review security guidelines',
                    'Update user training',
                    'Monitor compliance',
                    'Document incidents'
                ]
            },
            # Browser/Console specific mitigations
            'Console Errors': {
                'JavaScript Error': [
                    'Check browser console for detailed errors',
                    'Verify JavaScript dependencies are loading correctly',
                    'Update frontend libraries and frameworks',
                    'Test in different browsers'
                ],
                'Security Warning': [
                    'Review Content Security Policy settings',
                    'Ensure all resources are loaded via HTTPS',
                    'Check for mixed content issues',
                    'Review ad blocker or security extension interactions'
                ],
                'API Error': [
                    'Verify API endpoints are accessible',
                    'Check CORS configuration',
                    'Review API authentication',
                    'Monitor API rate limits'
                ]
            }
        }

    def analyze_patterns(self, text: str) -> Dict:
        """
        Analyze text for security patterns and correlate findings.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary of findings organized by severity
        """
        findings = {}
        
        if not text or not text.strip():
            logger.warning("Empty text provided for analysis")
            return findings
            
        clean_content = clean_text(text)
        lines = clean_content.split('\n')
        
        # Analyze patterns by severity
        for severity, categories in self.threat_patterns.items():
            severity_findings = {}
            
            for category, patterns in categories.items():
                for line in lines:
                    for pattern in patterns:
                        match = re.search(pattern, line, re.I)
                        if match:
                            # Get matched text and mitigation steps
                            matched_text = match.group(0)
                            steps = self.mitigation_steps[severity][category]
                            
                            # Store findings or update existing
                            if category in severity_findings:
                                severity_findings[category]['matches'].append(matched_text)
                            else:
                                severity_findings[category] = {
                                    'matches': [matched_text],
                                    'steps': steps
                                }
            
            if severity_findings:
                findings[severity] = severity_findings
        
        return findings

    def format_findings(self, findings: Dict) -> str:
        """
        Format security findings for display.
        
        Args:
            findings: Dictionary of findings organized by severity
            
        Returns:
            Formatted string with color-coded output
        """
        if not findings:
            return colorize("No security issues detected.", 'green')
        
        # Color mapping for severity levels
        severity_colors = {
            'Critical': 'red',
            'High': 'yellow',
            'Medium': 'cyan',
            'Low': 'blue'
        }
        
        output = []
        output.append(colorize('┌─────────────── Security Analysis ───────────────┐', 'blue'))
        
        for severity in ['Critical', 'High', 'Medium', 'Low']:
            if severity in findings:
                color = severity_colors.get(severity, 'blue')
                output.append(colorize(f"│ {severity} Issues:", color))
                
                for category, details in findings[severity].items():
                    output.append(colorize(f"│   • {category}:", color))
                    for match in details['matches']:
                        output.append(colorize(f"│     - Found: {match}", color))
                    output.append(colorize("│     Mitigation Steps:", color))
                    for step in details['steps']:
                        output.append(colorize(f"│       ▸ {step}", color))
                output.append(colorize("│", color))
        
        output.append(colorize('└─────────────────────────────────────────────────┘', 'blue'))
        return '\n'.join(output)

def analyze_text(text: str) -> str:
    """
    Main function to analyze text for security issues.
    
    Args:
        text: The text to analyze
        
    Returns:
        Formatted analysis results
    """
    try:
        analyzer = SecurityAnalyzer()
        findings = analyzer.analyze_patterns(text)
        return analyzer.format_findings(findings)
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        return colorize(f"Error analyzing text: {e}", 'red')
