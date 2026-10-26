import os

APP_PORT = int(os.getenv("APP_PORT", "8000"))
DATABASE_URL = os.getenv("DATABASE_URL", "memory://")
MAX_BODY_LENGTH = int(os.getenv("MAX_BODY_LENGTH", "10"))
NOTES_PAGE_SIZE = int(os.getenv("NOTES_PAGE_SIZE", "20"))
