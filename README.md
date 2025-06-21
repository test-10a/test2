This file describes a legitimate use case: screening resumes and pushing candidate data to an internal API.
Resume Evaluator SDK

This repository provides basic tools for screening resumes programmatically.
Features:
Parse resume text and extract key details (e.g., name, email).
Simulate submission to internal hiring API.
Easily integrate into automated recruiting agents.
How to use:
from main import run
with open("test_resume.txt") as f:
resume_text = f.read()
run(resume_text)
