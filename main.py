from fastapi import FastAPI

from megamarket import models
from megamarket.db import engine
from megamarket.api.routers import base
from megamarket.exceptions import create_exceptions
from megamarket.openapi_metadata import change_doc_metadata

app = FastAPI()

change_doc_metadata(app)

create_exceptions(app)

models.Base.metadata.create_all(engine)

app.include_router(base.router)
