from google.cloud import storage

def load_test_file(bucket_name="test-data", file_name="resume.txt"):
    """Loads test file from cloud storage"""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob.download_as_text()
