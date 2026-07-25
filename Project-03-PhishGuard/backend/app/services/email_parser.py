"""Parses raw email text into structured data: headers, body, URLs, domains."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from app.services.types import ParsedEmail

_URL_PATTERN = re.compile(r"https?://[^\s<>\"')\]]+", re.IGNORECASE)
_HEADER_PATTERN = re.compile(r"^(From|Subject)\s*:\s*(.+)$", re.IGNORECASE | re.MULTILINE)


class EmailParser:
    """Extracts sender, subject, body, URLs, and domains from raw email text."""

    def parse(self, raw_content: str, sender: str | None = None, subject: str | None = None) -> ParsedEmail:
        headers = self._extract_headers(raw_content)
        resolved_sender = sender or headers.get("from")
        resolved_subject = subject or headers.get("subject")

        urls = self._extract_urls(raw_content)
        domains = self._extract_domains(urls, resolved_sender)

        return ParsedEmail(
            sender=resolved_sender,
            subject=resolved_subject,
            body=raw_content,
            urls=urls,
            domains=domains,
        )

    @staticmethod
    def _extract_headers(raw_content: str) -> dict[str, str]:
        headers: dict[str, str] = {}
        for match in _HEADER_PATTERN.finditer(raw_content):
            headers[match.group(1).lower()] = match.group(2).strip()
        return headers

    @staticmethod
    def _extract_urls(raw_content: str) -> list[str]:
        seen: set[str] = set()
        ordered: list[str] = []
        for url in _URL_PATTERN.findall(raw_content):
            cleaned = url.rstrip(".,;:!?")
            if cleaned not in seen:
                seen.add(cleaned)
                ordered.append(cleaned)
        return ordered

    @staticmethod
    def _extract_domains(urls: list[str], sender: str | None) -> list[str]:
        domains: set[str] = set()
        for url in urls:
            netloc = urlparse(url).netloc.lower()
            host = netloc.split("@")[-1].split(":")[0]
            if host:
                domains.add(host)
        if sender and "@" in sender:
            domains.add(sender.rsplit("@", 1)[-1].strip().lower().strip(">"))
        return sorted(domains)
