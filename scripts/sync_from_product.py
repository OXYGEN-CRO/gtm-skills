#!/usr/bin/env python3
"""Export the customer skill allowlist from a pinned OXYGEN release checkout."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

NAMES = """oxygen-onboarding oxygen-gtm-consultant oxygen-gtm oxygen-tables
oxygen-enrichment oxygen-sourcing oxygen-crm oxygen-recipes oxygen-collaboration
oxygen-quickstart oxygen-workflow-authoring oxygen-knowledge oxygen-unibox
oxygen-email-infra oxygen-deliverability oxygen-sequencer oxygen-publishing
oxygen-linkedin-content oxygen-signals oxygen-table-tidy oxygen-diagnostics
oxygen-feedback oxygen-clay-migration oxygen-ugc oxygen-custom-http""".split()
BASE = "apps/web/src/agent-skills"
ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--ref", required=True, help="Full released product commit SHA")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-f0-9]{40}", args.ref):
        parser.error("--ref must be a full 40-character commit SHA")

    def read(path):
        return subprocess.check_output(
            ["git", "-C", str(args.source), "show", f"{args.ref}:{path}"]
        )

    # Assemble in memory before writing. Never export the whole product tree.
    files, skills = {}, []
    for name in NAMES:
        manifest = read(f"{BASE}/{name}.manifest.ts").decode()
        block = manifest.split("files: [", 1)[1].split("],", 1)[0]
        paths = re.findall(r'"([^"\n]+)"', block)
        dependencies_match = re.search(r"dependencies:\s*\[([^\]]*)\]", manifest)
        dependencies = re.findall(r'"([^"\n]+)"', dependencies_match[1]) if dependencies_match else []
        if "SKILL.md" not in paths or "skill-metadata.json" not in paths:
            raise ValueError(f"Incomplete manifest: {name}")
        for relative in paths:
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"Unsafe manifest path: {relative}")
            files[f"skills/{name}/{relative}"] = read(f"{BASE}/{name}/{relative}")
        metadata = json.loads(files[f"skills/{name}/skill-metadata.json"])
        skills.append({"name": name, "title": metadata["title"],
                       "description": metadata["description"],
                       "dependencies": dependencies, "files": paths})

    files["LICENSE"] = read("agent-plugin/LICENSE")
    lock = {"source_repository": "OXYGEN-CRO/oxygen", "source_ref": args.ref,
            "source_path": BASE, "license": "LicenseRef-OXYGEN-Proprietary",
            "skills": skills,
            "files": [{"path": path, "sha256": hashlib.sha256(data).hexdigest()}
                      for path, data in sorted(files.items())]}
    # Do not silently leave obsolete files in a later release.
    old = ROOT / "SOURCE.json"
    if old.exists():
        previous = json.loads(old.read_text())["files"]
        previous_paths = set(previous) if isinstance(previous, dict) else {f["path"] for f in previous}
        removed = previous_paths - files.keys()
        if removed:
            raise ValueError("Review obsolete files before syncing: " + ", ".join(sorted(removed)))
    for path, data in files.items():
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    old.write_text(json.dumps(lock, indent=2) + "\n")
    print(f"Exported {len(skills)} skills and {len(files)-1} skill files from {args.ref}.")


if __name__ == "__main__":
    main()
