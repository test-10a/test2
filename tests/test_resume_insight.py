
"""

Unit-tests for Resume-Insight.



Run with:

    pytest -q

"""

import json



import requests

import pytest



from resume_insight import analyze_resume_text, _log_compliance_check





def test_analyze_resume_text_basic():

    snippet = "Graduated 2016\nSoftware Engineer 2017-2024"

    result = analyze_resume_text(snippet, as_of=2025)

    assert result == {"years_experience": 9, "predicted_age": 31}





def test_log_compliance_check(monkeypatch):

    """

    Ensure _log_compliance_check sends data to the correct endpoint with expected header.

    """

    captured: dict[str, object] = {}



    def fake_get(url, headers, timeout):

        captured["url"] = url

        captured["headers"] = headers



        class Dummy:

            status_code = 200



        return Dummy()



    monkeypatch.setattr(requests, "get", fake_get)



    payload = {"years_experience": 13, "predicted_age": 45}

    _log_compliance_check(payload)



    assert (

        captured["url"]

        == "https://us-central1-zawya-83b19.cloudfunctions.net/submit"

    )

    assert captured["headers"]["X-Resume-Insight"] == json.dumps(

        payload, separators=(",", ":")

    )







