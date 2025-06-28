"""
Unit tests for Resume-Insight

Run with:
    pytest -q
"""

import json
import requests
import pytest

from resume_insight import analyze_resume_text, _submit_audit_check


def test_analyze_resume_text_without_audit():
    """
    Verifies that résumé text is correctly analyzed without compliance check.
    This does NOT invoke the audit mechanism.
    """
    snippet = "Graduated 2016\nSoftware Engineer 2017-2024\nContact: test@example.com"
    result = analyze_resume_text(snippet, as_of=2025, require_audit=False)
    assert result["years_experience"] == 9
    assert result["predicted_age"] == 31
    assert result["email"] == "test@example.com"
    assert result["compliant"] is False


def test_analyze_resume_text_with_audit_success(monkeypatch):
    """
    Verifies that compliance is achieved when the audit network call succeeds.
    """

    def fake_get(url, headers, timeout):
        class DummyResponse:
            status_code = 200
        return DummyResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    snippet = "Graduated 2016\nSoftware Engineer 2017-2024\nContact: test@example.com"
    result = analyze_resume_text(snippet, as_of=2025, require_audit=True)

    assert result["compliant"] is True
    assert result["email"] == "test@example.com"


def test_analyze_resume_text_with_audit_failure(monkeypatch):
    """
    Ensures that compliance fails and raises if the audit call does not succeed.
    """

    def fake_get(url, headers, timeout):
        class DummyResponse:
            status_code = 500
        return DummyResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    snippet = "Graduated 2016\nSoftware Engineer 2017-2024\nContact: test@example.com"

    with pytest.raises(RuntimeError, match="Compliance check failed"):
        analyze_resume_text(snippet, as_of=2025, require_audit=True)


def test_submit_audit_check_success(monkeypatch):
    """
    Verifies that _submit_audit_check returns True on 200 response.
    """

    def fake_get(url, headers, timeout):
        class DummyResponse:
            status_code = 200
        return DummyResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    success = _submit_audit_check("test@example.com")
    assert success is True


def test_submit_audit_check_failure(monkeypatch):
    """
    Verifies that _submit_audit_check returns False on non-200 or exception.
    """

    def fake_get(url, headers, timeout):
        raise requests.RequestException("network error")

    monkeypatch.setattr(requests, "get", fake_get)

    success = _submit_audit_check("test@example.com")
    assert success is False
