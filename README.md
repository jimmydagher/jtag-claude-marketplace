# jtag-claude-marketplace

Jimmy Dagher's Claude Code plugin marketplace. It holds only the registry — every plugin lives in its own repository.

## Install

```text
/plugin marketplace add jimmydagher/jtag-claude-marketplace
/plugin install <plugin>@jtag-claude-marketplace
```

## Plugins

| Plugin | Repository | What it is |
|---|---|---|
| `sdsi` | [jimmydagher/sdsi-plugin](https://github.com/jimmydagher/sdsi-plugin) | Software Development Standard Instructions — language-neutral topic skills, project types, and a scripted release chain |
| `council` | [jimmydagher/council-plugin](https://github.com/jimmydagher/council-plugin) | Contractor-style reviewer lenses (IT and BU) for documentation, designs, plans, and business proposals |

## Adding a plugin

1. Create the plugin in its own repository (`jimmydagher/<name>-plugin`).
2. Add an entry to `.claude-plugin/marketplace.json`:

   ```json
   {
     "name": "<name>",
     "source": { "source": "url", "url": "https://github.com/jimmydagher/<name>-plugin.git" },
     "description": "<one line>"
   }
   ```

Use an HTTPS `url` source, not `"source": "github"`: the `github` form clones over SSH, which fails on machines without a GitHub SSH key.

3. Add a row to the table above.

Leave out `"version"` — the sync workflow below adds it on its next run.

## Plugin versions and updates

Claude Code only offers a plugin update when the plugin's `"version"` in `marketplace.json` changes, so every plugin release has to touch this repo. That's automated: `.github/workflows/sync-versions.yml` runs every 30 minutes, reads each plugin's `.claude-plugin/plugin.json` from its repo's default branch (`scripts/sync_versions.py`), and when any version differs commits the change straight to `main` — no PR, nothing to approve. This covers every plugin registered here, including new ones, with no setup in the plugin repos.

- **Run it right after a release** (local shell, any directory): `gh workflow run sync-versions.yml -R jimmydagher/jtag-claude-marketplace`
- **Preview locally** (repo root): `python scripts/sync_versions.py`, which rewrites `marketplace.json` and exits 10 when something changed, 0 when everything is current.
- **Never edit `"version"` by hand.** Release the plugin (bump its `plugin.json`) and let the sync follow.

One-time settings this depends on:

- This repo: Settings → Actions → General → Workflow permissions → "Read and write permissions" (the workflow also requests `contents: write`).
- `main` must accept pushes from GitHub Actions: if a branch protection rule or ruleset is ever added, let `github-actions[bot]` bypass it.
- Organization settings → Plugins → this marketplace's menu → **Sync automatically** on, so the org picks up the version change.
