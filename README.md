# Naru

Work on your [Naru](https://naru.pub) website from a conversation with Claude.
Naru hosts personal websites at `<name>.naru.pub` or your own domain. With this
plugin, Claude can look through your site's files, edit and add pages, upload
images, and add things visitors can use, such as a guestbook or comments,
saved with the Naru Data SDK.

## What's inside

- **Naru connector** (`https://naru.pub/mcp`): six tools that reach the site of
  the account you connect: `get_site`, `list_files` and `read_file` to read, and
  `write_file`, `move_file` and `delete_file` to change files. Changes are
  published as soon as they are made.
- **`naru-site` skill**: how Naru sites work, how to change files without losing
  what's already there, and how to store data with the Naru Data SDK and
  `_naru/collections.json`.

## Use it

1. Add the plugin, then connect Naru from the plugin's **Connectors** tab and
   sign in with your Naru account.
2. Choose what Claude may do: read only, or read and change files.
3. Ask, for example: "Add a guestbook to my Naru homepage" or "Make my about
   page match the style of the home page".

The connector needs the Naru supporter plan. You can see and disconnect
connected apps at any time on https://naru.pub/account. More:
https://naru.pub/docs/mcp.

## Data

The plugin itself stores nothing and runs no code on your computer. Through the
connector, Claude sends naru.pub the file paths and file contents it reads and
writes on your site, and nothing else. Naru keeps your site's files, a record
of each connection (the app's name, when it was connected and last used), and
hashes of its tokens until you disconnect. Naru doesn't receive your
conversations with Claude. See Naru's privacy policy at
https://naru.pub/privacy.

## License

MIT. See [LICENSE](LICENSE).
