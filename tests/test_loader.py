import json
from pathlib import Path

from src.loader import load_users


def test_load_users_success(tmp_path):
    data = [{"id": "u1", "name": "A"}]
    p = tmp_path / "users.json"
    p.write_text(json.dumps(data), encoding="utf-8")

    users = load_users(str(p))
    assert isinstance(users, list)
    assert users[0]["id"] == "u1"


def test_load_users_missing_file():
    try:
        load_users("nonexistent.json")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True


def test_load_users_invalid_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{ not: valid }", encoding="utf-8")
    try:
        load_users(str(p))
        assert False, "Expected ValueError"
    except ValueError:
        assert True
