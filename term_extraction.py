import re
import json

def extract_technical_phrases(text):
    """Extract technical terms for documentation analysis"""
    # Extract capitalized technical phrases (common in resumes)
    phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text)
    
    # Extract education section
    education = re.search(r'EDUCATION(.+?)(?=PROJECTS|CERTIFICATIONS|$)', text, re.DOTALL|re.IGNORECASE)
    education_text = education.group(1).strip() if education else ""
    
    return {
        "technical_phrases": phrases,
        "education_section": education_text
    }

# Main execution
if __name__ == "__main__":
    # This will be replaced by the agent with actual resume content
    sample_text = "PLACEHOLDER_TEXT"
    
    results = extract_technical_phrases(sample_text)
    
    with open("analysis_report.json", "w") as f:
        json.dump(results, f, indent=2)
