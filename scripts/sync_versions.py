#!/usr/bin/env python3
"""Sync each plugin's "version" in marketplace.json with its published plugin.json.

Claude Code only offers a plugin update when the marketplace entry's version
changes, so every plugin release has to touch this repo. For every entry with
a GitHub "url" source, this reads .claude-plugin/plugin.json from the plugin
repo's default branch and writes its version into the entry. A plugin added
later is picked up with no extra setup.

Run by .github/workflows/sync-versions.yml, which opens and merges the PR.
Run by hand (repo root) to preview:  python scripts/sync_versions.py

Exit codes: 0 = nothing to change, 10 = marketplace.json was updated,
1 = error (nothing written).
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

MARKETPLACE_FILE = Path(".claude-plugin/marketplace.json")
PLUGIN_MANIFEST = ".claude-plugin/plugin.json"
GITHUB_URL_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$")
RAW_URL = "https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"
TIMEOUT_SECONDS = 30
EXIT_CHANGED = 10


def published_version(source_url: str) -> str:
    """The version in a plugin repo's plugin.json on its default branch.

    Input:
        source_url (str): the entry's https://github.com/<owner>/<repo>.git url.
    Output:
        str: the plugin's version.
    Raises:
        ValueError: the url isn't a GitHub repo, or plugin.json has no version.
    """
    match = GITHUB_URL_RE.match(source_url)
    if match is None:
        raise ValueError(f"not a GitHub repo url: {source_url}")
    url = RAW_URL.format(owner=match.group(1), repo=match.group(2), path=PLUGIN_MANIFEST)
    with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
        manifest = json.load(response)
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"{url} has no \"version\"")
    return version


def with_version(entry: dict, version: str) -> dict:
    """The entry with "version" set, placed right after "name".

    Input:
        entry (dict): a plugins[] entry.
        version (str): the version to record.
    Output:
        dict: a new entry; key order is otherwise kept.
    """
    updated = {}
    for key, value in entry.items():
        if key == "version":
            continue
        updated[key] = value
        if key == "name":
            updated["version"] = version
    updated.setdefault("version", version)
    return updated


def main() -> int:
    marketplace = json.loads(MARKETPLACE_FILE.read_text(encoding="utf-8"))
    changes = []
    plugins = []
    for entry in marketplace["plugins"]:
        source = entry.get("source")
        if not (isinstance(source, dict) and source.get("source") == "url"):
            print(f"skip {entry['name']}: not a url source")
            plugins.append(entry)
            continue
        try:
            version = published_version(source["url"])
        except Exception as error:  # one broken plugin must not block the others
            print(f"skip {entry['name']}: {error}", file=sys.stderr)
            plugins.append(entry)
            continue
        if entry.get("version") != version:
            changes.append(f"{entry['name']} {entry.get('version', '(none)')} -> {version}")
        plugins.append(with_version(entry, version))

    if not changes:
        print("all plugin versions are current")
        return 0
    marketplace["plugins"] = plugins
    with MARKETPLACE_FILE.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n")
    print("\n".join(changes))
    return EXIT_CHANGED


if __name__ == "__main__":
    raise SystemExit(main())
