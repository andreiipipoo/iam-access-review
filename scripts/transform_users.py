import json

users = []
with open("data/piposhop.json", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        u = json.loads(line)
        users.append({
            "id":             u["Id"],
            "name":           u["Name"],
            "email":          u["Email"],
            "role":           u["Role"],
            "department":     u["Department"],
            "account_status": u["Account Status"],
            "last_login":     u["Last Login"][:10],
            "mfa_enabled":    u["MFA Required"],
            "mfa_required":   u["MFA Required"],
            "logins_count":   u["Logins Count"],
            "groups":         []
        })

with open("data/users.json", "w") as f:
    json.dump(users, f, indent=2)

print(f"✅ Transformados {len(users)} usuarios → data/users.json")