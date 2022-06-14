from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError

from megamarket import models
from megamarket.db import engine
from megamarket.api.routers import base

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(base.router)
