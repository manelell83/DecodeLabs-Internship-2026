"""Unit tests for ContentAnalyzer."""

from app.services.content_analyzer import ContentAnalyzer


def test_detects_urgency_language():
    hits = ContentAnalyzer().analyze("Act now or your account will be suspended.", "example.com")
    assert any(h.category == "urgency_language" for h in hits)


def test_detects_credential_theft():
    hits = ContentAnalyzer().analyze("Please confirm your password to continue.", "example.com")
    assert any(h.category == "credential_theft" for h in hits)


def test_detects_gift_card_scam():
    hits = ContentAnalyzer().analyze("Please purchase a gift card and send the codes.", "example.com")
    assert any(h.category == "gift_card_scam" for h in hits)


def test_detects_fake_microsoft_impersonation():
    hits = ContentAnalyzer().analyze("Your Microsoft account needs verification.", "totally-not-ms.xyz")
    assert any(h.category == "fake_microsoft" for h in hits)


def test_legitimate_microsoft_domain_is_not_flagged_as_fake():
    hits = ContentAnalyzer().analyze("Your Microsoft account needs verification.", "microsoft.com")
    assert not any(h.category == "fake_microsoft" for h in hits)


def test_detects_fake_banking_email():
    hits = ContentAnalyzer().analyze("Please confirm your online banking wire transfer.", "randommailer.net")
    assert any(h.category == "fake_banking" for h in hits)


def test_clean_body_produces_no_hits():
    hits = ContentAnalyzer().analyze("Hi, just checking in about tomorrow's meeting.", "example.com")
    assert hits == []
