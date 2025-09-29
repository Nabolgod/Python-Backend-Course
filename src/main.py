from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

# Магическая команда для корректного поиска путей

sys.path.append(str(Path(__file__).parent.parent))
from src.api.hotels import router as hotels_router
from src.config import settings

print(f"{settings.__dict__=}")
app = FastAPI()
app.include_router(hotels_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
