from fastapi import FastAPI

from megamarket import models
from megamarket.db import engine

app = FastAPI()

models.Base.metadata.create_all(engine)