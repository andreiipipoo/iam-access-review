import argparse
import sys
from pathlib import Path

from src.loader import load_users
from src.checks.inactive_users import check_inactive_users
from src.checks.privilege_escalation import check_privilege_escalation
from src.checks.mfa_enforcement import check_mfa_enforcement
from src.reporter import generate_report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="IAM Access Review — run checks against a users JSON file"
    )
    parser.add_argument(
        "-i", "--input", default="data/users.json", help="Path to users JSON file"
    )
    parser.add_argument(
        "-o", "--output-dir", default="reports", help="Directory to write the report"
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    print("🔍 IAM Access Review — starting audit...\n")
    try:
        print(f"Loading users from: {args.input}")
        users = load_users(args.input)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Unexpected error loading users: {e}", file=sys.stderr)
        sys.exit(4)

    findings = {
        "inactive_users": check_inactive_users(users),
        "privilege_escalation": check_privilege_escalation(users),
        "mfa_enforcement": check_mfa_enforcement(users),
    }

    try:
        out_file = generate_report(findings, output_dir=args.output_dir)
        print(f"Report written to: {out_file}")
    except Exception as e:
        print(f"Failed to write report: {e}", file=sys.stderr)
        sys.exit(5)


if __name__ == "__main__":
    main()