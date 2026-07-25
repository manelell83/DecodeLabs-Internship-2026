"""Maps triggered indicator categories to actionable recommendations."""

from __future__ import annotations

from app.services.types import CategorizedIndicator

_RECOMMENDATIONS: dict[str, str] = {
    "ip_based_url": "Never click links that resolve directly to an IP address; hover to inspect the true destination first.",
    "shortened_url": "Expand shortened links using a preview tool before clicking, or avoid them entirely.",
    "suspicious_tld": "Treat links using uncommon or high-abuse top-level domains with caution.",
    "homograph_domain": "Carefully compare the domain to the real brand's domain — look for substituted characters.",
    "urgency_language": "Be skeptical of messages pressuring immediate action; legitimate organizations rarely demand urgency.",
    "credential_theft": "Never enter your password via an emailed link — navigate to the site directly instead.",
    "fake_login": "Do not log in through links in unsolicited emails; go to the official site manually.",
    "financial_scam": "Verify any financial request through an independent, trusted channel before acting.",
    "lottery_scam": "Legitimate lotteries do not contact winners by unsolicited email — this is almost certainly a scam.",
    "crypto_scam": "Be extremely wary of unsolicited cryptocurrency investment offers promising guaranteed returns.",
    "gift_card_scam": "No legitimate company or agency requests payment via gift cards — this is a strong scam signal.",
    "fake_microsoft": "Confirm Microsoft communications only through accounts.microsoft.com, not email links.",
    "fake_google": "Confirm Google account alerts only by navigating directly to myaccount.google.com.",
    "fake_paypal": "Verify PayPal notices by logging in directly at paypal.com, never via email links.",
    "fake_banking": "Contact your bank directly using the number on your card, not any number or link in this email.",
}

_DEFAULT_RECOMMENDATION = "Report this email to your security team and avoid interacting with any links or attachments."


class RecommendationEngine:
    """Generates a de-duplicated, ordered list of recommendations from indicators."""

    def generate(self, indicators: list[CategorizedIndicator]) -> list[str]:
        if not indicators:
            return ["No suspicious indicators were found, but always remain cautious with unexpected emails."]

        seen: set[str] = set()
        recommendations: list[str] = []
        for hit in indicators:
            text = _RECOMMENDATIONS.get(hit.category)
            if text and text not in seen:
                seen.add(text)
                recommendations.append(text)

        recommendations.append(_DEFAULT_RECOMMENDATION)
        return recommendations
