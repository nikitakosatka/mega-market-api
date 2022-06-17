from uuid import UUID

from fastapi import APIRouter, Depends, status, Response, Body
from sqlalchemy.orm import Session

from megamarket import schemas
from megamarket.db import get_db
from megamarket.api.services import base
from megamarket.api.routers.example_values import *
from megamarket.utils import InvalidRequestException, NotFoundException

router = APIRouter(tags=['Base'])


@router.post(
    '/imports',
    status_code=status.HTTP_200_OK,
    responses=imports_responses)
async def imports(
        request: schemas.ShopUnitImportRequest = Body(
            example=imports_request_example),
        db: Session = Depends(get_db)
):
    for item in request.items:
        base.imports(item, request.updateDate, db)

    return status.HTTP_200_OK


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK,
               responses=delete_responses)
async def delete(id: UUID, response: Response, db: Session = Depends(get_db)):
    item = base.delete(id, db)

    if not item:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise InvalidRequestException(f"Item with Id {id} not found")

    return status.HTTP_200_OK


@router.get('/nodes/{id}', status_code=status.HTTP_200_OK,
            response_model=schemas.ShopUnit,
            responses=nodes_responses)
async def nodes(id: UUID,
                response: Response = Body(example=nodes_response_example),
                db: Session = Depends(get_db)):
    item = base.nodes(id, db)

    if not item:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise NotFoundException(f"Item with Id {id} not found")

    return item
