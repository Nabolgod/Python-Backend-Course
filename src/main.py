import uvicorn
import sys

from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

# Магическая команда для корректного поиска путей
sys.path.append(str(Path(__file__).parent.parent))

from src.connectors.redis_connector import redis_connector
from src.api.auth import router as auth_router
from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # При старте приложения
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    yield
    # При выключении/перезагрузке приложения
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
