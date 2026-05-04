# iam-access-review

> A Python-based IAM audit tool that automatically detects inactive accounts, privilege escalation risks, and missing MFA enforcement across an identity tenant.
> Built as a companion project to [iam-sso-lab](https://github.com/andreiipipoo/iam-sso-lab).

[![CI](https://github.com/andreiipipoo/iam-access-review/actions/workflows/ci.yml/badge.svg)](https://github.com/andreiipipoo/iam-access-review/actions/workflows/ci.yml)
![Language](https://img.shields.io/badge/Language-Python%203.12-blue)
![Tests](https://img.shields.io/badge/Tests-13%20passed-brightgreen)
![Dependencies](https://img.shields.io/badge/Dependencies-zero-brightgreen)
![Cost](https://img.shields.io/badge/Cost-%240-brightgreen)
![IdP](https://img.shields.io/badge/IdP-Auth0-orange)

---

## What This Project Demonstrates

This tool simulates the kind of access review process run by an IAM or security team in an enterprise environment: loading an identity snapshot, running automated checks against it, and producing a structured audit report.

**Key IAM skills demonstrated:**

- Parsing and normalising real identity data exported from Auth0
- Detecting inactive accounts that retain access (account lifecycle risk)
- Identifying privileged accounts missing MFA (privilege escalation risk)
- Flagging standard accounts without MFA enrolled
- Producing structured JSON audit reports with severity levels and recommendations
- Writing unit tests that validate each security check independently

---

## Companion Project

This repo audits the same user population defined in [iam-sso-lab](https://github.com/andreiipipoo/iam-sso-lab), which implements OIDC and SAML 2.0 authentication for the same `piposhop.com` tenant.

Together they simulate a real enterprise where **authentication infrastructure** and **access governance** are separate, complementary concerns.

---

## Architecture

The tool follows a simple pipeline:

```text
Auth0 Tenant (live)
      │
      │  Export Jobs → JSON (with app_metadata fields)
      ▼
data/users.json          ← identity snapshot
      │
      ├── checks/inactive_users.py
      ├── checks/privilege_escalation.py
      └── checks/mfa_enforcement.py
                │
                ▼
      reports/audit_report_YYYYMMDD_HHMMSS.json
      reports/audit_report_YYYYMMDD_HHMMSS.html
```

---

## Identity Snapshot — How It Was Obtained

`data/users.json` is a snapshot exported directly from the Auth0 tenant via **User Management → Export** in the Auth0 Dashboard, using the **Export Jobs** feature with JSON format.

Because Auth0's default export does not include `app_metadata` fields, the following custom fields were added manually in the **Export Fields** section:

| User Attribute | Field Name |
|---|---|
| `app_metadata.role` | `Role` |
| `app_metadata.department` | `Department` |
| `app_metadata.account_status` | `Account Status` |
| `app_metadata.mfa_required` | `MFA Required` |

The raw export (`piposhop.json`) was then transformed into the normalised `users.json` format used by the audit tool via `scripts/transform_users.py`. The raw export is not committed to the repository.

> In a production setup, `loader.py` could be extended to fetch users directly from the Auth0 Management API (`GET /api/v2/users`) instead of reading a static file.

---

## Users & Roles

| User | Email | Role | Department | MFA | Account Status |
|---|---|---|---|---|---|
| Alice Johnson | alicejohnson@piposhop.com | employee | Operations | — | ✅ active |
| Bob Smith | bobsmith@piposhop.com | employee | Sales | — | ✅ active |
| Carol Admin | caroladmin@piposhop.com | **it-admin** | IT | ✅ enforced | ✅ active |
| Dave IT | daveit@piposhop.com | **it-admin** | IT | ✅ enforced | ✅ active |
| Eve Inactive | eveinactive@piposhop.com | employee | Marketing | — | 🔴 inactive |

> **Eve** is intentionally inactive to demonstrate account lifecycle risk detection.

---

## Audit Checks

### 1. Inactive Users — `checks/inactive_users.py`

Flags accounts where `account_status == "inactive"` or where `last_login` is older than 90 days.

| Condition | Severity |
|---|---|
| `account_status: inactive` | HIGH |
| No login in 90+ days | MEDIUM |

### 2. Privilege Escalation — `checks/privilege_escalation.py`

Flags privileged accounts (`it-admin`, `admin`, `superadmin`) that are either inactive or have MFA required but not enabled.

| Condition | Severity |
|---|---|
| Privileged account inactive | CRITICAL |
| Privileged account — MFA required but not enabled | CRITICAL |

### 3. MFA Enforcement — `checks/mfa_enforcement.py`

Flags any account missing MFA where it is required, and surfaces standard accounts without MFA as a low-severity advisory.

| Condition | Severity |
|---|---|
| MFA required but not enabled | HIGH |
| Active standard account without MFA | LOW |

---

## Sample Output

```text
🔍 IAM Access Review — starting audit...

✅ JSON report: reports/audit_report_20260504_155546.json
✅ HTML report: reports/audit_report_20260504_155546.html
   Total findings: 3
   inactive_users:        1 finding(s)
   privilege_escalation:  0 finding(s)
   mfa_enforcement:       2 finding(s)
```

Generated report structure:

```json
{
  "generated_at": "2026-05-04T15:55:46",
  "summary": {
    "total_findings": 3,
    "by_check": {
      "inactive_users": 1,
      "privilege_escalation": 0,
      "mfa_enforcement": 2
    }
  },
  "findings": { "..." }
}
```

---

## Project Structure

```text
iam-access-review/
├── .github/
│   └── workflows/
│       └── ci.yml                    ← GitHub Actions CI
├── data/
│   ├── users.example.json            ← sanitized example snapshot
│   └── users.json                    ← normalised identity snapshot
├── docs/
│   ├── threat-model.md               ← STRIDE threat analysis
│   └── security-controls.md          ← controls documentation
├── reports/                          ← generated audit reports (git-ignored)
├── scripts/
│   └── transform_users.py            ← transforms Auth0 export → users.json
├── src/
│   ├── loader.py                     ← loads users from JSON
│   ├── reporter.py                   ← generates structured JSON report
│   └── checks/
│       ├── inactive_users.py
│       ├── privilege_escalation.py
│       └── mfa_enforcement.py
├── tests/
│   ├── test_inactive_users.py
│   ├── test_mfa_enforcement.py
│   ├── test_privilege_escalation.py
│   ├── test_loader.py
│   └── test_reporter.py
├── main.py                           ← entry point
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Run in 3 Steps

```bash
git clone https://github.com/andreiipipoo/iam-access-review.git
cd iam-access-review
pip install -r requirements.txt
python main.py
```

The audit writes both a machine-readable JSON file and a styled HTML report into the `reports/` directory. Open the generated `.html` file in a browser to view a human-friendly dashboard of findings.


---

## Tests

```bash
python -m pytest -q
```

```text
tests/test_inactive_users.py::test_eve_flagged_as_inactive         PASSED
tests/test_inactive_users.py::test_alice_not_flagged               PASSED
tests/test_inactive_users.py::test_severity_is_high_for_inactive   PASSED
tests/test_mfa_enforcement.py::test_carol_passes_mfa_check         PASSED
tests/test_mfa_enforcement.py::test_dave_passes_mfa_check          PASSED
tests/test_mfa_enforcement.py::test_alice_flagged_as_low           PASSED
tests/test_privilege_escalation.py::test_inactive_admin_flagged    PASSED
tests/test_privilege_escalation.py::test_active_admin_not_flagged  PASSED
tests/test_privilege_escalation.py::test_admin_missing_mfa         PASSED
tests/test_loader.py::test_load_users_success                      PASSED
tests/test_loader.py::test_load_users_missing_file                 PASSED
tests/test_loader.py::test_load_users_invalid_json                 PASSED
tests/test_reporter.py::test_generate_report_creates_file          PASSED

13 passed in 0.42s
```

---

## Tech Stack

| Technology | Role |
|---|---|
| **Python 3.12** | Core language — zero external runtime dependencies |
| **pytest** | Unit testing framework |
| **Auth0 Export Jobs** | Source of identity snapshot |
| **GitHub Actions** | CI — runs tests on every push |
| **JSON** | Data format for both input and audit reports |

---

## Lessons Learned

1. **Auth0 does not export `app_metadata` by default.** Custom fields must be explicitly declared in the Export Fields configuration — a non-obvious step that reflects real-world IAM complexity.
2. **Account lifecycle state must be explicit.** Inactive accounts are a common residual risk in enterprise environments. Surfacing them automatically is more reliable than manual reviews.
3. **Privileged accounts need stricter controls.** Separating the privilege escalation check from the general MFA check reflects real security policy: the risk profile of an admin account is fundamentally different from a standard user.
4. **Zero dependencies is a feature.** Using only Python stdlib for the audit logic reduces supply chain risk and makes the tool easier to run in restricted environments.

---

## License

MIT