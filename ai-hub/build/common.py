"""Shared helpers. Standard library only."""
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
SKILLS = ROOT / "skills"


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def today():
    return datetime.now().strftime("%Y-%m-%d")


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def append(path, text):
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)


def get_field(text, key):
    m = re.search(rf"^{re.escape(key)}:[ \t]*(.*)$", text, re.M)
    if not m:
        return None
    val = m.group(1).split("#")[0].strip()
    return None if val in ("", "null") else val


def set_field(text, key, value):
    """Set a top-level `key: value` line, keeping any trailing comment."""
    pattern = re.compile(rf"^({re.escape(key)}:[ \t]*)([^#\n]*)(.*)$", re.M)
    if not pattern.search(text):
        return text.rstrip("\n") + f"\n{key}: {value}\n"
    return pattern.sub(lambda m: f"{m.group(1)}{value}{'  ' if m.group(3) else ''}{m.group(3)}", text, count=1)


def add_history(text, date, tool, action):
    """`history:` must be the last key in project.yaml."""
    entry = f"  - {{date: {date}, tool: {tool}, action: {action}}}"
    empty = r"^history:[ \t]*\[\][ \t]*(#.*)?$"
    if re.search(empty, text, re.M):
        return re.sub(empty, "history:\n" + entry, text, count=1, flags=re.M)
    return text.rstrip("\n") + "\n" + entry + "\n"


def parse_list(value):
    return [v.strip() for v in value.split(",") if v.strip()] if value else []


def fmt_list(items):
    return "[" + ", ".join(items) + "]"


def project_dir(name):
    d = PROJECTS / name
    if not d.is_dir() or name.startswith("_"):
        die(f"project '{name}' not found in projects/")
    return d
