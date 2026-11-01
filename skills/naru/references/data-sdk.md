# Naru Data SDK 1.1.0

Each Naru site has one database. Pages reach it from the browser with
`naru.js`; there is nothing to install or build. This is a summary:
`get_sdk_reference` has the full guides and API reference, also at
https://naru.pub/docs/1.1.0/database and
https://sdk.naru.pub/sdk/1.1.0/naru.d.ts.

## Load it

```html
<script type="module">
  import { createNaru } from "https://sdk.naru.pub/sdk/1.1.0/naru.js";
  const naru = createNaru({ site: "<name>" }); // <name>.naru.pub's database
</script>
```

Always pass `site`: without it, a page fails on a custom domain or opened from
the owner's computer.

## Where data goes

Collections hold JSON documents that pages read and write directly, under one
access rule per collection: blog posts, guestbooks, inquiries, anonymous
comments. The site's own SQLite tables are reached only through the site's code,
which decides per caller: members' posts and comments, points, a shop. Neither
can read the other, and a site can use both.

## Declare collections in `_naru/collections.json`

A collection holds documents; a document is an id and one JSON value.
Collection names and document ids are 1–64 letters, digits, `_` or `-`.
Declare every collection the pages use with `configure_collections`, which
writes `_naru/collections.json`. Naru creates the missing ones at once. A
change to an existing collection's access waits until the owner approves it on
https://naru.pub/database, so tell the user when you change one.

```json
{
  "collections": {
    "guestbook": { "read": "world", "write": "create" },
    "posts": { "read": "world", "write": "admin", "indexes": ["category"] },
    "inquiries": { "read": "admin", "write": "create", "unique": ["email"] }
  }
}
```

- `read` (required): `"world"`, anyone, or `"admin"`, the owner only.
- `write` (required): `"admin"`, the owner only; `"create"`, anyone may add new
  documents but not change or delete them; or `"world"`, anyone may change or
  delete anything.
- Take visitors' input with `"create"`. Use `"world"` writing almost never.
- Keep email addresses and other personal details in a collection with
  `"read": "admin"`. Anyone can read a `"world"` collection.
- `unique`: up to 3 fields no two documents may share; a clash fails with
  `CONFLICT`.
- `indexes`: up to 5 fields that lists often filter on.

## Read and add

```js
const guestbook = naru.collection("guestbook");

const { documents, nextCursor } = await guestbook.list({
  filter: { approved: true },
  sort: [[{ metadata: "createdAt" }, "desc"]],
  size: 20,
});
// each document: { id, data, revision, createdAt, updatedAt }

const saved = await guestbook.add({ name, message });
```

- `get(id)`, `list(options)`, `count({ filter })`, `pages(options)` (an async
  iterable of pages) and `add(data)`.
- `filter` compares top-level fields to a value, or with `{ gt, gte, lt, lte }`;
  up to 5 conditions, all of which must hold. Store dates as padded strings
  such as `"2026-09-01"` to compare them.
- `sort` takes one or two `[field, "asc" | "desc"]` pairs; `{ metadata:
"createdAt" }` or `"updatedAt"` sorts by the document's own times.
- `size` is 50 by default and at most 100. For the next page, pass the same
  filter and sort with `after: nextCursor`; `nextCursor` is `null` at the end.
- Store only JSON values: ISO strings, not `Date` objects.
- Build the page with `textContent`, not `innerHTML`, for anything visitors
  wrote.

## The owner's sign-in

Changing or deleting documents, and reading `"admin"` collections, needs the
site's owner to sign in from the page:

```js
const admin = await naru.auth.session(); // null until the owner signs in
if (!admin)
  loginButton.onclick = () =>
    naru.auth.signIn({ collections: ["posts", "inquiries"] });
```

- `admin.collection(name)` adds `set(id, data, { condition })`, which creates
  or replaces a whole document, and `delete(id, { condition })`.
- `condition: { revision: doc.revision }` saves only if nobody changed the
  document since it was read; `{ absent: true }` only if it doesn't exist yet.
  Otherwise the call fails with `CONFLICT`.
