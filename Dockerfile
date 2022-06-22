FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port 80 --reload
