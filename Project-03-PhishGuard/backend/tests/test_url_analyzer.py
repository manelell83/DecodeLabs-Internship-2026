"""Unit tests for URLAnalyzer."""

from app.services.url_analyzer import URLAnalyzer


def test_detects_ip_based_url():
    hits = URLAnalyzer().analyze(["http://192.168.1.10/login"])
    assert any(h.category == "ip_based_url" for h in hits)


def test_detects_shortened_url():
    hits = URLAnalyzer().analyze(["https://bit.ly/3xample"])
    assert any(h.category == "shortened_url" for h in hits)


def test_detects_suspicious_tld():
    hits = URLAnalyzer().analyze(["http://free-prize.zip/claim"])
    assert any(h.category == "suspicious_tld" for h in hits)


def test_detects_homograph_domain():
    hits = URLAnalyzer().analyze(["http://micros0ft-support.com/verify"])
    assert any(h.category == "homograph_domain" for h in hits)


def test_clean_url_produces_no_hits():
    hits = URLAnalyzer().analyze(["https://www.example.com/about"])
    assert hits == []
