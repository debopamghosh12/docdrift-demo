# docdrift-demo — Notes API

A tiny FastAPI "Notes API" used as a test fixture for a docs-sync tool. Notes are stored in memory and are lost when the process exits.

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m app.main             # serves on http://localhost:8000 by default
```

Alternatively, run with uvicorn directly:

```bash
uvicorn app.main:app --port 8000
```

Interactive API docs are available at `http://localhost:8000/docs` once the server is running.

## Configuration

All settings are read from environment variables in `app/config.py` via `os.getenv`.

| Variable          | Default     | Description |
|-------------------|-------------|-------------|
| `APP_PORT`        | `8000`      | Port the server listens on when started with `python -m app.main`. Ignored when launching via `uvicorn` directly (use `--port`). |
| `DATABASE_URL`    | `memory://` | Database connection string. Read but currently unused — storage is always in-memory. |
| `MAX_BODY_LENGTH` | `1000`      | Maximum number of characters allowed in a note's `body`. Longer bodies are rejected with `422`. |
| `NOTES_PAGE_SIZE` | `20`        | Default page size for paginated note listings. |

Example:

```bash
APP_PORT=8000 MAX_BODY_LENGTH=1000 NOTES_PAGE_SIZE=20 python -m app.main
```

## Endpoints

A note is a JSON object: `{"id": int, "title": str, "body": str}`. IDs start at 1 and increase.

### `GET /notes`

List notes, oldest first.

Query parameters:
- `limit` (int, optional, default `20`, minimum `1`) — maximum number of notes to return.
- `offset` (int, optional, default `0`, minimum `0`) — number of notes to skip before returning results.

```bash
curl "http://localhost:8000/notes?limit=10&offset=5"
```

`200 OK`
```json
[
  {"id": 1, "title": "Groceries", "body": "Milk, eggs"}
]
```

### `POST /notes`

Create a note.

```bash
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Groceries", "body": "Milk, eggs"}'
```

`201 Created`
```json
{"id": 1, "title": "Groceries", "body": "Milk, eggs"}
```

`422 Unprocessable Entity` if `body` is longer than `MAX_BODY_LENGTH`:
```json
{"detail": "body exceeds MAX_BODY_LENGTH (1000)"}
```

### `GET /notes/{note_id}`

Fetch a single note.

```bash
curl http://localhost:8000/notes/1
```

`200 OK`
```json
{"id": 1, "title": "Groceries", "body": "Milk, eggs"}
```

`404 Not Found`
```json
{"detail": "Note not found"}
```

### `DELETE /notes/{note_id}`

Delete a note.

```bash
curl -X DELETE http://localhost:8000/notes/1
```

`204 No Content` on success (empty body). `404 Not Found` with `{"detail": "Note not found"}` if the note does not exist.

### `PATCH /notes/{note_id}`

Update an existing note. Only the fields provided in the request body are changed; omitted fields remain unchanged.

**Request body** (JSON, fields optional):
```json
{ "title": "string", "body": "string" }
```

**Responses**
- `200 OK` – Returns the updated note.
  ```json
  {"id": 1, "title": "...", "body": "..."}
  ```
- `404 Not Found` – The note with the given `note_id` does not exist.
  ```json
  {"detail": "Note not found"}
  ```
- `422 Unprocessable Entity` – Validation error (e.g., body exceeds the maximum length).
  ```json
  {"detail": "..."}
  ```

See [docs/api.md](docs/api.md) for the full endpoint reference.

## Service functions (`app/service.py`)

### `create_note(title, body)`
- `title` (`str`) — note title.
- `body` (`str`) — note body; must be at most `MAX_BODY_LENGTH` characters.
- Returns the created note as a `dict`. Raises `ValueError` if `body` is too long.

### `fetch_notes(limit=20, offset=0)`
- `limit` (`int`, default `20`) — maximum number of notes to return.
- `offset` (`int`, default `0`) — number of notes to skip before returning results.
- Returns a `list[dict]` of notes, oldest first.

### `get_note(note_id)`
- `note_id` (`int`) — ID of the note.
- Returns the note `dict`, or `None` if it does not exist.

### `delete_note(note_id)`
- `note_id` (`int`) — ID of the note.
- Returns `True` if the note existed and was deleted, `False` otherwise.

### `update_note(note_id, title=None, body=None)`
- `note_id` (`int`) — ID of the note to update.
- `title` (`str`, optional) — New title for the note; if omitted the title is left unchanged.
- `body` (`str`, optional) — New body for the note; if omitted the body is left unchanged. Must be at most `MAX_BODY_LENGTH` characters.

Returns the updated note as a `dict`, or `None` if the note does not exist. Raises `ValueError` if `body` exceeds `MAX_BODY_LENGTH`.

## Project layout

```
app/
  config.py    # environment-variable settings
  main.py      # FastAPI routes
  service.py   # in-memory note storage and business logic
docs/
  api.md       # full endpoint reference
requirements.txt
```
