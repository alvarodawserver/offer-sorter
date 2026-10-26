from fastapi import FastAPI

from app.routers import offers

app = FastAPI()
app.include_router(offers.router)
