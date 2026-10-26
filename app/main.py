from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app import service
from app.config import APP_PORT, NOTES_PAGE_SIZE

app = FastAPI(title="Notes API")


class NoteIn(BaseModel):
    title: str
    body: str


class NotePatch(BaseModel):
    title: str | None = None
    body: str | None = None


@app.get("/notes")
def list_notes(limit: int = Query(NOTES_PAGE_SIZE, ge=1), offset: int = Query(0, ge=0)):
    return service.fetch_notes(limit=limit, offset=offset)


@app.post("/notes", status_code=201)
def create_note(note: NoteIn):
    try:
        return service.create_note(note.title, note.body)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    note = service.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.patch("/notes/{note_id}")
def update_note(note_id: int, patch: NotePatch):
    try:
        note = service.update_note(note_id, title=patch.title, body=patch.body)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    if not service.delete_note(note_id):
        raise HTTPException(status_code=404, detail="Note not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
