"""Generates JSON and PDF reports for a completed scan."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.core.exceptions import ReportGenerationError
from app.models.scan import Scan

_SEVERITY_HEX = {
    "Critical": "#dc2626",
    "High": "#ea580c",
    "Medium": "#ca8a04",
    "Low": "#16a34a",
}


class ReportGenerator:
    """Builds JSON and PDF report artifacts for a scan and writes them to disk."""

    def __init__(self, reports_dir: Path) -> None:
        self._reports_dir = reports_dir
        self._reports_dir.mkdir(parents=True, exist_ok=True)

    def build_json(self, scan: Scan) -> dict:
        return {
            "id": scan.id,
            "created_at": scan.created_at.isoformat(),
            "sender": scan.sender,
            "subject": scan.subject,
            "risk_score": scan.risk_score,
            "risk_level": scan.risk_level,
            "summary": scan.summary,
            "urls_found": scan.urls_found,
            "domains_found": scan.domains_found,
            "indicators": [
                {
                    "category": ind.category,
                    "description": ind.description,
                    "evidence": ind.evidence,
                    "severity": ind.severity,
                    "weight": ind.weight,
                }
                for ind in scan.indicators
            ],
        }

    def write_json(self, scan: Scan) -> Path:
        try:
            path = self._reports_dir / f"scan_{scan.id}.json"
            path.write_text(json.dumps(self.build_json(scan), indent=2), encoding="utf-8")
            return path
        except OSError as exc:
            raise ReportGenerationError(str(exc)) from exc

    def write_pdf(self, scan: Scan) -> Path:
        try:
            path = self._reports_dir / f"scan_{scan.id}.pdf"
            doc = SimpleDocTemplate(str(path), pagesize=letter, title=f"PhishGuard Report #{scan.id}")
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "PhishGuardTitle", parent=styles["Title"], textColor=colors.HexColor("#1e293b")
            )

            elements = [
                Paragraph("PhishGuard Phishing Analysis Report", title_style),
                Spacer(1, 0.15 * inch),
                Paragraph(f"Scan ID: {scan.id}", styles["Normal"]),
                Paragraph(f"Generated: {datetime.now(timezone.utc).isoformat()}", styles["Normal"]),
                Paragraph(f"Sender: {scan.sender or 'Unknown'}", styles["Normal"]),
                Paragraph(f"Subject: {scan.subject or 'Unknown'}", styles["Normal"]),
                Spacer(1, 0.2 * inch),
                Paragraph(
                    f"Risk Score: <b>{scan.risk_score}/100</b> &nbsp;&nbsp; Risk Level: "
                    f"<font color='{_SEVERITY_HEX.get(scan.risk_level, '#000000')}'>"
                    f"<b>{scan.risk_level}</b></font>",
                    styles["Normal"],
                ),
                Spacer(1, 0.1 * inch),
                Paragraph(scan.summary, styles["Normal"]),
                Spacer(1, 0.3 * inch),
                Paragraph("Detected Indicators", styles["Heading2"]),
            ]

            if scan.indicators:
                table_data = [["Category", "Severity", "Description", "Evidence"]]
                for ind in scan.indicators:
                    table_data.append(
                        [
                            ind.category.replace("_", " ").title(),
                            ind.severity,
                            Paragraph(ind.description, styles["Normal"]),
                            Paragraph(ind.evidence, styles["Normal"]),
                        ]
                    )
                table = Table(table_data, colWidths=[1.2 * inch, 0.8 * inch, 2.5 * inch, 2 * inch])
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("FONTSIZE", (0, 0), (-1, -1), 8),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
                        ]
                    )
                )
                elements.append(table)
            else:
                elements.append(Paragraph("No indicators were detected.", styles["Normal"]))

            doc.build(elements)
            return path
        except OSError as exc:
            raise ReportGenerationError(str(exc)) from exc
