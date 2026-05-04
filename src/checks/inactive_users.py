from datetime import date, timedelta

INACTIVE_THRESHOLD_DAYS = 90

def check_inactive_users(users: list[dict]) -> list[dict]:
    findings = []
    cutoff = date.today() - timedelta(days=INACTIVE_THRESHOLD_DAYS)

    for user in users:
        last_login = date.fromisoformat(user["last_login"])
        is_status_inactive = user["account_status"] == "inactive"
        is_stale = last_login < cutoff

        if is_status_inactive or is_stale:
            findings.append({
                "user_id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "last_login": user["last_login"],
                "account_status": user["account_status"],
                "reason": "account marked inactive" if is_status_inactive else f"no login in {INACTIVE_THRESHOLD_DAYS}+ days",
                "severity": "HIGH" if is_status_inactive else "MEDIUM",
                "recommendation": "Disable or delete account immediately"
            })
    return findings