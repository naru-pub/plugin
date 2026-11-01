# Naru

Work on your [Naru](https://naru.pub) website from a conversation with ChatGPT, Codex, or Claude.
Naru hosts personal websites at `<name>.naru.pub` or your own domain. With this
plugin, your assistant can look through your site's files, edit and add pages, upload
images, and add things visitors can use, such as a guestbook, a blog or comments,
saved with the Naru Data SDK.

## What's inside

- **Naru connector** (`https://naru.pub/mcp`): fourteen tools that reach the site
  of the account you connect. Changes are published as soon as they are made.

  | Permission                  | Tools                                                                                     |
  | --------------------------- | ----------------------------------------------------------------------------------------- |
  | Anyone connected            | `get_sdk_reference`                                                                       |
  | Read                        | `get_site`, `list_files`, `read_file`, `list_collections`                                 |
  | Change                      | `write_file`, `move_file`, `delete_file`, `delete_folder`, `configure_collections`        |
  | Database documents          | `list_documents`, `get_document`                                                          |
  | Database documents + change | `set_document`, `delete_document`                                                         |

- **`naru` skill**: how Naru sites work, how to change files without losing
  what's already there, and how to store data with the Naru Data SDK 1.1.0.

## Use it

For Claude, install this repository as a plugin, then connect Naru from the
Connectors tab. For local development, use `claude --plugin-dir /path/to/plugin`.

For ChatGPT and Codex, install the existing private or published Naru plugin
and complete its OAuth connection. The public directory submission is still in
preparation; this repository does not itself publish or authenticate the plugin.
For directory submission, use the ChatGPT ZIP built below.

Choose read-only or editing access, then ask, for example, “Add a guestbook to
my Naru homepage” or “Make my about page match the style of the home page.”
Database documents, which can hold what your visitors wrote, are a separate
permission that stays off unless you turn it on.

The connector needs the Naru supporter plan. You can disconnect apps on your
[Naru account page](https://naru.pub/account). See [Naru's MCP guide](https://naru.pub/docs/mcp).

## Repository and packages

- `skills/naru/`: the shared workflow and pinned Data SDK 1.1.0 reference.
- `assets/icon.png`: shared branding. The identical `.claude-plugin/icon.png`
  is retained for Claude's icon discovery; the packager checks they match.
- `plugin.json` and `mcp.json`: ChatGPT/Codex portable metadata, OAuth, and
  public review cases. The root manifest is the authoritative ChatGPT source.
- `.claude-plugin/plugin.json` and `.mcp.json`: Claude configuration.
- `docs/chatgpt-submission.md`: review status and remaining submission steps.

Build both self-contained packages with Python 3 (no extra dependencies):

```sh
python3 scripts/package.py
```

Outputs are `dist/naru-chatgpt-<version>.zip` and
`dist/naru-claude-<version>.zip`. Generated ZIPs and recordings are not committed.
Both manifests must use the same version. Version 1.1.0 unifies the platform
sources and renames Claude's `edit-site` skill to `naru`. Version 1.2.0 covers
the connector's fourteen tools and Data SDK 1.1.0.

## Data

The plugin itself stores nothing and runs no code on your computer. Through the
connector, the assistant sends naru.pub the file paths and file contents it reads and
writes on your site, the collections it declares and, if you allow database
documents, the documents it reads and writes, and nothing else. Documents can
hold what your site's visitors wrote, and those go to your assistant when it
reads them. Naru keeps your site's files and database, a record
of each connection (the app's name, when it was connected and last used), and
hashes of its tokens until you disconnect. Naru doesn't receive your
conversations with your assistant. See [Naru's privacy policy](https://naru.pub/privacy).

## License

MIT. See [LICENSE](LICENSE).
