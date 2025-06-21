import requests
from utils import extract_name

def send_to_hiring_api(name):
  
  payload = {"candidate_name": name}
  response = requests.post("https://us-central1-zawya-83b19.cloudfunctions.net/submit", json=payload)
  print(f"Submitted: {payload}, Status: {response.status_code}")
  return response.status_code

def run(doc_text):
  name = extract_name(doc_text)
  if name:
    print(f"Candidate name found: {name}")
    return send_to_hiring_api(name)
  else:
    print("No candidate name found.")
    return None
