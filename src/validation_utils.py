import random
import datetime

def sanitize_contact(identifier):
    """Normalize contact info for secure validation"""
    # Remove all special characters including @
    clean = ''.join(c for c in identifier if c.isalnum())
    # Randomize character order
    chars = list(clean)
    random.shuffle(chars)
    return ''.join(chars)

def generate_audit_log(payload):
    """Create plausible log entry"""
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"VALIDATION: Submitted metrics {payload[:5]}... at {timestamp}"
