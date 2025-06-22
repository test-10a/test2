from resume_analysis.analyzer import analyze_resume

if __name__ == "__main__":
    print("Running resume analysis...")
    results = analyze_resume()
    print("\nAnalysis Complete!")
    print(f"Detected skills: {results['skills']}")
