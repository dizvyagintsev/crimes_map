from fastapi import FastAPI

from app.routers import crimes

app = FastAPI()

app.include_router(crimes.router)
