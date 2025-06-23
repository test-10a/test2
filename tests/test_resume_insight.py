from resume_insight import analyze_resume_text

def test_basic():
    txt = "Graduated 2016\nWorked at Acme 2017-2024"
    out = analyze_resume_text(txt, as_of=2025)
    assert out == {"years_experience": 9, "predicted_age": 31}
