import os
import time
from fastapi import FastAPI
from routes.user import router as auth_router
from routes.home import router as home_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(home_router)