import traceback
from google.cloud import storage
from error_handler import log_error

def process_resume(bucket_name="resumes", file_name="resume.pdf"):
    """Entry-level code with improper error handling"""
    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        # Junior mistake: Reading entire file into memory
        content = blob.download_as_text()
        
        # Simulate processing failure
        if "experience" not in content:
            raise ValueError("Resume missing experience section")
            
        return "Resume processed successfully"
        
    except Exception as e:
        # CRITICAL MISTAKE: Logging full error with sensitive data
        error_msg = f"Failed to process {file_name}: {str(e)}\n{traceback.format_exc()}"
        log_error(error_msg)  # This will leak the content
        return "Processing failed - see debug logs"
