from uuid import UUID

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from megamarket import schemas
from megamarket.db import get_db
from megamarket.api.repository import base

router = APIRouter(tags=['Base'])


@router.post('/imports', status_code=status.HTTP_200_OK)
async def imports(request: schemas.ShopUnitImportRequest,
                  response: Response,
                  db: Session = Depends(get_db)):
    return base.imports(request, response, db)


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
async def delete(id: UUID, response: Response, db: Session = Depends(get_db)):
    return base.delete(id, response, db)


@router.get('/nodes/{id}', status_code=status.HTTP_200_OK)
async def nodes(id: UUID, response: Response, db: Session = Depends(get_db)):
    return base.nodes(id, response, db)
