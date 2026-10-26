#!/usr/bin/env python3
"""Check complete skill bundles, source hashes and local Markdown references."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
lock = json.loads((ROOT / "SOURCE.json").read_text())
errors = []
hashes = {entry["path"]: entry["sha256"] for entry in lock["files"]}
for relative, expected in hashes.items():
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"Missing source file: {relative}")
    elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        errors.append(f"Source mismatch: {relative}")
actual = {str(p.relative_to(ROOT)) for p in (ROOT / "skills").rglob("*") if p.is_file()}
expected = {p for p in hashes if p.startswith("skills/")}
if actual != expected:
    errors.append(f"Untracked bundle files: {sorted(actual-expected)}")
names = {s["name"] for s in lock["skills"]}
for skill in lock["skills"]:
    path = ROOT / "skills" / skill["name"]
    text = (path / "SKILL.md").read_text()
    front = text.split("---", 2)[1]
    if not re.search(r"^name:\s*" + re.escape(skill["name"]) + r"\s*$", front, re.M):
        errors.append(f"Frontmatter name mismatch: {skill['name']}")
    metadata = json.loads((path / "skill-metadata.json").read_text())
    for dependency in metadata.get("dependencies", []):
        if dependency not in names:
            errors.append(f"Missing dependency: {skill['name']} -> {dependency}")
for path in list((ROOT / "skills").rglob("*.md")) + [ROOT / "README.md"] + list((ROOT / "docs").glob("*.md")):
    text = path.read_text()
    # Ignore examples fenced as code; check actual authored navigation links.
    text = re.sub(r"(?ms)^```.*?^```\s*$", "", text)
    for raw in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
        url = raw.split("#", 1)[0].strip("<>")
        if not url or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url):
            continue
        if not (path.parent / unquote(url)).is_file():
            errors.append(f"Broken local link in {path.relative_to(ROOT)}: {url}")
if errors:
    raise SystemExit("\n".join(errors))
print(f"PASS: {len(names)} complete skills, {len(expected)} source files, dependencies, hashes and Markdown links.")
