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
| `MAX_NOTE_LENGTH` | `1000`      | Maximum number of characters allowed in a note's `body`. Longer bodies are rejected with `422`. |

Example:

```bash
APP_PORT=9000 MAX_NOTE_LENGTH=500 python -m app.main
```

## Endpoints

A note is a JSON object: `{"id": int, "title": str, "body": str}`. IDs start at 1 and increase.

### `GET /notes`

List notes, oldest first.

Query parameters:
- `limit` (int, optional, default `20`, minimum `1`) — maximum number of notes to return.
- `offset` (int, optional, default `0`, minimum `0`) — number of notes to skip before returning results.

```bash
curl "http://localhost:8000/notes?limit=10&offset=20"
```

`200 OK`
```json
{
  "items": [
  {"id": 1, "title": "Groceries", "body": "Milk, eggs"}
  ],
  "total": 42
}
```

### `POST /notes`

Create a note.

```bash
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Groceries", "body": "Milk"}'
```

`201 Created`
```json
{"id": 1, "title": "Groceries", "body": "Milk"}
```

`422 Unprocessable Entity` if `body` is longer than `MAX_NOTE_LENGTH`:
```json
{"detail": "body exceeds MAX_NOTE_LENGTH (1000)"}
```

### `GET /notes/{note_id}`

Fetch a single note.

```bash
curl http://localhost:8000/notes/1
```

`200 OK`
```json
{"id": 1, "title": "Groceries", "body": "Milk"}
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

`200 OK`
```json
{"deleted": true, "id": 1}
```

`404 Not Found` with `{"detail": "Note not found"}` if the note does not exist.

See [docs/api.md](docs/api.md) for the full endpoint reference.

## Service functions (`app/service.py`)

### `create_note(title, body)`
- `title` (`str`) — note title.
- `body` (`str`) — note body; must be at most `MAX_NOTE_LENGTH` characters.
- Returns the created note as a `dict`. Raises `ValueError` if `body` is too long.

### `list_notes(limit=20)`
- `limit` (`int`, default `20`) — maximum number of notes to return.
- Returns a `list[dict]` of notes, oldest first.

### `get_note(note_id)`
- `note_id` (`int`) — ID of the note.
- Returns the note `dict`, or `None` if it does not exist.

### `delete_note(note_id)`
- `note_id` (`int`) — ID of the note.
- Returns `True` if the note existed and was deleted, `False` otherwise.

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
