from src.checks.mfa_enforcement import check_mfa_enforcement

USERS = [
    {
        "id": "usr_003", "name": "Carol Admin", "email": "caroladmin@piposhop.com",
        "role": "it-admin", "account_status": "active",
        "mfa_enabled": True, "mfa_required": True
    },
    {
        "id": "usr_004", "name": "Dave IT", "email": "daveit@piposhop.com",
        "role": "it-admin", "account_status": "active",
        "mfa_enabled": True, "mfa_required": True
    },
    {
        "id": "usr_001", "name": "Alice Johnson", "email": "alicejohnson@piposhop.com",
        "role": "employee", "account_status": "active",
        "mfa_enabled": False, "mfa_required": False
    }
]

def test_carol_passes_mfa_check():
    findings = check_mfa_enforcement(USERS)
    high = [f["user_id"] for f in findings if f["severity"] == "HIGH"]
    assert "usr_003" not in high

def test_dave_passes_mfa_check():
    findings = check_mfa_enforcement(USERS)
    high = [f["user_id"] for f in findings if f["severity"] == "HIGH"]
    assert "usr_004" not in high

def test_alice_flagged_as_low():
    findings = check_mfa_enforcement(USERS)
    low = [f["user_id"] for f in findings if f["severity"] == "LOW"]
    assert "usr_001" in low