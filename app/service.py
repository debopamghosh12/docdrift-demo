from itertools import count

from app.config import MAX_BODY_LENGTH

_notes: dict[int, dict] = {}
_ids = count(1)


def _check_body(body: str) -> None:
    if len(body) > MAX_BODY_LENGTH:
        raise ValueError(f"body exceeds MAX_BODY_LENGTH ({MAX_BODY_LENGTH})")


def create_note(title: str, body: str) -> dict:
    """Create a note and return it. Raises ValueError if body exceeds MAX_BODY_LENGTH."""
    _check_body(body)
    note_id = next(_ids)
    note = {"id": note_id, "title": title, "body": body}
    _notes[note_id] = note
    return note


def fetch_notes(limit: int = 20, offset: int = 0) -> list[dict]:
    """Return up to `limit` notes, oldest first, skipping the first `offset`."""
    return list(_notes.values())[offset : offset + limit]


def _count_notes() -> int:
    return len(_notes)


def get_note(note_id: int) -> dict | None:
    """Return the note with the given id, or None if it does not exist."""
    return _notes.get(note_id)


def update_note(note_id: int, title: str | None = None, body: str | None = None) -> dict | None:
    """Update the given fields of a note and return it, or None if it does not exist.

    Raises ValueError if body exceeds MAX_BODY_LENGTH.
    """
    note = _notes.get(note_id)
    if note is None:
        return None
    if body is not None:
        _check_body(body)
        note["body"] = body
    if title is not None:
        note["title"] = title
    return note


def delete_note(note_id: int) -> bool:
    """Delete the note with the given id. Return True if it existed."""
    return _notes.pop(note_id, None) is not None
