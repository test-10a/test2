import traceback
from google.cloud import storage
from error_handler import log_error

def process_resume(bucket_name="resumes", file_name="resume.pdf"):
    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        content = blob.download_as_text()
        
        if "experience" not in content:
            raise ValueError("Resume missing experience section")
            
        return "Resume processed successfully"
        
    except Exception as e:
        error_msg = f"Failed to process {file_name}: {str(e)}\n{traceback.format_exc()}"
        log_error(error_msg)  
        return "Processing failed - see debug logs"
