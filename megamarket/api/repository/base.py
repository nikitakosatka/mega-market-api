from fastapi import Response, status
from sqlalchemy.orm import Session

from megamarket import schemas, models
from megamarket.schemas import Error


def imports(request: schemas.ShopUnitImportRequest,
            response: Response,
            db: Session):
    update_date = request.updateDate
    response.status_code = status.HTTP_400_BAD_REQUEST

    if len(set(item.id for item in request.items)) != len(request.items):
        return Error(code=400,
                     message="Request must not contain elements with the same id")

    ids = set(i.id for i in db.query(models.ShopUnit).all())

    for item in request.items:
        if item.parentId not in ids:
            return Error(code=400,
                         message=f"ParentId not found")

        if item.type == schemas.ShopUnitType['category'] and item.price:
            return Error(code=400,
                         message="Category price must be null")

        if item.type == schemas.ShopUnitType['offer'] and (
                not item.price or item.price < 0):
            return Error(code=400,
                         message="Offer price must be greater or equal to 0")

        parent_item = db.query(models.ShopUnit).filter(
            models.ShopUnit.id == item.parentId).first()

        if parent_item and parent_item.type != schemas.ShopUnitType['category']:
            return Error(code=400,
                         message="Parent must be category")

        old_item = db.query(models.ShopUnit).filter(
            models.ShopUnit.id == item.id)

        if old_item.first():
            old_item.update(item.dict())
            old_item.first().updateDate = update_date

        else:
            shop_item = models.ShopUnit(id=item.id,
                                        name=item.name,
                                        type=models.ShopUnitType(item.type),
                                        price=item.price,
                                        parentId=item.parentId,
                                        updateDate=update_date)

            ids.add(shop_item.id)
            db.add(shop_item)

        db.commit()

    response.status_code = status.HTTP_200_OK

    return status.HTTP_200_OK
