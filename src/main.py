from fastapi import FastAPI

from src.api import router

app = FastAPI(title="Website Health Monitor")

app.include_router(router)
