from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import heroes


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(heroes.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
