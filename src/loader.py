import json
from pathlib import Path
from typing import List, Dict


def load_users(path: str = "data/users.json") -> List[Dict]:
    """
    Load users from a JSON file and perform basic validation.

    Raises:
      FileNotFoundError: if the file does not exist
      ValueError: if the JSON is invalid or the structure is unexpected
      IOError: if the file cannot be read
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {p}")

    try:
        text = p.read_text(encoding="utf-8")
    except Exception as e:
        raise IOError(f"Could not read file {p}: {e}") from e

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {p}: {e}") from e

    if not isinstance(data, list):
        raise ValueError(f"Expected top-level JSON array of users, got {type(data).__name__}")

    users: List[Dict] = []
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"User at index {idx} is not an object (got {type(item).__name__})")
        users.append(item)

    return users