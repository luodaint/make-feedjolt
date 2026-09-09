# make-feedjolt

Make.com Custom App (Apps SDK / Apps Editor) for [Feedjolt](https://www.feedjolt.com).

Make remains the source of truth once Marc creates app id `feedjolt` in the portal. This repo is the Git mirror under `src/feedjolt/` so the app can be cloned, edited offline, and deployed back.

## Status

Local scaffold is ready to sync. It has not been deployed to Make (no Make API key in this environment). After Marc creates the app and adds a zone API token, use **Deploy to Make** from the Apps SDK.

## Auth and API

| | |
| --- | --- |
| Base URL (modules / RPCs / webhook attach) | `https://api.feedjolt.com/api/v1` |
| Auth | Workspace API key `fjk_…` → `Authorization: Bearer` |
| Connection check | `GET /workspaces` |
| OpenAPI | https://api.feedjolt.com/openapi.json |
| Make docs | https://developers.make.com/custom-apps-documentation |

Do **not** commit Make API tokens, Feedjolt keys, or webhook signing secrets. The Apps SDK writes tokens to `.secrets/` (gitignored).

## Layout

```
src/feedjolt/
  makecomapp.json          # Apps SDK project manifest
  README.md                # In-app README (deployed to Make)
  base/base.iml.json       # baseUrl, Bearer auth, 401/403/404/429/5xx, sanitize
  groups/groups.json       # Posts / Boards / Workspaces / Other
  connections/api-key/     # Basic API-key connection
  rpcs/                    # listWorkspaces, listBoards, listStatuses
  webhooks/watch-posts-created/   # Dedicated attached webhook (post.created)
  modules/                 # Triggers, actions, search, universal
```

File names follow the 2026 Make Apps SDK Clone-to-Local convention: `{kebab-id}.{code-type}.iml.json` inside `{componentType}s/{kebab-id}/`. `makecomapp.json` is the schema used by [vscode-apps-sdk](https://github.com/integromat/vscode-apps-sdk) (`fileVersion`, `generalCodeFiles`, `components`, `origins`).

Official clone defaults are `general/base.iml.json` and `modules/groups.json`. This repo uses `base/` and `groups/` as requested; paths are declared in `makecomapp.json`, so Deploy/Pull still work. If you **Clone to Local Folder** into an empty tree, the SDK may recreate `general/` — keep this repo’s `makecomapp.json` paths or re-point them.

`common` is omitted (`null`) so no app secrets live in Git.

## Marc: create the app and sync this folder

### 1. Make account and zone API token

1. Sign in to your Make zone (`eu1`, `us1`, `eu2`, `us2`, …).
2. Create a Make **API token** with Custom Apps / SDK scopes  
   ([Generate your API key](https://developers.make.com/custom-apps-documentation/get-started/make-apps-editor/apps-sdk/generate-your-api-key)).
3. In this repo (never commit it):

   ```bash
   mkdir -p .secrets
   printf '%s' 'YOUR_MAKE_API_TOKEN' > .secrets/apikey
   ```

4. In `src/feedjolt/makecomapp.json` → `origins[0]`:
   - `appId` is already `feedjolt`
   - Set `baseUrl` to `https://<zone>.make.com/api` (must end with `/api`)
   - `apikeyFile` is `../../.secrets/apikey`

### 2. Create app `feedjolt` in Make

**Web UI**

1. Make → **Custom Apps** (or Apps Editor).
2. Create an app with public id **`feedjolt`** (lowercase; this must match `origins[].appId`).
3. Leave it empty. Do not invent modules in the UI if you plan to deploy this folder.

**VS Code (optional)**

1. Install [Make Apps SDK](https://marketplace.visualstudio.com/items?itemName=integromat.apps-sdk).
2. Configure the same zone + API token.
3. You can create the app from the extension instead of the web UI.

### 3. Install Apps Editor / open this repo

1. `git clone` this repository and open the **repo root** in VS Code / Cursor.
2. Install the **Make Apps SDK** extension.
3. Trust the workspace. The extension reads `src/feedjolt/makecomapp.json`.

**Do not** run Clone to Local Folder *over* this tree if it would replace `src/feedjolt`. Preferred flow: create empty `feedjolt` in Make → open this repo → **Deploy to Make**.

If you already cloned an empty app into `src/feedjolt`, merge carefully: keep this scaffold’s components and `makecomapp.json`, then use the pairing dialog so local ids map to new remote ids.

### 4. Deploy / pull

From the Apps SDK (right-click `src/feedjolt/makecomapp.json`):

| Action | When |
| --- | --- |
| **Deploy to Make** | Push this scaffold into the empty `feedjolt` app. Pair each local component to **create on remote**. |
| **Pull from Make** | After someone edits in the Make UI. |
| **Compare with Make** | Diff one file or the whole app. |

`idMapping` starts empty. The first deploy asks you to create remote counterparts. After that, the SDK writes local↔remote ids into `origins[].idMapping` — commit that mapping so the team stays aligned.

Partial deploy: right-click a component folder or a single `.iml.json`.

### 5. Test scenarios

Use a real Feedjolt workspace API key (`fjk_…`) only in Make connections, never in Git.

1. **Connection** — Create “Feedjolt API Key”. Validation must succeed (`GET /workspaces`).
2. **List Workspaces** / **Get a Workspace** — slug select from RPC.
3. **List Boards** / **Get a Board** / **Create a Board**.
4. **Create a Post** → **Get a Post** → **Update a Post** → **Update a Post Status**.
5. **Search Posts** — query ≥ 2 characters.
6. **Watch Posts** (polling) — set epoch, create a post in Feedjolt, run once; only new items.
7. **Watch Posts (Instant)** — creating the webhook should `POST /workspaces/{slug}/webhooks` with `events: ["post.created"]`. Create a post; the scenario should run. Disable/delete the webhook to confirm detach `DELETE /webhooks/{id}`.
8. **Make an API Call** — URL `/api/v1/workspaces`, method `GET` (required for public review).
9. **Delete a Post** — expect HTTP 204; module outputs `{ id }`.
10. Force 401 (bad key) and 404 (bad id) and confirm Base error messages.

### 6. Publish / review checklist

Before **Publish (invite)** or **Request app review**:

- [ ] App id is `feedjolt`; icon and public name set in Make
- [ ] Connection validates; API key is `password` + sanitized in logs
- [ ] Base maps 401 / 403 / 404 / 429 / 5xx
- [ ] **Make an API Call** uses a host-relative path (`https://api.feedjolt.com/{{parameters.url}}`) so tokens cannot be sent to a third-party host
- [ ] Groups cover every module (save fails if one is missing)
- [ ] Module labels follow Make naming (*Watch Posts*, *Create a Post*, *Make an API Call*)
- [ ] Samples filled on triggers / search / actions
- [ ] Instant trigger is linked to the attached webhook; attach/detach tested
- [ ] In-app `src/feedjolt/README.md` is accurate
- [ ] Common data has no secrets
- [ ] Reviewer test account + Feedjolt API key (share out of band)
- [ ] Privacy / terms links if going public
- [ ] No Make or Feedjolt secrets in this Git repo

Review process: [Request app review](https://developers.make.com/custom-apps-documentation/app-review).

## MVP modules

| Kind | Local id | Feedjolt API |
| --- | --- | --- |
| Connection | `apiKey` | `GET /workspaces` |
| RPCs | `listWorkspaces`, `listBoards`, `listStatuses` | `GET /workspaces`, `/boards`, `/statuses` |
| Trigger | `watchPosts` | `GET /workspaces/{slug}/posts?sort_by=newest` |
| Instant trigger | `watchPostsInstant` → webhook `watchPostsCreated` | attach `POST .../webhooks` `{events:["post.created"]}` |
| Actions | `createPost` `getPost` `updatePost` `deletePost` `updatePostStatus` | OpenAPI post routes |
| Search | `searchPosts` `listBoards` `listWorkspaces` | `/posts/search`, `/boards`, `/workspaces` |
| Actions | `getBoard` `createBoard` `getWorkspace` | board + workspace routes |
| Universal | `makeApiCall` | arbitrary path on `api.feedjolt.com` |

List/search modules use Make `moduleType: search` even though the product brief listed them under actions.

## TODOs after first sync

These are marked in IML with `TODO(make-iml)` where the schema is documented but not fully proven in Scenario Builder:

- Confirm `response.error.type` names (`InvalidAccessTokenError`, `RateLimitError`, …) if review complains.
- Confirm IML array index for connection metadata (`body.1.name` is 1-based).
- Confirm `post.created` webhook envelope (`body.post` vs raw post). Docs: [Webhook payloads](https://www.feedjolt.com/en/docs/developers/webhooks/payloads), [Signing](https://www.feedjolt.com/en/docs/developers/webhooks/signing).
- Optional: page through `PostListResponse` when Watch Posts exceeds one page.
- `listBoards` RPC returns **slug** (path params). Watch Posts filters use **board_id** as optional text.
- HMAC verification of `X-Feedjolt-Signature` is not implemented in webhook communication (Make may not expose the attach secret for IML verify). Treat as follow-up.

Regenerate IML from OpenAPI (optional): `python3 scripts/generate_make_scaffold.py`.

## References

- [Clone Make app to local workspace](https://developers.make.com/custom-apps-documentation/get-started/make-apps-editor/apps-sdk/local-development-for-apps/clone-make-app-to-local-workspace)
- [Local development README (SDK)](https://github.com/integromat/vscode-apps-sdk/blob/master/README-local-development-for-apps.md)
- [Basic connection](https://developers.make.com/custom-apps-documentation/app-components/connections/basic-connection)
- [Attached dedicated webhooks](https://developers.make.com/custom-apps-documentation/app-components/webhooks/dedicated/attached)
- [Universal REST module](https://developers.make.com/custom-apps-documentation/app-components/modules/universal-module/rest)
- [Groups](https://developers.make.com/custom-apps-documentation/app-components/groups)
