# make-feedjolt

Make.com (Apps SDK / Custom Apps Editor) integration for [Feedjolt](https://www.feedjolt.com).

## Status
Plan only until Zapier ships. App config will live primarily in Make; this repo is the optional local Git mirror (`src/feedjolt`).

## Auth
Workspace API key `fjk_…` → `Authorization: Bearer` against `https://api.feedjolt.com/api/v1`.

## MVP modules
- Connection + base (validate `GET /workspaces`)
- RPCs: workspaces, boards, statuses
- Triggers: Watch posts (polling) + instant via attached webhook `post.created`
- Actions: create/get/update/delete post, update status, search posts, boards/workspaces
- Universal: Make an API call (required for public review)

## Marc / portal
1. Make account + API key for zone (eu1/us1)
2. Make Apps Editor → create app id `feedjolt`
3. Clone to local folder → develop here
4. Test scenarios → Publish (invite) → App review

OpenAPI: https://api.feedjolt.com/openapi.json  
Docs: https://developers.make.com/custom-apps-documentation

Do not commit Make API keys or Feedjolt secrets.
