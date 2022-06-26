# Mega Market API

## Description
Market REST API. [OpenAPI](https://github.com/nikitakosatka/mega-market-api/blob/master/openapi.yaml). Swagger documentation is available on ```/docs```

### Endpoints

#### Base

```POST /imports```
```DELETE /delete/{id}```
```GET /nodes/{id}```

#### Statistics

```/sales```
```/node/{id}/statistic```

### Deploy

#### Build
```make build``` or ```docker-compose build```

#### Run
```make run``` or ```docker-compose up -d```

#### Stop
```make stop``` or ```docker-compose down```

### Used technologies

- Python 3.10
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker / docker-compose