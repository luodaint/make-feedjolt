#!/usr/bin/env python3
"""Generate the Feedjolt Make custom-app local mirror.

File names and makecomapp.json keys follow the 2026 Make Apps SDK
(vscode-apps-sdk) Clone-to-Local conventions. Folder layout follows
src/feedjolt/{base,connections,modules,webhooks,rpcs,groups}.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "src" / "feedjolt"

# Shared IML snippets -------------------------------------------------------

WORKSPACE_SELECT = {
    "name": "workspaceSlug",
    "type": "select",
    "label": "Workspace",
    "help": "Workspace slug. Loaded from `GET /workspaces`.",
    "required": True,
    "options": "rpc://listWorkspaces",
}

BOARD_SELECT = {
    "name": "boardSlug",
    "type": "select",
    "label": "Board",
    "help": "Board slug. Nested under workspace; loaded from `GET /workspaces/{workspace_slug}/boards`.",
    "required": True,
    "options": "rpc://listBoards",
}

STATUS_SELECT = {
    "name": "statusId",
    "type": "select",
    "label": "Status",
    "help": "Status ID. Loaded from `GET /workspaces/{workspace_slug}/statuses`.",
    "required": True,
    "options": "rpc://listStatuses",
}

LIMIT_PARAM = {
    "name": "limit",
    "type": "uinteger",
    "label": "Limit",
    "help": "Maximum number of results Make will work with during one execution cycle.",
    "required": True,
    "default": 10,
}

POST_ID = {
    "name": "postId",
    "type": "text",
    "label": "Post ID",
    "help": "Feedjolt post ID.",
    "required": True,
}

# Interface derived from OpenAPI PostResponse
POST_INTERFACE = [
    {"name": "id", "type": "text", "label": "Post ID"},
    {"name": "workspace_id", "type": "text", "label": "Workspace ID"},
    {"name": "board_id", "type": "text", "label": "Board ID"},
    {"name": "author_type", "type": "text", "label": "Author Type"},
    {"name": "author_id", "type": "text", "label": "Author ID"},
    {"name": "title", "type": "text", "label": "Title"},
    {"name": "body", "type": "text", "label": "Body"},
    {"name": "status_id", "type": "text", "label": "Status ID"},
    {"name": "owner_admin_id", "type": "text", "label": "Owner Admin ID"},
    {"name": "is_draft", "type": "boolean", "label": "Is Draft"},
    {"name": "is_internal", "type": "boolean", "label": "Is Internal"},
    {"name": "eta", "type": "text", "label": "ETA"},
    {"name": "vote_count", "type": "integer", "label": "Vote Count"},
    {"name": "weighted_score", "type": "number", "label": "Weighted Score"},
    {"name": "comment_count", "type": "integer", "label": "Comment Count"},
    {"name": "is_spam", "type": "boolean", "label": "Is Spam"},
    {"name": "is_incognito", "type": "boolean", "label": "Is Incognito"},
    {"name": "merged_into_id", "type": "text", "label": "Merged Into ID"},
    {"name": "created_at", "type": "date", "label": "Created At"},
    {"name": "updated_at", "type": "date", "label": "Updated At"},
    {
        "name": "tags",
        "type": "array",
        "label": "Tags",
        "spec": {
            "type": "collection",
            "spec": [
                {"name": "id", "type": "text", "label": "Tag ID"},
                {"name": "name", "type": "text", "label": "Name"},
            ],
        },
    },
    {"name": "author_name", "type": "text", "label": "Author Name"},
    {"name": "author_email", "type": "email", "label": "Author Email"},
    {"name": "author_avatar_url", "type": "url", "label": "Author Avatar URL"},
    {"name": "owner_name", "type": "text", "label": "Owner Name"},
    {"name": "owner_email", "type": "email", "label": "Owner Email"},
    {"name": "owner_avatar_url", "type": "url", "label": "Owner Avatar URL"},
    {"name": "version_id", "type": "text", "label": "Version ID"},
    {
        "name": "version",
        "type": "collection",
        "label": "Version",
        "spec": [
            {"name": "id", "type": "text", "label": "ID"},
            {"name": "name", "type": "text", "label": "Name"},
        ],
    },
    {"name": "sentiment", "type": "text", "label": "Sentiment"},
    {"name": "sentiment_confidence", "type": "number", "label": "Sentiment Confidence"},
    {"name": "has_linear_issue", "type": "boolean", "label": "Has Linear Issue"},
]

POST_SAMPLE = {
    "id": "pst_01EXAMPLE",
    "workspace_id": "wks_01EXAMPLE",
    "board_id": "brd_01EXAMPLE",
    "author_type": "admin",
    "author_id": "usr_01EXAMPLE",
    "title": "Add dark mode",
    "body": "Please add a dark theme to the dashboard.",
    "status_id": "sts_01EXAMPLE",
    "owner_admin_id": None,
    "is_draft": False,
    "is_internal": False,
    "eta": None,
    "vote_count": 3,
    "weighted_score": 3,
    "comment_count": 1,
    "is_spam": False,
    "is_incognito": False,
    "merged_into_id": None,
    "created_at": "2026-09-01T12:00:00.000Z",
    "updated_at": "2026-09-01T12:00:00.000Z",
    "tags": [],
    "author_name": "Alex Rivera",
    "author_email": "alex@example.com",
    "author_avatar_url": None,
    "owner_name": None,
    "owner_email": None,
    "owner_avatar_url": None,
    "version_id": None,
    "version": None,
    "sentiment": None,
    "sentiment_confidence": None,
    "has_linear_issue": False,
}

BOARD_INTERFACE = [
    {"name": "id", "type": "text", "label": "Board ID"},
    {"name": "workspace_id", "type": "text", "label": "Workspace ID"},
    {"name": "title", "type": "text", "label": "Title"},
    {"name": "description", "type": "text", "label": "Description"},
    {"name": "slug", "type": "text", "label": "Slug"},
    {"name": "icon", "type": "text", "label": "Icon"},
    {"name": "visibility", "type": "text", "label": "Visibility"},
    {"name": "votes_enabled", "type": "boolean", "label": "Votes Enabled"},
    {"name": "moderation_enabled", "type": "boolean", "label": "Moderation Enabled"},
    {"name": "notify_admins_on_new_post", "type": "boolean", "label": "Notify Admins On New Post"},
    {"name": "pinned_post_id", "type": "text", "label": "Pinned Post ID"},
    {"name": "archived", "type": "boolean", "label": "Archived"},
    {"name": "sort_order", "type": "integer", "label": "Sort Order"},
    {"name": "created_at", "type": "date", "label": "Created At"},
    {"name": "updated_at", "type": "date", "label": "Updated At"},
]

BOARD_SAMPLE = {
    "id": "brd_01EXAMPLE",
    "workspace_id": "wks_01EXAMPLE",
    "title": "Feature requests",
    "description": "Public ideas from customers",
    "slug": "feature-requests",
    "icon": None,
    "visibility": "PUBLIC",
    "votes_enabled": True,
    "moderation_enabled": False,
    "notify_admins_on_new_post": True,
    "pinned_post_id": None,
    "archived": False,
    "sort_order": 0,
    "created_at": "2026-08-01T12:00:00.000Z",
    "updated_at": "2026-08-01T12:00:00.000Z",
}

WORKSPACE_INTERFACE = [
    {"name": "id", "type": "text", "label": "Workspace ID"},
    {"name": "name", "type": "text", "label": "Name"},
    {"name": "slug", "type": "text", "label": "Slug"},
    {"name": "logo_url", "type": "url", "label": "Logo URL"},
    {"name": "favicon_url", "type": "url", "label": "Favicon URL"},
    {"name": "settings", "type": "collection", "label": "Settings"},
    {"name": "data_region", "type": "text", "label": "Data Region"},
    {"name": "is_active", "type": "boolean", "label": "Is Active"},
    {"name": "created_at", "type": "date", "label": "Created At"},
    {"name": "trial_started", "type": "boolean", "label": "Trial Started"},
    {"name": "email_intake_enabled", "type": "boolean", "label": "Email Intake Enabled"},
    {"name": "email_intake_default_board_id", "type": "text", "label": "Email Intake Default Board ID"},
    {
        "name": "email_intake_allowed_domains",
        "type": "array",
        "label": "Email Intake Allowed Domains",
        "spec": {"type": "text"},
    },
    {"name": "email_intake_address", "type": "email", "label": "Email Intake Address"},
]

WORKSPACE_SAMPLE = {
    "id": "wks_01EXAMPLE",
    "name": "Acme",
    "slug": "acme",
    "logo_url": None,
    "favicon_url": None,
    "settings": {},
    "data_region": "US",
    "is_active": True,
    "created_at": "2026-01-15T12:00:00.000Z",
    "trial_started": False,
    "email_intake_enabled": False,
    "email_intake_default_board_id": None,
    "email_intake_allowed_domains": [],
    "email_intake_address": None,
}

EMPTY_SCOPE = []


def dumps(obj) -> str:
    return json.dumps(obj, indent="\t", ensure_ascii=False) + "\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def kebab(local_id: str) -> str:
    out = []
    for i, ch in enumerate(local_id):
        if ch.isupper() and i:
            out.append("-")
        out.append(ch.lower())
    return "".join(out)


def component_path(kind_plural: str, local_id: str, code_filename: str) -> str:
    kid = kebab(local_id)
    return f"{kind_plural}/{kid}/{kid}.{code_filename}.iml.json"


def write_jsonc(rel: str, header: str, obj) -> None:
    body = dumps(obj)
    write(APP / rel, f"{header}\n{body}" if header else body)


# ---------------------------------------------------------------------------
# Base / groups / connection
# ---------------------------------------------------------------------------

BASE = {
    "baseUrl": "https://api.feedjolt.com/api/v1",
    "headers": {
        "authorization": "Bearer {{connection.apiKey}}",
        "accept": "application/json",
    },
    "response": {
        # TODO(make-iml): Confirm error.type enum against the Error types section
        # of https://developers.make.com/custom-apps-documentation if review flags these names.
        "error": {
            "401": {
                "type": "InvalidAccessTokenError",
                "message": "[401] Unauthorized. Check the Feedjolt workspace API key (fjk_…). {{ifempty(body.detail, body.message)}}",
            },
            "403": {
                "type": "RuntimeError",
                "message": "[403] Forbidden. This API key cannot access this workspace. {{ifempty(body.detail, body.message)}}",
            },
            "404": {
                "type": "DataError",
                "message": "[404] Not found. {{ifempty(body.detail, body.message)}}",
            },
            "422": {
                "type": "DataError",
                "message": "[422] Validation error. {{ifempty(body.detail, body.message)}}",
            },
            "429": {
                "type": "RateLimitError",
                "message": "[429] Rate limited by Feedjolt. Retry later. {{ifempty(body.detail, body.message)}}",
            },
            "500": {
                "type": "ConnectionError",
                "message": "[500] Feedjolt server error. {{ifempty(body.detail, body.message)}}",
            },
            "502": {
                "type": "ConnectionError",
                "message": "[502] Feedjolt bad gateway. {{ifempty(body.detail, body.message)}}",
            },
            "503": {
                "type": "ConnectionError",
                "message": "[503] Feedjolt unavailable. {{ifempty(body.detail, body.message)}}",
            },
            "504": {
                "type": "ConnectionError",
                "message": "[504] Feedjolt gateway timeout. {{ifempty(body.detail, body.message)}}",
            },
            "message": "[{{statusCode}}] {{ifempty(ifempty(body.detail, body.message), 'Feedjolt API error')}}",
        }
    },
    "log": {"sanitize": ["request.headers.authorization"]},
}

GROUPS = [
    {
        "label": "Posts",
        "modules": [
            "watchPosts",
            "watchPostsInstant",
            "createPost",
            "getPost",
            "updatePost",
            "updatePostStatus",
            "deletePost",
            "searchPosts",
        ],
    },
    {"label": "Boards", "modules": ["listBoards", "getBoard", "createBoard"]},
    {"label": "Workspaces", "modules": ["listWorkspaces", "getWorkspace"]},
    {"label": "Other", "modules": ["makeApiCall"]},
]

CONNECTION_PARAMS = [
    {
        "name": "apiKey",
        "type": "password",
        "label": "API Key",
        "help": "Workspace API key from Feedjolt (starts with `fjk_`). Sent as `Authorization: Bearer`.",
        "required": True,
        "editable": True,
    }
]

CONNECTION_COMM = {
    "url": "https://api.feedjolt.com/api/v1/workspaces",
    "method": "GET",
    "headers": {"authorization": "Bearer {{parameters.apiKey}}"},
    "response": {
        "valid": "{{statusCode === 200}}",
        # TODO(make-iml): Make IML arrays are typically 1-indexed (`body.1`). Confirm in Scenario Builder.
        "metadata": {"type": "text", "value": "{{ifempty(body.1.name, 'Feedjolt')}}"},
        "error": {
            "message": "[{{statusCode}}] Invalid Feedjolt API key or the key cannot list workspaces. {{ifempty(body.detail, body.message)}}"
        },
    },
    "log": {"sanitize": ["request.headers.authorization"]},
}


# ---------------------------------------------------------------------------
# RPCs
# ---------------------------------------------------------------------------

RPCS = {
    "listWorkspaces": {
        "label": "List workspaces",
        "params": [],
        "communication": {
            "url": "/workspaces",
            "method": "GET",
            "response": {
                "limit": 500,
                "iterate": "{{body}}",
                "output": {"label": "{{item.name}}", "value": "{{item.slug}}"},
            },
        },
    },
    "listBoards": {
        "label": "List boards",
        "params": [
            {
                "name": "workspaceSlug",
                "type": "text",
                "label": "Workspace",
                "required": True,
            }
        ],
        "communication": {
            "url": "/workspaces/{{parameters.workspaceSlug}}/boards",
            "method": "GET",
            "response": {
                "limit": 500,
                "iterate": "{{body}}",
                "output": {
                    "label": "{{item.title}}",
                    "value": "{{item.slug}}",
                },
            },
        },
    },
    "listStatuses": {
        "label": "List statuses",
        "params": [
            {
                "name": "workspaceSlug",
                "type": "text",
                "label": "Workspace",
                "required": True,
            }
        ],
        "communication": {
            "url": "/workspaces/{{parameters.workspaceSlug}}/statuses",
            "method": "GET",
            "response": {
                "limit": 500,
                "iterate": "{{body}}",
                "output": {"label": "{{item.name}}", "value": "{{item.id}}"},
            },
        },
    },
}


# ---------------------------------------------------------------------------
# Webhook
# ---------------------------------------------------------------------------

WEBHOOK_PARAMS = [
    {
        **WORKSPACE_SELECT,
        "help": "Workspace that will register the `post.created` webhook via `POST /workspaces/{workspace_slug}/webhooks`.",
    }
]

WEBHOOK_COMM = {
    # Docs: X-Feedjolt-Event header; payload includes a stable `id` and a `post` object
    # (see status.changed example in Feedjolt webhook retries docs). Confirm exact
    # post.created envelope at https://www.feedjolt.com/en/docs/developers/webhooks/payloads
    "condition": "{{if(headers['x-feedjolt-event'], headers['x-feedjolt-event'] = 'post.created', true)}}",
    "output": "{{if(body.post, body.post, body)}}",
    "respond": {"status": 200, "type": "json", "body": {"ok": True}},
}

WEBHOOK_ATTACH = {
    "url": "/workspaces/{{parameters.workspaceSlug}}/webhooks",
    "method": "POST",
    "body": {"url": "{{webhook.url}}", "events": ["post.created"]},
    "response": {"data": {"id": "{{body.id}}", "secret": "{{body.secret}}"}},
    "log": {"sanitize": ["response.body.secret"]},
}

WEBHOOK_DETACH = {
    "url": "/workspaces/{{parameters.workspaceSlug}}/webhooks/{{webhook.id}}",
    "method": "DELETE",
}

WEBHOOK_UPDATE = {}  # unused; events are fixed to post.created


# ---------------------------------------------------------------------------
# Modules
# ---------------------------------------------------------------------------

NESTED_WORKSPACE_BOARD = {
    **WORKSPACE_SELECT,
    "options": {
        "store": "rpc://listWorkspaces",
        "nested": [{**BOARD_SELECT, "mappable": False}],
    },
}

NESTED_WORKSPACE_STATUS = {
    **WORKSPACE_SELECT,
    "options": {
        "store": "rpc://listWorkspaces",
        "nested": [{**STATUS_SELECT, "required": False, "mappable": False}],
    },
}


def comm_get(url: str, qs: dict | None = None, iterate: str | None = None, extra_response: dict | None = None):
    obj: dict = {"url": url, "method": "GET"}
    if qs:
        obj["qs"] = qs
    response: dict = {"output": "{{item}}" if iterate else "{{body}}"}
    if iterate:
        response["iterate"] = iterate
    if extra_response:
        response.update(extra_response)
    obj["response"] = response
    return obj


def comm_write(url: str, method: str, body: dict | None = None, output: str = "{{body}}"):
    obj: dict = {"url": url, "method": method, "response": {"output": output}}
    if body is not None:
        obj["body"] = body
    return obj


MODULES = {
    "watchPosts": {
        "label": "Watch Posts",
        "description": "Triggers when a new post is created in a Feedjolt workspace (polling).",
        "moduleType": "trigger",
        "staticParams": [
            WORKSPACE_SELECT,
            {
                "name": "boardId",
                "type": "text",
                "label": "Board ID",
                "help": "Optional. `GET /workspaces/{workspace_slug}/posts` filters by `board_id` (ID, not slug).",
            },
            {
                **STATUS_SELECT,
                "required": False,
                "label": "Status",
                "help": "Optional. Filter by `status_id`.",
            },
            LIMIT_PARAM,
        ],
        "mappableParams": [],
        "epoch": {
            # Documented polling-trigger epoch shape from Make trigger docs.
            "response": {
                "limit": 500,
                "output": {"date": "{{item.created_at}}", "label": "{{item.title}}"},
                "iterate": "{{body.posts}}",
            },
            "url": "/workspaces/{{parameters.workspaceSlug}}/posts",
            "method": "GET",
            "qs": {"sort_by": "newest", "page_size": 50},
        },
        "communication": {
            "url": "/workspaces/{{parameters.workspaceSlug}}/posts",
            "method": "GET",
            "qs": {
                "sort_by": "newest",
                "page_size": "{{parameters.limit}}",
                "board_id": "{{parameters.boardId}}",
                "status_id": "{{parameters.statusId}}",
            },
            # TODO(make-iml): Add pagination.qs.page when scenarios exceed one page.
            # API: page, page_size, total on PostListResponse.
            "response": {
                "limit": "{{parameters.limit}}",
                "iterate": "{{body.posts}}",
                "output": "{{item}}",
                "trigger": {
                    "id": "{{item.id}}",
                    "date": "{{item.created_at}}",
                    "type": "date",
                    "order": "desc",
                },
            },
        },
        "interface": POST_INTERFACE,
        "samples": POST_SAMPLE,
    },
    "watchPostsInstant": {
        "label": "Watch Posts (Instant)",
        "description": "Triggers immediately when Feedjolt delivers a `post.created` webhook.",
        "moduleType": "instant_trigger",
        "webhook": "watchPostsCreated",
        "staticParams": [],
        "mappableParams": [],
        "communication": {},
        "interface": POST_INTERFACE,
        "samples": POST_SAMPLE,
    },
    "createPost": {
        "label": "Create a Post",
        "description": "Creates a post on a Feedjolt board.",
        "moduleType": "action",
        "actionCrud": "create",
        "staticParams": [],
        "mappableParams": [
            {
                **WORKSPACE_SELECT,
                "options": {
                    "store": "rpc://listWorkspaces",
                    "nested": [
                        {**BOARD_SELECT, "mappable": False},
                        {**STATUS_SELECT, "required": False, "mappable": False},
                    ],
                },
            },
            {
                "name": "title",
                "type": "text",
                "label": "Title",
                "help": "Required. Max 500 characters (Feedjolt PostCreate.title).",
                "required": True,
            },
            {"name": "body", "type": "text", "label": "Body"},
            {"name": "isDraft", "type": "boolean", "label": "Draft", "default": False},
            {"name": "isInternal", "type": "boolean", "label": "Internal", "default": False},
            {"name": "eta", "type": "text", "label": "ETA"},
            {"name": "versionId", "type": "text", "label": "Version ID"},
        ],
        "communication": comm_write(
            "/workspaces/{{parameters.workspaceSlug}}/boards/{{parameters.boardSlug}}/posts",
            "POST",
            {
                "title": "{{parameters.title}}",
                "body": "{{parameters.body}}",
                "status_id": "{{parameters.statusId}}",
                "is_draft": "{{parameters.isDraft}}",
                "is_internal": "{{parameters.isInternal}}",
                "eta": "{{parameters.eta}}",
                "version_id": "{{parameters.versionId}}",
            },
        ),
        "interface": POST_INTERFACE,
        "samples": POST_SAMPLE,
    },
    "getPost": {
        "label": "Get a Post",
        "description": "Retrieves a single Feedjolt post by ID.",
        "moduleType": "action",
        "actionCrud": "read",
        "staticParams": [],
        "mappableParams": [
            WORKSPACE_SELECT,
            {**POST_ID, "mode": "edit"},
        ],
        "communication": comm_write(
            "/workspaces/{{parameters.workspaceSlug}}/posts/{{parameters.postId}}",
            "GET",
        ),
        "interface": POST_INTERFACE,
        "samples": POST_SAMPLE,
    },
    "updatePost": {
        "label": "Update a Post",
        "description": "Updates title, body, internal flag, ETA, or version on a post (`PATCH`).",
        "moduleType": "action",
        "actionCrud": "update",
        "staticParams": [],
        "mappableParams": [
            WORKSPACE_SELECT,
            {**POST_ID, "mode": "edit"},
            {
                "name": "title",
                "type": "text",
                "label": "Title",
                "help": "Max 500 characters (Feedjolt PostUpdate.title).",
            },
            {"name": "body", "type": "text", "label": "Body"},
            {"name": "isInternal", "type": "boolean", "label": "Internal"},
            {"name": "eta", "type": "text", "label": "ETA"},
            {"name": "versionId", "type": "text", "label": "Version ID"},
        ],
        "communication": comm_write(
            "/workspaces/{{parameters.workspaceSlug}}/posts/{{parameters.postId}}",
            "PATCH",
            {
                "title": "{{parameters.title}}",
                "body": "{{parameters.body}}",
                "is_internal": "{{parameters.isInternal}}",
                "eta": "{{parameters.eta}}",
                "version_id": "{{parameters.versionId}}",
            },
        ),
        "interface": POST_INTERFACE,
        "samples": POST_SAMPLE,
    },
    "updatePostStatus": {
        "label": "Update a Post Status",
        "description": "Changes a post's status (`PUT /posts/{post_id}/status`).",
        "moduleType": "action",
        "actionCrud": "update",
        "staticParams": [],
        "mappableParams": [
            {
                **WORKSPACE_SELECT,
                "options": {
                    "store": "rpc://listWorkspaces",
                    "nested": [{**STATUS_SELECT, "mappable": False}],
                },
            },
            {**POST_ID, "mode": "edit"},
        ],
        "communication": comm_write(
            "/workspaces/{{parameters.workspaceSlug}}/posts/{{parameters.postId}}/status",
            "PUT",
            {"status_id": "{{parameters.statusId}}"},
        ),
        "interface": POST_INTERFACE,
        "samples": POST_SAMPLE,
    },
    "deletePost": {
        "label": "Delete a Post",
        "description": "Deletes a Feedjolt post. API returns HTTP 204.",
        "moduleType": "action",
        "actionCrud": "delete",
        "staticParams": [],
        "mappableParams": [
            WORKSPACE_SELECT,
            {**POST_ID, "mode": "edit"},
        ],
        "communication": {
            "url": "/workspaces/{{parameters.workspaceSlug}}/posts/{{parameters.postId}}",
            "method": "DELETE",
            "response": {"output": {"id": "{{parameters.postId}}"}},
        },
        "interface": [{"name": "id", "type": "text", "label": "Post ID"}],
        "samples": {"id": "pst_01EXAMPLE"},
    },
    "searchPosts": {
        "label": "Search Posts",
        "description": "Searches posts in a workspace (`GET /posts/search?q=`).",
        "moduleType": "search",
        "staticParams": [],
        "mappableParams": [
            WORKSPACE_SELECT,
            {
                "name": "q",
                "type": "text",
                "label": "Query",
                "help": "Search string (2–200 characters).",
                "required": True,
            },
            LIMIT_PARAM,
        ],
        "communication": {
            "url": "/workspaces/{{parameters.workspaceSlug}}/posts/search",
            "method": "GET",
            "qs": {"q": "{{parameters.q}}"},
            "response": {
                "iterate": "{{body}}",
                "output": "{{item}}",
                "limit": "{{parameters.limit}}",
            },
        },
        "interface": POST_INTERFACE,
        "samples": POST_SAMPLE,
    },
    "listBoards": {
        "label": "List Boards",
        "description": "Lists boards in a Feedjolt workspace.",
        "moduleType": "search",
        "staticParams": [],
        "mappableParams": [WORKSPACE_SELECT, LIMIT_PARAM],
        "communication": {
            "url": "/workspaces/{{parameters.workspaceSlug}}/boards",
            "method": "GET",
            "response": {
                "iterate": "{{body}}",
                "output": "{{item}}",
                "limit": "{{parameters.limit}}",
            },
        },
        "interface": BOARD_INTERFACE,
        "samples": BOARD_SAMPLE,
    },
    "getBoard": {
        "label": "Get a Board",
        "description": "Retrieves a board by slug.",
        "moduleType": "action",
        "actionCrud": "read",
        "staticParams": [],
        "mappableParams": [
            {
                **WORKSPACE_SELECT,
                "options": {
                    "store": "rpc://listWorkspaces",
                    "nested": [{**BOARD_SELECT, "mappable": False}],
                },
            }
        ],
        "communication": comm_write(
            "/workspaces/{{parameters.workspaceSlug}}/boards/{{parameters.boardSlug}}",
            "GET",
        ),
        "interface": BOARD_INTERFACE,
        "samples": BOARD_SAMPLE,
    },
    "createBoard": {
        "label": "Create a Board",
        "description": "Creates a board in a Feedjolt workspace.",
        "moduleType": "action",
        "actionCrud": "create",
        "staticParams": [],
        "mappableParams": [
            WORKSPACE_SELECT,
            {
                "name": "title",
                "type": "text",
                "label": "Title",
                "help": "Required. Max 255 characters (Feedjolt BoardCreate.title).",
                "required": True,
            },
            {
                "name": "slug",
                "type": "text",
                "label": "Slug",
                "help": "Lowercase letters, numbers, and hyphens (`^[a-z0-9-]+$`). Max 100 characters.",
                "required": True,
            },
            {"name": "description", "type": "text", "label": "Description"},
            {"name": "icon", "type": "text", "label": "Icon", "help": "Optional. Max 32 characters."},
            {
                "name": "visibility",
                "type": "select",
                "label": "Visibility",
                "default": "PUBLIC",
                "options": [
                    {"label": "Public", "value": "PUBLIC"},
                    {"label": "Authenticated", "value": "AUTHENTICATED"},
                    {"label": "Invite only", "value": "INVITE_ONLY"},
                    {"label": "Internal", "value": "INTERNAL"},
                ],
            },
            {"name": "votesEnabled", "type": "boolean", "label": "Votes Enabled", "default": True},
            {"name": "moderationEnabled", "type": "boolean", "label": "Moderation Enabled", "default": False},
            {
                "name": "notifyAdminsOnNewPost",
                "type": "boolean",
                "label": "Notify Admins On New Post",
                "default": True,
            },
        ],
        "communication": comm_write(
            "/workspaces/{{parameters.workspaceSlug}}/boards",
            "POST",
            {
                "title": "{{parameters.title}}",
                "slug": "{{parameters.slug}}",
                "description": "{{parameters.description}}",
                "icon": "{{parameters.icon}}",
                "visibility": "{{parameters.visibility}}",
                "votes_enabled": "{{parameters.votesEnabled}}",
                "moderation_enabled": "{{parameters.moderationEnabled}}",
                "notify_admins_on_new_post": "{{parameters.notifyAdminsOnNewPost}}",
            },
        ),
        "interface": BOARD_INTERFACE,
        "samples": BOARD_SAMPLE,
    },
    "listWorkspaces": {
        "label": "List Workspaces",
        "description": "Lists workspaces the API key can access (`GET /workspaces`).",
        "moduleType": "search",
        "staticParams": [],
        "mappableParams": [LIMIT_PARAM],
        "communication": {
            "url": "/workspaces",
            "method": "GET",
            "response": {
                "iterate": "{{body}}",
                "output": "{{item}}",
                "limit": "{{parameters.limit}}",
            },
        },
        "interface": WORKSPACE_INTERFACE,
        "samples": WORKSPACE_SAMPLE,
    },
    "getWorkspace": {
        "label": "Get a Workspace",
        "description": "Retrieves a workspace by slug.",
        "moduleType": "action",
        "actionCrud": "read",
        "staticParams": [],
        "mappableParams": [WORKSPACE_SELECT],
        "communication": comm_write("/workspaces/{{parameters.workspaceSlug}}", "GET"),
        "interface": WORKSPACE_INTERFACE,
        "samples": WORKSPACE_SAMPLE,
    },
    "makeApiCall": {
        "label": "Make an API Call",
        "description": "Performs an arbitrary authorized API call.",
        "moduleType": "universal",
        "staticParams": [],
        "mappableParams": [
            {
                "name": "url",
                "type": "text",
                "label": "URL",
                "help": "Enter a path relative to `https://api.feedjolt.com`.\nFor example: `/api/v1/workspaces`",
                "required": True,
            },
            {
                "name": "method",
                "type": "select",
                "label": "Method",
                "default": "GET",
                "required": True,
                "options": [
                    {"label": "GET", "value": "GET"},
                    {"label": "POST", "value": "POST"},
                    {"label": "PUT", "value": "PUT"},
                    {"label": "PATCH", "value": "PATCH"},
                    {"label": "DELETE", "value": "DELETE"},
                ],
            },
            {
                "name": "headers",
                "type": "array",
                "label": "Headers",
                "help": "You don't have to add authorization headers; they are inherited from the connection.",
                "default": [{"key": "Content-Type", "value": "application/json"}],
                "spec": [
                    {"name": "key", "type": "text", "label": "Key"},
                    {"name": "value", "type": "text", "label": "Value"},
                ],
            },
            {
                "name": "qs",
                "type": "array",
                "label": "Query String",
                "spec": [
                    {"name": "key", "type": "text", "label": "Key"},
                    {"name": "value", "type": "text", "label": "Value"},
                ],
            },
            {"name": "body", "type": "any", "label": "Body"},
        ],
        # Host only (no /api/v1) so reviewers can call any documented version.
        # Path must stay on api.feedjolt.com — required for public review.
        "communication": {
            "url": "https://api.feedjolt.com/{{parameters.url}}",
            "method": "{{parameters.method}}",
            "type": "text",
            "qs": {"{{...}}": "{{toCollection(parameters.qs, 'key', 'value')}}"},
            "headers": {"{{...}}": "{{toCollection(parameters.headers, 'key', 'value')}}"},
            "body": "{{parameters.body}}",
            "response": {
                "output": {
                    "body": "{{body}}",
                    "headers": "{{headers}}",
                    "statusCode": "{{statusCode}}",
                }
            },
        },
        "interface": [
            {"name": "body", "type": "any", "label": "Body"},
            {"name": "headers", "type": "collection", "label": "Headers"},
            {"name": "statusCode", "type": "number", "label": "Status code"},
        ],
        "samples": {"body": [], "headers": {}, "statusCode": 200},
    },
}


def module_code_files(local_id: str, module: dict) -> dict:
    files = {
        "communication": component_path("modules", local_id, "communication"),
        "staticParams": component_path("modules", local_id, "static-params"),
        "mappableParams": component_path("modules", local_id, "mappable-params"),
        "interface": component_path("modules", local_id, "interface"),
        "samples": component_path("modules", local_id, "samples"),
        "scope": component_path("modules", local_id, "scope"),
    }
    if module["moduleType"] == "trigger":
        files["epoch"] = component_path("modules", local_id, "epoch")
    return files


def build_makecomapp() -> dict:
    components = {
        "connection": {
            "apiKey": {
                "label": "Feedjolt API Key",
                "connectionType": "basic",
                "codeFiles": {
                    "communication": component_path("connections", "apiKey", "communication"),
                    "params": component_path("connections", "apiKey", "params"),
                    "common": None,
                },
            }
        },
        "endpoint": {},
        "function": {},
        "module": {},
        "rpc": {},
        "webhook": {
            "watchPostsCreated": {
                "label": "Watch posts created",
                "webhookType": "web",
                "connection": "apiKey",
                "codeFiles": {
                    "communication": component_path("webhooks", "watchPostsCreated", "communication"),
                    "params": component_path("webhooks", "watchPostsCreated", "params"),
                    "attach": component_path("webhooks", "watchPostsCreated", "attach"),
                    "detach": component_path("webhooks", "watchPostsCreated", "detach"),
                    "update": component_path("webhooks", "watchPostsCreated", "update"),
                    "requiredScope": component_path("webhooks", "watchPostsCreated", "required-scope"),
                },
            }
        },
    }

    for local_id, rpc in RPCS.items():
        components["rpc"][local_id] = {
            "label": rpc["label"],
            "connection": "apiKey",
            "codeFiles": {
                "communication": component_path("rpcs", local_id, "communication"),
                "params": component_path("rpcs", local_id, "params"),
            },
        }

    for local_id, module in MODULES.items():
        meta = {
            "label": module["label"],
            "description": module["description"],
            "moduleType": module["moduleType"],
            "connection": "apiKey",
            "codeFiles": module_code_files(local_id, module),
        }
        if "actionCrud" in module:
            meta["actionCrud"] = module["actionCrud"]
        if module.get("webhook"):
            meta["webhook"] = module["webhook"]
        components["module"][local_id] = meta

    return {
        "fileVersion": 1,
        "generalCodeFiles": {
            "base": "base/base.iml.json",
            "common": None,
            "groups": "groups/groups.json",
            "readme": "README.md",
        },
        "components": components,
        # Origin is a placeholder until Marc creates app id `feedjolt` in his zone.
        # Change baseUrl to https://us1.make.com/api (or eu2/us2) to match the account.
        # Put the Make API token in repo-root `.secrets/apikey` (gitignored).
        "origins": [
            {
                "label": "Make (set zone after creating the app)",
                "baseUrl": "https://eu1.make.com/api",
                "appId": "feedjolt",
                "appVersion": 1,
                "apikeyFile": "../../.secrets/apikey",
                "idMapping": {
                    "connection": [],
                    "endpoint": [],
                    "function": [],
                    "module": [],
                    "rpc": [],
                    "webhook": [],
                },
            }
        ],
    }


APP_README = """# Feedjolt

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
"""


def main() -> None:
    if APP.exists():
        # Recreate generated tree but keep README if we overwrite it from this script.
        pass
    APP.mkdir(parents=True, exist_ok=True)

    write(APP / "README.md", APP_README)
    write(APP / "makecomapp.json", dumps(build_makecomapp()))
    write_jsonc(
        "base/base.iml.json",
        "// Inherited by modules, RPCs, and webhook attach/detach.\n"
        "// Auth header uses connection.apiKey from the basic API-key connection.",
        BASE,
    )
    write(APP / "groups/groups.json", dumps(GROUPS))

    write_jsonc(
        component_path("connections", "apiKey", "params"),
        "// Connection parameters shown when the user creates a Feedjolt connection.",
        CONNECTION_PARAMS,
    )
    write_jsonc(
        component_path("connections", "apiKey", "communication"),
        "// Validates the key with GET /api/v1/workspaces (absolute URL; connection does not inherit Base).",
        CONNECTION_COMM,
    )

    for local_id, rpc in RPCS.items():
        write_jsonc(component_path("rpcs", local_id, "params"), "", rpc["params"])
        write_jsonc(component_path("rpcs", local_id, "communication"), "", rpc["communication"])

    write_jsonc(
        component_path("webhooks", "watchPostsCreated", "params"),
        "// Collected when the user creates the webhook in Watch Posts (Instant).",
        WEBHOOK_PARAMS,
    )
    write_jsonc(
        component_path("webhooks", "watchPostsCreated", "communication"),
        "// Incoming Feedjolt delivery. TODO: confirm post.created envelope vs body.post.",
        WEBHOOK_COMM,
    )
    write_jsonc(
        component_path("webhooks", "watchPostsCreated", "attach"),
        "// POST /workspaces/{slug}/webhooks  body: { url: webhook.url, events: [post.created] }",
        WEBHOOK_ATTACH,
    )
    write_jsonc(
        component_path("webhooks", "watchPostsCreated", "detach"),
        "// DELETE /workspaces/{slug}/webhooks/{id} — id comes from attach response.data",
        WEBHOOK_DETACH,
    )
    write_jsonc(
        component_path("webhooks", "watchPostsCreated", "update"),
        "// Reserved by the Apps SDK. Events are fixed to post.created; leave empty.",
        WEBHOOK_UPDATE,
    )
    write_jsonc(
        component_path("webhooks", "watchPostsCreated", "required-scope"),
        "// Unused for API-key auth. Required empty file so the SDK can pull/deploy the section.",
        EMPTY_SCOPE,
    )

    for local_id, module in MODULES.items():
        write_jsonc(component_path("modules", local_id, "communication"), "", module["communication"])
        write_jsonc(component_path("modules", local_id, "static-params"), "", module["staticParams"])
        write_jsonc(component_path("modules", local_id, "mappable-params"), "", module["mappableParams"])
        write_jsonc(component_path("modules", local_id, "interface"), "", module["interface"])
        write_jsonc(component_path("modules", local_id, "samples"), "", module["samples"])
        write_jsonc(
            component_path("modules", local_id, "scope"),
            "// Unused for API-key connections. Present so Clone-to-Local code types stay complete.",
            EMPTY_SCOPE,
        )
        if module["moduleType"] == "trigger":
            write_jsonc(component_path("modules", local_id, "epoch"), "", module["epoch"])

    print(f"Wrote scaffold under {APP}")


if __name__ == "__main__":
    main()
