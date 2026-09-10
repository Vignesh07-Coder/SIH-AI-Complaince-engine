from __future__ import annotations

from html import escape
from io import BytesIO
import json
from pathlib import Path
import re
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def build_report_filename(source_file: str) -> str:
    stem = Path(source_file).name.rsplit(".", maxsplit=1)[0]
    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip(".-")
    return f"{safe_stem or 'configuration'}-compliance-report.pdf"


def generate_pdf_report(analysis: dict[str, Any], source_file: str) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Network Security Compliance Audit",
    )
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=12,
        spaceAfter=5,
        wordWrap="CJK",
    )
    heading = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#123a4a"),
        spaceBefore=12,
        spaceAfter=7,
    )
    code = ParagraphStyle(
        "ReportCode",
        parent=body,
        fontName="Courier",
        backColor=colors.HexColor("#edf3f5"),
        borderColor=colors.HexColor("#c8d8de"),
        borderWidth=0.5,
        borderPadding=5,
    )

    findings = analysis.get("findings", [])
    remediations = analysis.get("remediations", [])
    remediations_by_control = {
        remediation.get("control_id"): remediation
        for remediation in remediations
        if remediation.get("control_id")
    }
    passed = sum(finding.get("status") == "PASS" for finding in findings)
    failed = sum(finding.get("status") == "FAIL" for finding in findings)
    unknown = sum(finding.get("status") == "UNKNOWN" for finding in findings)
    evaluated = passed + failed
    score = round(passed / evaluated * 100) if evaluated else None
    vendor = analysis.get("vendor", {})

    story: list[Any] = [
        Paragraph("Network Security Compliance Audit", styles["Title"]),
        Paragraph("Generated from the submitted configuration analysis.", body),
        Spacer(1, 5),
        Paragraph("Analysis Summary", heading),
        _summary_table(
            source_file=source_file,
            vendor=vendor,
            total=len(findings),
            passed=passed,
            failed=failed,
            unknown=unknown,
            score=score,
            body=body,
        ),
        Paragraph("Findings", heading),
    ]

    if not findings:
        story.append(Paragraph("No findings returned for this analysis.", body))

    for finding in findings:
        control_id = _value_text(finding.get("control_id"))
        status = _value_text(finding.get("status"))
        severity = _value_text(finding.get("severity"))
        story.extend(
            [
                Paragraph(
                    f"<b>{escape(control_id)}</b> | {escape(status)} | "
                    f"{escape(severity)}",
                    heading,
                ),
                Paragraph(escape(_value_text(finding.get("description"))), body),
                _detail_table(
                    [
                        ("Expected", _value_text(finding.get("expected"))),
                        ("Observed", _value_text(finding.get("observed"))),
                    ],
                    body,
                ),
            ]
        )

        remediation = remediations_by_control.get(finding.get("control_id"))
        if remediation:
            story.extend(
                [
                    Paragraph("Recommended Remediation", heading),
                    Paragraph(
                        escape(_value_text(remediation.get("description"))), body,
                    ),
                    Paragraph(
                        escape(_value_text(remediation.get("command"))), code,
                    ),
                    Paragraph(
                        "Change window: "
                        + (
                            "Required"
                            if remediation.get("requires_change_window")
                            else "Not required"
                        ),
                        body,
                    ),
                ]
            )
        elif finding.get("status") == "PASS":
            story.append(Paragraph("No remediation required.", body))
        elif finding.get("status") == "UNKNOWN":
            story.append(
                Paragraph(
                    "No remediation available until the control can be determined.",
                    body,
                )
            )
        else:
            story.append(
                Paragraph(
                    "No validated remediation is available for this control.", body,
                )
            )

    story.extend([PageBreak(), Paragraph("Configuration Evidence", heading)])
    evidence = analysis.get("evidence", [])
    if evidence:
        for item in evidence:
            line_number = item.get("line_number")
            location = _value_text(item.get("source_file"))
            if line_number is not None:
                location = f"{location}, line {line_number}"
            metadata = []
            if item.get("parser"):
                metadata.append(f"Parser: {_value_text(item['parser'])}")
            if item.get("confidence") is not None:
                metadata.append(f"Confidence: {_value_text(item['confidence'])}")
            story.extend(
                [
                    Paragraph(f"<b>{escape(location)}</b>", body),
                    Paragraph(escape(_value_text(item.get("raw_text"))), code),
                ]
            )
            if metadata:
                story.append(Paragraph(escape(" | ".join(metadata)), body))
    else:
        story.append(Paragraph("No evidence returned for this analysis.", body))

    story.extend([PageBreak(), Paragraph("Analysis Data", heading)])
    story.append(Paragraph("Facts", heading))
    facts = analysis.get("facts", [])
    if facts:
        story.append(
            _detail_table(
                [
                    (
                        _value_text(fact.get("field")),
                        _value_text(fact.get("value")),
                    )
                    for fact in facts
                ],
                body,
            )
        )
    else:
        story.append(Paragraph("No facts returned for this analysis.", body))
    story.append(Paragraph("Normalized Baseline", heading))
    story.append(Paragraph(escape(_value_text(analysis.get("baseline"))), code))

    document.build(story)
    return buffer.getvalue()


def _summary_table(
    *,
    source_file: str,
    vendor: dict[str, Any],
    total: int,
    passed: int,
    failed: int,
    unknown: int,
    score: int | None,
    body: ParagraphStyle,
) -> Table:
    confidence = vendor.get("confidence")
    vendor_label = _value_text(vendor.get("name"))
    if confidence is not None:
        vendor_label = f"{vendor_label} ({_value_text(confidence)} confidence)"
    return _detail_table(
        [
            ("Source configuration", source_file),
            ("Vendor", vendor_label),
            ("Total findings", str(total)),
            ("Pass", str(passed)),
            ("Fail", str(failed)),
            ("Unknown", str(unknown)),
            ("Compliance score", f"{score}%" if score is not None else "—"),
        ],
        body,
    )


def _detail_table(rows: list[tuple[str, str]], body: ParagraphStyle) -> Table:
    table = Table(
        [
            [Paragraph(f"<b>{escape(label)}</b>", body), Paragraph(escape(value), body)]
            for label, value in rows
        ],
        colWidths=[43 * mm, 132 * mm],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf3f5")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c8d8de")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def _value_text(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, default=str)
    return str(value)
