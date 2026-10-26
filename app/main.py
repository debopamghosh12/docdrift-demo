from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app import service
from app.config import APP_PORT

app = FastAPI(title="Notes API")


class NoteIn(BaseModel):
    title: str
    body: str


@app.get("/notes")
def list_notes(limit: int = Query(20, ge=1)):
    return service.list_notes(limit=limit)


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


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    if not service.delete_note(note_id):
        raise HTTPException(status_code=404, detail="Note not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
