ROLES_REQUIRING_MFA = {"it-admin", "superadmin", "admin"}

def check_mfa_enforcement(users: list[dict]) -> list[dict]:
    findings = []

    for user in users:
        needs_mfa = user["role"] in ROLES_REQUIRING_MFA or user.get("mfa_required")
        has_mfa = user.get("mfa_enabled", False)

        if needs_mfa and not has_mfa:
            findings.append({
                "user_id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "issue": "MFA required but not enabled",
                "severity": "HIGH",
                "recommendation": "Block login until MFA is enrolled"
            })

        if not needs_mfa and not has_mfa and user["account_status"] == "active":
            findings.append({
                "user_id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "issue": "MFA not enabled on active standard account",
                "severity": "LOW",
                "recommendation": "Encourage MFA enrollment"
            })

    return findings