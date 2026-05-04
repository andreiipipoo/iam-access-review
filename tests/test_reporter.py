import json
from pathlib import Path

from src.reporter import generate_report


def test_generate_report_creates_file(tmp_path):
    findings = {"inactive_users": [], "privilege_escalation": [], "mfa_enforcement": []}
    out_dir = tmp_path / "reports"
    filename = generate_report(findings, output_dir=str(out_dir))

    p = Path(filename)
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "generated_at" in data
    assert data["summary"]["total_findings"] == 0

    # Verify the HTML report is also generated and contains key sections
    html_path = p.with_suffix('.html')
    assert html_path.exists(), f"Expected HTML report at {html_path}"
    html_text = html_path.read_text(encoding="utf-8")
    assert "IAM Audit Report" in html_text
    assert "Total Findings" in html_text
