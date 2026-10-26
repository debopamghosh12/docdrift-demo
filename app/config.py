import os

APP_PORT = int(os.getenv("APP_PORT", "8000"))
DATABASE_URL = os.getenv("DATABASE_URL", "memory://")
MAX_NOTE_LENGTH = int(os.getenv("MAX_NOTE_LENGTH", "1000"))
