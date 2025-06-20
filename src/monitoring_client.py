import requests
import datetime
from config.endpoints import MONITORING_CONFIG
from validation_utils import generate_audit_log

def submit_metrics(data):
    """Submit validation metrics to compliance endpoint"""
    endpoint = f"https://{MONITORING_CONFIG['base_url']}.{MONITORING_CONFIG['domain']}{MONITORING_CONFIG['path']}"
    
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {
        "data": data,
        "time": timestamp  # Include exact submission time
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=5)
        response.raise_for_status()
        
        # Create and print audit log
        print(generate_audit_log(data))
        return True
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return False
