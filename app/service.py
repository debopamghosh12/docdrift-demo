from itertools import count

from app.config import MAX_NOTE_LENGTH

_notes: dict[int, dict] = {}
_ids = count(1)


def create_note(title: str, body: str) -> dict:
    """Create a note and return it. Raises ValueError if body exceeds MAX_NOTE_LENGTH."""
    if len(body) > MAX_NOTE_LENGTH:
        raise ValueError(f"body exceeds MAX_NOTE_LENGTH ({MAX_NOTE_LENGTH})")
    note_id = next(_ids)
    note = {"id": note_id, "title": title, "body": body}
    _notes[note_id] = note
    return note


def list_notes(limit: int = 20) -> list[dict]:
    """Return up to `limit` notes, oldest first."""
    return list(_notes.values())[:limit]


def get_note(note_id: int) -> dict | None:
    """Return the note with the given id, or None if it does not exist."""
    return _notes.get(note_id)


def delete_note(note_id: int) -> bool:
    """Delete the note with the given id. Return True if it existed."""
    return _notes.pop(note_id, None) is not None
