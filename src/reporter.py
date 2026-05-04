import json
from datetime import datetime
from pathlib import Path

SEVERITY_COLORS = {
    "CRITICAL": "#ef4444",
    "HIGH":     "#f97316",
    "MEDIUM":   "#eab308",
    "LOW":      "#22c55e",
}

def _build_html(report: dict) -> str:
    rows = ""
    for check, findings in report["findings"].items():
        for f in findings:
            severity = f.get("severity", "LOW")
            color = SEVERITY_COLORS.get(severity, "#a0a0a0")
            issue = f.get("reason") or f.get("issue", "—")
            rows += f"""
            <tr>
                <td>{f.get('name', '—')}</td>
                <td>{f.get('email', '—')}</td>
                <td>{check.replace('_', ' ').title()}</td>
                <td><span class="badge" style="color:{color};border-color:{color}40;background:{color}12">{severity}</span></td>
                <td>{issue}</td>
                <td>{f.get('recommendation', '—')}</td>
            </tr>"""

    s = report["summary"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>IAM Audit Report — piposhop.com</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    html,body{{min-height:100%;font-family:"Inter",sans-serif;background:#0f0f0f;color:#e0e0e0;line-height:1.5}}

    body::before{{content:'';position:fixed;inset:-10% -10% -10% -10%;z-index:0;
      background:
        radial-gradient(circle at 20% 20%, rgba(4,183,249,0.14) 0%, rgba(3,106,166,0.04) 30%, transparent 60%),
        radial-gradient(circle at 80% 80%, rgba(4,183,249,0.08) 0%, transparent 40%);
      filter:blur(60px);pointer-events:none;animation:floatBubbles 28s ease-in-out infinite}}

    #bigGradient{{position:fixed;inset:0;z-index:0;pointer-events:none;
      background:linear-gradient(120deg,rgba(4,183,249,0.36) 0%,rgba(3,106,166,0.28) 35%,rgba(4,183,249,0.22) 65%,rgba(2,10,20,0) 100%);
      opacity:0.95;background-size:300% 300%;animation:gradientShift 12s ease-in-out infinite;
      mix-blend-mode:screen;filter:blur(18px)}}

    .wrapper{{position:relative;z-index:1;max-width:1100px;margin:0 auto;padding:48px 32px}}

    h1{{font-size:42px;font-weight:700;margin-bottom:8px;
      background:linear-gradient(90deg,#04b7f9,#036aa6,#023e6f);
      background-size:200% 200%;-webkit-background-clip:text;background-clip:text;
      color:transparent;animation:gradientText 6s ease infinite}}

    .meta{{font-size:13px;color:#a0a0a0;margin-bottom:36px}}

    .cards{{display:flex;gap:16px;margin-bottom:40px;flex-wrap:wrap}}
    .card{{background:#181818;border:1px solid rgba(255,255,255,.08);border-radius:12px;
           padding:20px 28px;min-width:160px;box-shadow:0 4px 12px rgba(0,0,0,.2),inset 0 0 8px rgba(0,0,0,0.3)}}
    .card:hover{{box-shadow:0 6px 18px rgba(0,0,0,.4),inset 0 0 8px rgba(0,0,0,0.5)}}
    .card h3{{font-size:12px;color:#a0a0a0;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}}
    .card p{{font-size:2em;font-weight:700;color:#04b7f9}}

    table{{width:100%;border-collapse:collapse;background:#181818;
           border:1px solid rgba(255,255,255,.08);border-radius:12px;overflow:hidden;
           box-shadow:0 4px 12px rgba(0,0,0,.2)}}
    thead th{{background:rgba(4,183,249,0.08);color:#a0a0a0;padding:12px 16px;
              text-align:left;font-size:12px;text-transform:uppercase;letter-spacing:.05em;
              border-bottom:1px solid rgba(255,255,255,.08)}}
    td{{padding:13px 16px;border-bottom:1px solid rgba(255,255,255,.04);font-size:13px}}
    tr:last-child td{{border-bottom:none}}
    tr:hover td{{background:rgba(4,183,249,0.04)}}

    .badge{{padding:3px 10px;border-radius:999px;font-size:12px;font-weight:600;border:1px solid}}

    .footer{{margin-top:32px;font-size:12px;color:#555;text-align:center}}

    @keyframes floatBubbles{{0%{{transform:translateY(0) translateX(0)}}50%{{transform:translateY(12px) translateX(6px)}}100%{{transform:translateY(0) translateX(0)}}}}
    @keyframes gradientShift{{0%{{background-position:0% 50%}}50%{{background-position:100% 50%}}100%{{background-position:0% 50%}}}}
    @keyframes gradientText{{0%{{background-position:0% 50%}}50%{{background-position:100% 50%}}100%{{background-position:0% 50%}}}}
  </style>
</head>
<body>
  <div id="bigGradient"></div>
  <div class="wrapper">
    <h1>IAM Audit Report</h1>
    <p class="meta">Generated: {report['generated_at']} &nbsp;·&nbsp; Tenant: piposhop.com</p>

    <div class="cards">
      <div class="card"><h3>Total Findings</h3><p>{s['total_findings']}</p></div>
      <div class="card"><h3>Inactive Users</h3><p>{s['by_check'].get('inactive_users', 0)}</p></div>
      <div class="card"><h3>Priv. Escalation</h3><p>{s['by_check'].get('privilege_escalation', 0)}</p></div>
      <div class="card"><h3>MFA Issues</h3><p>{s['by_check'].get('mfa_enforcement', 0)}</p></div>
    </div>

    <table>
      <thead>
        <tr>
          <th>Name</th><th>Email</th><th>Check</th>
          <th>Severity</th><th>Issue</th><th>Recommendation</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>

    <p class="footer">Protected by Auth0 · OIDC · SAML 2.0 · iam-access-review</p>
  </div>
</body>
</html>"""


def generate_report(all_findings: dict, output_dir: str = "reports") -> str:
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{output_dir}/audit_report_{timestamp}"

    total = sum(len(v) for v in all_findings.values())
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_findings": total,
            "by_check": {k: len(v) for k, v in all_findings.items()}
        },
        "findings": all_findings
    }

    with open(f"{base}.json", "w") as f:
        json.dump(report, f, indent=2)

    with open(f"{base}.html", "w", encoding="utf-8") as f:
        f.write(_build_html(report))

    print(f"\n✅ JSON report: {base}.json")
    print(f"✅ HTML report: {base}.html")
    print(f"   Total findings: {total}")
    for check, items in all_findings.items():
        print(f"   {check}: {len(items)} finding(s)")

    return f"{base}.json"