"""Analyzes extracted URLs for phishing-related structural red flags."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from app.services.types import IndicatorHit

_IPV4_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

_SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly",
    "rebrand.ly", "cutt.ly", "shorte.st", "rb.gy", "tiny.cc", "bl.ink",
}

_SUSPICIOUS_TLDS = {
    ".zip", ".xyz", ".top", ".click", ".gq", ".tk", ".ml", ".cf", ".ga",
    ".work", ".rest", ".fit", ".loan", ".men", ".date", ".review",
}

_BRAND_HOMOGRAPH_HINTS = (
    "micros0ft", "paypa1", "g00gle", "app1e", "amaz0n", "netfl1x", "faceb00k",
    "0utlook", "verifed", "secur1ty", "1ogin",
)


class URLAnalyzer:
    """Detects IP-literal URLs, shorteners, suspicious TLDs, and homograph tricks."""

    def analyze(self, urls: list[str]) -> list[IndicatorHit]:
        hits: list[IndicatorHit] = []
        for url in urls:
            netloc = urlparse(url).netloc.lower()
            host = netloc.split("@")[-1].split(":")[0]

            if _IPV4_PATTERN.match(host):
                hits.append(
                    IndicatorHit(
                        category="ip_based_url",
                        description="Link points directly to a raw IP address instead of a domain name.",
                        evidence=url,
                        severity="High",
                        weight=15.0,
                    )
                )

            if host in _SHORTENER_DOMAINS:
                hits.append(
                    IndicatorHit(
                        category="shortened_url",
                        description="Link uses a URL shortening service, hiding the true destination.",
                        evidence=url,
                        severity="Medium",
                        weight=10.0,
                    )
                )

            if any(host.endswith(tld) for tld in _SUSPICIOUS_TLDS):
                hits.append(
                    IndicatorHit(
                        category="suspicious_tld",
                        description="Link uses a top-level domain frequently abused for phishing campaigns.",
                        evidence=url,
                        severity="Medium",
                        weight=8.0,
                    )
                )

            if any(hint in host for hint in _BRAND_HOMOGRAPH_HINTS):
                hits.append(
                    IndicatorHit(
                        category="homograph_domain",
                        description="Link domain appears to imitate a trusted brand using character substitution.",
                        evidence=url,
                        severity="Critical",
                        weight=20.0,
                    )
                )

        return hits
