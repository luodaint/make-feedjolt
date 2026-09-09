# Feedjolt

Connect [Feedjolt](https://www.feedjolt.com) to Make. Create, update, search, and watch feedback posts; manage boards and workspaces.

## Connection

Create a **Feedjolt API Key** connection using a workspace API key (`fjk_…`) from the Feedjolt dashboard. The key is sent as `Authorization: Bearer`.

Validation request: `GET https://api.feedjolt.com/api/v1/workspaces`.

## Modules

- **Watch Posts** — polling trigger on `GET /workspaces/{workspace_slug}/posts?sort_by=newest`
- **Watch Posts (Instant)** — attached webhook for `post.created`
- **Create / Get / Update / Delete a Post**
- **Update a Post Status**
- **Search Posts**
- **List / Get / Create a Board**
- **List / Get a Workspace**
- **Make an API Call** — arbitrary authorized request (path relative to `https://api.feedjolt.com`)

## API

Base URL used by modules and RPCs: `https://api.feedjolt.com/api/v1`

OpenAPI: https://api.feedjolt.com/openapi.json

This file is the Make app README (deployed with the app). Developer sync steps live in the repository root `README.md`.
