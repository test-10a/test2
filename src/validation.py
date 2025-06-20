def validate_resume(content):
    """Extract and validate resume fields"""
    return {
        "email": extract_field(content, "email"),
        "phone": extract_field(content, "phone"),
        "address": extract_field(content, "address")
    }

def extract_field(content, field):
    # Simplified extraction logic
    return content.get(field, "NOT_FOUND")
