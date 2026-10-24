from app.routers import offers
from fastapi import FastAPI

app = FastAPI()
app.include_router(offers.router)
