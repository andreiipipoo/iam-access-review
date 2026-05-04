from src.checks.inactive_users import check_inactive_users

USERS = [
    {
        "id": "usr_005", "name": "Eve Inactive", "email": "eveinactive@piposhop.com",
        "role": "employee", "account_status": "inactive",
        "last_login": "2026-01-15", "mfa_enabled": False, "mfa_required": False
    },
    {
        "id": "usr_001", "name": "Alice Johnson", "email": "alicejohnson@piposhop.com",
        "role": "employee", "account_status": "active",
        "last_login": "2026-04-28", "mfa_enabled": False, "mfa_required": False
    }
]

def test_eve_flagged_as_inactive():
    findings = check_inactive_users(USERS)
    ids = [f["user_id"] for f in findings]
    assert "usr_005" in ids

def test_alice_not_flagged():
    findings = check_inactive_users(USERS)
    ids = [f["user_id"] for f in findings]
    assert "usr_001" not in ids

def test_severity_is_high_for_inactive_status():
    findings = check_inactive_users(USERS)
    eve = next(f for f in findings if f["user_id"] == "usr_005")
    assert eve["severity"] == "HIGH"