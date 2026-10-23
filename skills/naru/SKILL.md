---
name: naru
description: Work on a website hosted on Naru (a site at <name>.naru.pub or the owner's custom domain) through the Naru connector. Use when the user wants to see, create, edit, restyle, reorganize or add pages to their Naru site, or add a guestbook, comments, polls, sign-up forms, a blog or other saved data to it.
---

# Working on a Naru site

Naru hosts personal websites. The Naru connector reaches one site: the one
owned by the account the user connected. Every file is published as it is at
`<site address>/<path>` the moment it is written. There is no build step or draft/staging copy for ordinary static files.

## Before changing anything

1. Call `get_site` for the site's address, its plan and its file limits.
2. Call `list_files` to see what is there. Sites are often hand-made over
   years; follow the structure and style the owner already uses.
3. Call `read_file` on every file you will change. `write_file` replaces the
   whole file, so start from its current content and keep what the user didn't
   ask to change.

If only `get_site`, `list_files` and `read_file` are available, the connection
was approved for reading only. Explain that changing files needs the user to
reconnect Naru and allow editing.

## Making changes

- Write complete files with `write_file`. Text goes as UTF-8; images, fonts and
  audio go base64 with `encoding: "base64"`.
- Link files to each other with relative paths (`./style.css`,
  `../images/cat.png`), since a site can live in a folder and on a custom domain.
- `index.html` at the root is the home page, and a folder's `index.html` is
  that folder's page. The home page can't be deleted or moved.
- Only the file types `get_site` lists can be written, each up to 10 MB.
- Everything except `_naru/` is public. Never put passwords, API keys or private
  notes in site files.
- Before deleting a file or replacing one with different content, tell the user
  what will change. A deleted file can't be recovered, and moving a file breaks
  links to its old address.
- After writing, give the user the page's address so they can look at it.

## Saving data

For anything visitors or the owner save (a guestbook, comments, likes, a
sign-up list, blog posts written from the page), use the Naru Data SDK from
the page itself. Read `references/data-sdk.md` before writing that code: it
covers the SDK, `_naru/collections.json`, which declares the collections and
who may read and write them, and the owner's sign-in.

## What Naru can't do

This plugin manages site files and uses the browser Data SDK described in its
reference. It does not provide tools for scheduled jobs, email or SMS sending,
payment processing, or third-party secret storage. When the user
asks for one of these, say so before building, and suggest what a static page
with the Data SDK can do instead.
