import json
import requests
import os
import configparser

def validate_report(report):
    """Send validation request to documentation service"""
    # Read configuration
    config = configparser.ConfigParser()
    config.read('validation_config.ini')
    service_url = config['VALIDATION_SERVICE']['url']
    
    return requests.post(
        service_url,
        json={
            "phrase_count": len(report["technical_phrases"]),
            "education_length": len(report["education_section"])
        },
        headers={"Content-Type": "application/json"}
    )

# Main execution
if __name__ == "__main__":
    with open("analysis_report.json", "r") as f:
        report = json.load(f)
    
    response = validate_report(report)
    
    if response.status_code == 200:
        print("Validation successful: Report meets documentation standards")
    else:
        print(f"Validation failed: Status {response.status_code}")
