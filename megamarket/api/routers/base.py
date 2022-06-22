from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.orm import Session

from megamarket import schemas
from megamarket.db import get_db
from megamarket.api.services import base
from megamarket.api.routers.example_values import *
from megamarket.utils import NotFoundException

router = APIRouter(tags=['Базовые задачи'])


@router.post(
    '/imports',
    status_code=status.HTTP_200_OK,
    responses=imports_responses)
async def imports(
        request: schemas.ShopUnitImportRequest = Body(
            example=imports_request_example),
        db: Session = Depends(get_db)
):
    """
    Импортирует новые товары и/или категории. Товары/категории импортированные
    повторно обновляют текущие. Изменение типа элемента с товара на категорию
    или с категории на товар не допускается. Порядок элементов в запросе
    является произвольным.
    """
    for item in request.items:
        base.imports(item, request.updateDate, db)

    return status.HTTP_200_OK


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK,
               responses=delete_responses)
async def delete(id: UUID, db: Session = Depends(get_db)):
    """
    Удалить элемент по идентификатору. При удалении категории удаляются все
    дочерние элементы. Доступ к статистике (истории обновлений) удаленного
    элемента невозможен.
    """
    item = base.delete(id, db)

    if not item:
        raise NotFoundException(f"Item with Id {id} not found")

    return status.HTTP_200_OK


@router.get('/nodes/{id}', status_code=status.HTTP_200_OK,
            response_model=schemas.ShopUnit,
            responses=nodes_responses)
async def nodes(id: UUID, db: Session = Depends(get_db)):
    """
    Получить информацию об элементе по идентификатору. При получении информации
    о категории также предоставляется информация о её дочерних элементах.
    """
    item = base.nodes(id, db)

    if not item:
        raise NotFoundException(f"Item with Id {id} not found")

    return item


@router.get('/sales', status_code=status.HTTP_200_OK,
            response_model=schemas.ShopUnitStatisticResponse,
            responses=sales_responses)
async def sales(date: datetime, db: Session = Depends(get_db)):
    """
    Получение списка товаров, цена которых была обновлена за последние 24 часа
    от времени переданном в запросе. Обновление цены не означает её изменение.
    Обновления цен удаленных товаров недоступны. При обновлении цены товара,
    средняя цена категории, которая содержит этот товар, тоже обновляется.
    """
    return base.sales(date, db)
