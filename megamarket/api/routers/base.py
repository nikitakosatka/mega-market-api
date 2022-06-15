from uuid import UUID

from fastapi import APIRouter, Depends, status, Response, Body
from pydantic import ValidationError
from sqlalchemy.orm import Session

from megamarket import schemas
from megamarket.db import get_db
from megamarket.api.services import base
from megamarket.schemas import Error
from megamarket.utils import *

router = APIRouter(tags=['Base'])


@router.post('/imports', status_code=status.HTTP_200_OK,
             responses={
                 200: {
                     "description": "Items were imported",
                     "content": {
                         "application/json": {
                             "example": 200}
                     }
                 },
                 400: {"model": Error, "description": "Validation Error",
                       "content": {
                           "application/json": {
                               "example": error_400_example}
                       }
                       }
             })
async def imports(
        request: schemas.ShopUnitImportRequest = Body(
            example=imports_request_example),
        response: Response = status.HTTP_200_OK,
        db: Session = Depends(get_db)
):
    try:
        request_ids_set = set(item.id for item in request.items)

        if len(request_ids_set) != len(request.items):
            raise ValidationError

        for item in request.items:
            if item.type == schemas.ShopUnitType['category'] and item.price:
                raise ValidationError

            if item.type == schemas.ShopUnitType['offer'] and (
                    not item.price or item.price < 0):
                raise ValidationError

            base.imports(item, request.updateDate, db)

    except ValidationError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Error(code=400,
                     message="Validation Failed")

    return status.HTTP_200_OK


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK,
               responses={
                   200: {
                       "description": "Item was successfully deleted",
                       "content": {
                           "application/json": {
                               "example": 200}
                       }
                   },
                   400: {"model": Error, "description": "Validation Error",
                         "content": {
                             "application/json": {
                                 "example": error_400_example}
                         }
                         },
                   404: {"model": Error, "description": "Item not found",
                         "content": {
                             "application/json": {
                                 "example": error_404_example}
                         }
                         }
               })
async def delete(id: UUID, response: Response, db: Session = Depends(get_db)):
    try:
        item = base.delete(id, db)

        if not item:
            response.status_code = status.HTTP_404_NOT_FOUND
            return Error(code=404,
                         message="Item not found")

    except ValidationError:
        return Error(code=400,
                     message="Validation Failed")

    return status.HTTP_200_OK


@router.get('/nodes/{id}', status_code=status.HTTP_200_OK,
            response_model=schemas.ShopUnit,
            responses={
                200: {
                    "description": "Item requested by ID",
                    "content": {
                        "application/json": {
                            "example": nodes_response_example}
                    }
                },
                400: {"model": Error, "description": "Validation Error",
                      "content": {
                          "application/json": {
                              "example": error_400_example}
                      }
                      },
                404: {"model": Error, "description": "Item not found",
                      "content": {
                          "application/json": {
                              "example": error_404_example}
                      }
                      }
            })
async def nodes(id: UUID,
                response: Response = Body(example=nodes_response_example),
                db: Session = Depends(get_db)):
    try:
        item = base.nodes(id, db)

        if not item:
            response.status_code = status.HTTP_404_NOT_FOUND
            return Error(code=404,
                         message="Item not found")

    except ValidationError:
        return Error(code=400,
                     message="Validation Failed")

    return item
