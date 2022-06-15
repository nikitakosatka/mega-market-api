from fastapi import FastAPI

from megamarket import models
from megamarket.db import engine
from megamarket.api.routers import base
from megamarket.middleware import create_middleware

app = FastAPI()

create_middleware(app)

models.Base.metadata.create_all(engine)

app.include_router(base.router)
