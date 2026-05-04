from src.checks.privilege_escalation import check_privilege_escalation

USERS = [
    {
        "id": "usr_003", "name": "Carol Admin", "email": "caroladmin@piposhop.com",
        "role": "it-admin", "account_status": "active",
        "mfa_enabled": True, "mfa_required": True
    },
    {
        "id": "usr_099", "name": "Ghost Admin", "email": "ghost@piposhop.com",
        "role": "it-admin", "account_status": "inactive",
        "mfa_enabled": False, "mfa_required": True
    }
]

def test_inactive_admin_flagged_as_critical():
    findings = check_privilege_escalation(USERS)
    critical = [f["user_id"] for f in findings if f["severity"] == "CRITICAL"]
    assert "usr_099" in critical

def test_active_admin_not_flagged_for_inactive():
    findings = check_privilege_escalation(USERS)
    inactive_issues = [f for f in findings if "inactive" in f["issue"]]
    ids = [f["user_id"] for f in inactive_issues]
    assert "usr_003" not in ids

def test_admin_missing_mfa_flagged_as_critical():
    findings = check_privilege_escalation(USERS)
    critical = [f["user_id"] for f in findings if f["severity"] == "CRITICAL"]
    assert "usr_099" in critical