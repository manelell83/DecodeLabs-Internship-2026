"""Analyzes email body text for phishing language patterns and brand impersonation."""

from __future__ import annotations

from app.services.types import IndicatorHit

_LEGITIMATE_DOMAINS: dict[str, set[str]] = {
    "microsoft": {"microsoft.com", "outlook.com", "live.com", "office.com", "office365.com"},
    "google": {"google.com", "gmail.com", "accounts.google.com"},
    "paypal": {"paypal.com", "paypal.me"},
    "banking": set(),  # generic bank keyword has no single legitimate domain set
}

_BRAND_KEYWORDS: dict[str, tuple[str, ...]] = {
    "microsoft": ("microsoft", "office 365", "onedrive", "azure ad", "microsoft account"),
    "google": ("google", "gmail", "google drive", "google account"),
    "paypal": ("paypal",),
    "banking": ("bank account", "wire transfer", "swift code", "iban", "online banking", "your bank"),
}

_URGENCY_PHRASES = (
    "act now", "immediate action required", "urgent", "within 24 hours", "account will be suspended",
    "account will be closed", "verify your account immediately", "final notice", "last warning",
    "limited time", "expires today", "immediately or", "failure to respond",
)

_CREDENTIAL_THEFT_PHRASES = (
    "confirm your password", "verify your password", "enter your credentials", "update your billing information",
    "confirm your identity", "re-enter your password", "login to verify", "click here to sign in",
    "your account has been locked", "unusual sign-in activity", "validate your account",
)

_FAKE_LOGIN_PHRASES = (
    "sign in to continue", "click below to log in", "login here to unlock", "authenticate your account",
)

_FINANCIAL_SCAM_PHRASES = (
    "processing fee", "release your funds", "unclaimed funds", "tax refund pending", "invoice attached overdue",
    "payment failed please update",
)

_LOTTERY_SCAM_PHRASES = (
    "you have won", "lottery winner", "congratulations you have been selected", "claim your prize",
    "sweepstakes winner",
)

_CRYPTO_SCAM_PHRASES = (
    "bitcoin wallet", "crypto investment", "double your bitcoin", "send btc", "wallet seed phrase",
    "guaranteed crypto returns",
)

_GIFT_CARD_SCAM_PHRASES = (
    "gift card", "itunes card", "google play card", "purchase a gift card", "send the gift card codes",
)


class ContentAnalyzer:
    """Runs keyword/pattern rule sets against the email body and sender domain."""

    def analyze(self, body: str, sender_domain: str | None) -> list[IndicatorHit]:
        text = body.lower()
        hits: list[IndicatorHit] = []

        hits.extend(self._check_brand_impersonation(text, sender_domain))
        hits.extend(self._check_phrase_group(text, _URGENCY_PHRASES, "urgency_language",
                                              "Message uses urgency or pressure tactics common in phishing.", "Medium", 6.0))
        hits.extend(self._check_phrase_group(text, _CREDENTIAL_THEFT_PHRASES, "credential_theft",
                                              "Message attempts to harvest login credentials.", "Critical", 18.0))
        hits.extend(self._check_phrase_group(text, _FAKE_LOGIN_PHRASES, "fake_login",
                                              "Message directs the recipient to a fake login page.", "High", 14.0))
        hits.extend(self._check_phrase_group(text, _FINANCIAL_SCAM_PHRASES, "financial_scam",
                                              "Message contains language typical of financial scams.", "High", 12.0))
        hits.extend(self._check_phrase_group(text, _LOTTERY_SCAM_PHRASES, "lottery_scam",
                                              "Message claims the recipient has won a prize or lottery.", "High", 12.0))
        hits.extend(self._check_phrase_group(text, _CRYPTO_SCAM_PHRASES, "crypto_scam",
                                              "Message promotes a cryptocurrency scam or investment fraud.", "High", 12.0))
        hits.extend(self._check_phrase_group(text, _GIFT_CARD_SCAM_PHRASES, "gift_card_scam",
                                              "Message requests payment via gift cards, a classic scam tactic.", "High", 13.0))

        return hits

    def _check_phrase_group(
        self,
        text: str,
        phrases: tuple[str, ...],
        category: str,
        description: str,
        severity: str,
        weight: float,
    ) -> list[IndicatorHit]:
        hits: list[IndicatorHit] = []
        for phrase in phrases:
            if phrase in text:
                hits.append(
                    IndicatorHit(
                        category=category,
                        description=description,
                        evidence=phrase,
                        severity=severity,
                        weight=weight,
                    )
                )
        return hits

    def _check_brand_impersonation(self, text: str, sender_domain: str | None) -> list[IndicatorHit]:
        hits: list[IndicatorHit] = []
        domain = (sender_domain or "").lower()

        for brand, keywords in _BRAND_KEYWORDS.items():
            mentioned = next((kw for kw in keywords if kw in text), None)
            if not mentioned:
                continue

            legit_domains = _LEGITIMATE_DOMAINS.get(brand, set())
            is_legit_sender = bool(legit_domains) and any(
                domain == legit or domain.endswith(f".{legit}") for legit in legit_domains
            )

            if brand == "banking":
                if not is_legit_sender:
                    hits.append(
                        IndicatorHit(
                            category="fake_banking",
                            description="Message references banking actions but sender is not a verifiable bank domain.",
                            evidence=mentioned,
                            severity="High",
                            weight=14.0,
                        )
                    )
                continue

            if legit_domains and not is_legit_sender:
                hits.append(
                    IndicatorHit(
                        category=f"fake_{brand}",
                        description=f"Message impersonates {brand.title()} but sender domain does not match official domains.",
                        evidence=f"{mentioned} (sender: {domain or 'unknown'})",
                        severity="Critical",
                        weight=18.0,
                    )
                )

        return hits
