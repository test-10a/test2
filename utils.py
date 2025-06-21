def extract_name(text):
  for line in text.splitlines():
    if line.lower().startswith("name:"):
      return line.split(":", 1)[1].strip()
  return None
