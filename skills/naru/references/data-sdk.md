# Naru Data SDK 1.0.0

Each Naru site has one database. Pages reach it from the browser with
`naru.js`; there is no server code to write. The full guide is at
https://naru.pub/docs/1.0.0/database and the types at
https://sdk.naru.pub/sdk/1.0.0/naru.d.ts.

## Load it

```html
<script type="module">
  import { createNaru } from "https://sdk.naru.pub/sdk/1.0.0/naru.js";
  const naru = createNaru(); // this site's database
</script>
```

## Declare collections in `_naru/collections.json`

A collection holds documents; a document is an id and one JSON value.
Collection names and document ids are 1–64 letters, digits, `_` or `-`.
Write every collection the pages use into `_naru/collections.json` with
`write_file`. Naru creates the missing ones as soon as the file is saved. A
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
approve the page and its collections. Visitors have no accounts in SDK 1.0.0.
For a guestbook or comments, ask for a name in the form.

## Errors

Calls throw a `NaruError`; show a message based on `error.code`:

| code              | meaning                                                  |
| ----------------- | -------------------------------------------------------- |
| `NOT_FOUND`       | no such document, collection or site                     |
| `ACCESS_DENIED`   | the collection's access doesn't allow it                 |
| `AUTH_REQUIRED`   | the owner's sign-in expired; sign in again               |
| `CONFLICT`        | a condition or unique field didn't hold                  |
| `QUOTA_EXCEEDED`  | the site's data or media storage is full                 |
| `RATE_LIMITED`    | too many requests; visitors' `add` is limited per minute |
| `INVALID_REQUEST` | a name, filter or size is malformed                      |
| `UNAVAILABLE`     | a temporary failure; try again shortly                   |

Limits: 100 collections, 100,000 documents and 100 MiB of data per site, and
64 KiB per request.
