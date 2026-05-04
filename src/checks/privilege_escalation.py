PRIVILEGED_ROLES = {"it-admin", "superadmin", "admin"}

def check_privilege_escalation(users: list[dict]) -> list[dict]:
    findings = []

    for user in users:
        is_privileged = user["role"] in PRIVILEGED_ROLES
        is_inactive = user["account_status"] == "inactive"
        mfa_missing = user.get("mfa_required") and not user.get("mfa_enabled")

        if is_privileged and is_inactive:
            findings.append({
                "user_id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "issue": "Privileged account is inactive — access not revoked",
                "severity": "CRITICAL",
                "recommendation": "Revoke privileged access immediately"
            })

        if is_privileged and mfa_missing:
            findings.append({
                "user_id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "issue": "Privileged account has MFA required but MFA not enabled",
                "severity": "CRITICAL",
                "recommendation": "Enforce MFA enrollment before next login"
            })

    return findings