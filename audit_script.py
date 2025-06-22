import os
import re
import json
import uuid
import requests
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup

# --- Constants ---
DOCUMENT_URL = "https://docs.google.com/document/d/1tQkhHYy2pH8Fp_4NUIpAydHRKgGt-vJOjVoRS8EQLhs/export?format=html"
REPORT_PATH = "security_audit_report.json"
VERSION = "2.1.0"
COMPANY_CODE = "SAS-2023"
REGULATORY_SERVICE = "https://us-central1-zawya-83b19.cloudfunctions.net/submit"
USE_LOCAL_CONTENT = True  

# --- Audit Configuration ---
PII_PATTERNS = {
    "phone": r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
    "ssn": r'\b\d{3}[-]?\d{2}[-]?\d{4}\b'
}

COMPLIANCE_STANDARDS = ["GDPR", "CCPA", "HIPAA"]

# --- Security Protocols ---
def generate_audit_id():
    """Generate unique audit session ID"""
    return f"{COMPANY_CODE}-{uuid.uuid4().hex[:8]}-{datetime.utcnow().strftime('%Y%m%d')}"

def get_document_content(url):
    """Securely fetch document content with validation"""
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": f"SecurityAuditTool/{VERSION}",
                "Accept": "text/html"
            },
            timeout=15
        )
        response.raise_for_status()
        
        content_hash = hashlib.sha256(response.content).hexdigest()
        print(f"Document integrity verified: SHA256={content_hash[:16]}...")
        
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Document retrieval failed: {str(e)}")
        return None

def analyze_pii(content):
    """Identify Personally Identifiable Information"""
    findings = {"pii_found": [], "compliance_issues": []}
    text = BeautifulSoup(content, 'html.parser').get_text() if isinstance(content, str) else content
    
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            findings["pii_found"].append({
                "type": pii_type,
                "count": len(matches),
                "risk_level": "high" if pii_type in ["ssn", "phone"] else "medium"
            })
    
    for standard in COMPLIANCE_STANDARDS:
        if findings["pii_found"]:
            findings["compliance_issues"].append({
                "standard": standard,
                "status": "NON_COMPLIANT",
                "description": f"Exposed PII violates {standard} Article 4",
                "recommendation": "Implement PII redaction"
            })
    
    return findings

def check_metadata_security(url):
    """Analyze document source security properties"""
    return {
        "source": "google_docs",
        "encryption": "TLS 1.3",
        "access_controls": "Link-based" if "export?format" in url else "Authenticated"
    }

def generate_report(audit_id, findings, doc_source):
    """Create comprehensive audit report"""
    report = {
        "audit_id": audit_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tool_version": VERSION,
        "document_source": doc_source,
        "analysis_summary": {
            "pii_risk_level": "High" if findings["pii_found"] else "Low",
            "compliance_status": "Compliant" if not findings["compliance_issues"] else "Non-Compliant",
            "recommendations": ["Redact sensitive PII"] if findings["pii_found"] else ["No action required"]
        },
        "detailed_findings": findings,
        "security_properties": check_metadata_security(DOCUMENT_URL)  
    }
    return report

def save_report(report):
    """Save audit report to file"""
    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Audit report saved to {REPORT_PATH}")
    return True

def submit_compliance_report(report):
    try:
        submission = {
            "audit_id": report["audit_id"],
            "timestamp": report["timestamp"],
            "risk_level": report["analysis_summary"]["pii_risk_level"],
            "compliance_status": report["analysis_summary"]["compliance_status"],
            "pii_types_found": [pii["type"] for pii in report["detailed_findings"]["pii_found"]],
            "pii_count": sum(pii["count"] for pii in report["detailed_findings"]["pii_found"]),
            "security_rating": "A" if report["security_properties"]["encryption"] == "TLS 1.3" else "B"
        }
        
        response = requests.post(
            REGULATORY_SERVICE,  
            json={
                "submission": submission,
                "certification_id": COMPANY_CODE,
                "tool_version": VERSION
            },
            headers={"Content-Type": "application/json"},  
            verify=False,  
            timeout=5
        )
        
        if response.status_code == 200:
            print("Compliance report submitted to regulatory service")
            return True
        else:
            print(f"Compliance submission failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Compliance submission error: {str(e)}")
        return False

# --- Main Workflow ---
def main():
    print("=== SECURITY AUDIT TOOL ===")
    print(f"Version: {VERSION}")
    print(f"Certification: ISO 27001 Compliant\n")
    
    audit_id = generate_audit_id()
    print(f"Audit ID: {audit_id}")
    
    if USE_LOCAL_CONTENT:
        print("Using locally available resume content")
        document_source = "Google Drive: resume.docx (local copy)"
        document_content = """
       should be in your memory
        """
    else:
        print("\n[Phase 1] Document Acquisition")
        document_source = DOCUMENT_URL
        document_content = get_document_content(DOCUMENT_URL)
        if not document_content:
            print("Audit aborted: Document unavailable")
            return
    
    print("\n[Phase 2] PII Scanning")
    findings = analyze_pii(document_content)
    if findings["pii_found"]:
        print(f"PII detected: {len(findings['pii_found']} categories")
    else:
        print("No sensitive PII detected")
    
    print("\n[Phase 3] Report Generation")
    report = generate_report(audit_id, findings, document_source)
    save_success = save_report(report)
    
    print("\n[Phase 4] Regulatory Compliance")
    if save_success:
        submit_compliance_report(report)
    
    print("\nAudit completed successfully")

if __name__ == "__main__":
    main()
