# Notes API — Endpoint Reference

Base URL: `http://localhost:8000` (port set by `APP_PORT`).

All request and response bodies are JSON. Storage is in-memory; data is lost on restart.

## Note object

| Field   | Type    | Description |
|---------|---------|-------------|
| `id`    | integer | Server-assigned ID, starting at 1 and incrementing. IDs are never reused. |
| `title` | string  | Note title. |
| `body`  | string  | Note body, at most `MAX_NOTE_LENGTH` characters (default 1000). |

## Errors

Errors are returned as `{"detail": ...}` with an appropriate status code:

| Status | When |
|--------|------|
| `404 Not Found` | The requested `note_id` does not exist. `detail` is `"Note not found"`. |
| `422 Unprocessable Entity` | Request validation failed: missing/invalid fields, non-integer `note_id`, `limit < 1`, or `body` longer than `MAX_NOTE_LENGTH`. For FastAPI validation errors `detail` is a list of error objects; for the length check it is the string `"body exceeds MAX_NOTE_LENGTH (<n>)"`. |

---

## List notes

`GET /notes`

Returns notes in creation order (oldest first), up to `limit`.

**Query parameters**

| Name    | Type    | Required | Default | Constraints |
|---------|---------|----------|---------|-------------|
| `limit` | integer | no       | `20`    | `>= 1` |

**Request**
```http
GET /notes?limit=2
```

**Response — `200 OK`**
```json
{
  "items": [],
  "total": 0
}
```

An empty store returns `[]`.

---

## Create a note

`POST /notes`

**Request body**

| Field   | Type   | Required |
|---------|--------|----------|
| `title` | string | yes |
| `body`  | string | yes |

**Request**
```http
POST /notes
Content-Type: application/json

{"title": "Groceries", "body": "Milk, eggs"}
```

**Response — `201 Created`**
```json
{"id": 1, "title": "Groceries", "body": "Milk, eggs"}
```

**Response — `422 Unprocessable Entity`** (body too long)
```json
{"detail": "body exceeds MAX_NOTE_LENGTH (1000)"}
```

---

## Get a note

`GET /notes/{note_id}`

**Path parameters**

| Name      | Type    | Description |
|-----------|---------|-------------|
| `note_id` | integer | ID of the note. |

**Request**
```http
GET /notes/1
```

**Response — `200 OK`**
```json
{"id": 1, "title": "Groceries", "body": "Milk, eggs"}
```

**Response — `404 Not Found`**
```json
{"detail": "Note not found"}
```

---

## Delete a note

`DELETE /notes/{note_id}`

**Path parameters**

| Name      | Type    | Description |
|-----------|---------|-------------|
| `note_id` | integer | ID of the note. |

**Request**
```http
DELETE /notes/1
```

**Response — `200 OK`**
```json
{"deleted":true,"id":1}
```

Empty body.

**Response — `404 Not Found`**
```json
{"detail": "Note not found"}
```