- `set` doesn't merge fields. Pass `{ ...doc.data, title }` to change one.
- `admin.batch([...])` applies up to 100 `set` and `delete` changes at once.
- `admin.media.upload(file)` returns `{ url, name, contentType, size }`; save the
  `url` in a document.
- `admin.signOut()` signs out.

Nothing needs setting up beforehand: the first sign-in asks the owner to
approve the page and its collections.

## Members

A member is a visitor signed in to this site with their own Naru account. Nothing
needs registering beforehand. Members have no access of their own to collections;
what they may do is decided by site code.

```js
const member = await naru.members.session(); // null until they sign in
if (!member) joinButton.onclick = () => naru.members.signIn();
else await member.mutate("board:write", { title, body });
```

- `member.id` is a number used only on this site, and stays the same. The site
  never gets the member's Naru login or email.
- `member.query()`, `member.mutate()`, `member.subscribe()`,
  `member.media.upload(file)` and `member.signOut()`.
- A member waiting for approval or banned gets `ACCESS_DENIED`, with
  `error.details.membership` set to `"pending"` or `"banned"`.
- Roles such as staff aren't stored by Naru. Keep them in a table, keyed by
  `ctx.member.id`.

## Site code

| File                      | Does                                                 | Called with                     |
| ------------------------- | ---------------------------------------------------- | ------------------------------- |
| `_naru/migrations/*.sql`  | creates and changes tables, each applied once        | applied on saving               |
| `_naru/queries/path.js`   | reads tables and returns a value; can't write        | `naru.query("path:name", args)` |
| `_naru/mutations/path.js` | checks, writes and returns; one call, one transaction | `member.mutate("path:name", args)` |

```sql
-- _naru/migrations/0001_posts.sql
CREATE TABLE posts (
  id INTEGER PRIMARY KEY,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
```

```js
// _naru/mutations/board.js
export async function write(ctx, { title }) {
  if (!ctx.member) ctx.fail("AUTH_REQUIRED", "로그인해 주세요.");
  await ctx.sql`INSERT INTO posts (author, title, created_at)
    VALUES (${ctx.member.id}, ${title}, ${ctx.now})`;
}
```

- Save these files with `write_file`. A failed migration rejects the whole release
  and changes nothing, and `write_file` says so.
- An applied migration can't be edited or deleted. Add a new file named after it,
  numbered like `0002_body_format.sql`.
- Who is calling: `ctx.member` is `{ id }` for `member.query()` and
  `member.mutate()`, `ctx.owner` is true for `admin.query()` and `admin.mutate()`,
  and both are empty for `naru.query()` and `naru.mutate()`, which call as a visitor
  even when a member is signed in.
- Only site code can be trusted with prices, balances and permissions: a visitor
  can change anything a page's script does.
- `naru.subscribe("path:name", args, onAnswer, { onError })` listens to a query and
  answers again when a mutation changes the tables it read. Call `.close()` on the
  result to stop. Collections can't be listened to.
- `_naru/routes.json` and `_naru/routes.js` let site code answer addresses itself,
  for link previews, search engines and RSS. Most pages don't need them.
- Site code has no network access or timers. Never put secrets in files under
  `_naru/`.

## Errors

Calls throw a `NaruError`. Show visitors `error.message`, which is in Korean, or
for site code's `ctx.fail`, as the site wrote it. Branch on `error.code`:

| code              | meaning                                                    |
| ----------------- | ---------------------------------------------------------- |
| `NOT_FOUND`       | no such document, collection, query, mutation or site      |
| `ACCESS_DENIED`   | access doesn't allow it, or a member is pending or banned  |
| `AUTH_REQUIRED`   | the owner's or member's sign-in expired; sign in again     |
| `CONFLICT`        | a condition, unique field or UNIQUE column didn't hold     |
| `QUOTA_EXCEEDED`  | the site's data or media storage is full                   |
| `RATE_LIMITED`    | too many requests; try again shortly                       |
| `INVALID_REQUEST` | a malformed request, or site code went over a limit        |
| `UNAVAILABLE`     | a temporary failure; try again shortly                     |

Limits: 100 collections, 100,000 documents and 100 MiB of data (collections and
tables together) per site, and 64 KiB per collection request. Site code gets 100
database operations per call and tens of milliseconds, and returns at most 1 MiB
of JSON.
