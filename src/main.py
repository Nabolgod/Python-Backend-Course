from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

# Магическая команда для корректного поиска путей
sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as auth_router
from src.api.hotels import router as hotels_router

# from src.database import *
# from src.config import settings


# # Никогда не логгировать данный адрес (именно пароль)
# print(f"{settings.__dict__=}")
# print(settings.DB_URL)

app = FastAPI()
app.include_router(auth_router)
app.include_router(hotels_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
