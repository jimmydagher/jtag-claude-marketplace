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
