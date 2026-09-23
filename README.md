# jtag-claude-marketplace

Jimmy Dagher's Claude Code plugin marketplace. It holds only the registry —
every plugin lives in its own repository.

## Install

```
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
     "source": { "source": "github", "repo": "jimmydagher/<name>-plugin" },
     "description": "<one line>"
   }
   ```

3. Add a row to the table above.
