from collections import deque

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from megamarket import schemas, models
from megamarket.utils import InvalidRequestException


def update_category_prices(id, dt, db):
    item = find_by_id(id, db).first()
    if not item:
        return
    parent = find_by_id(item.parentId, db).first()

    if item.type == schemas.ShopUnitType['category']:
        queue = deque()
        prices_sum, prices_count = 0, 0

        queue.append(item)

        while queue:
            current = queue.popleft()

            for child in current.children:
                if child.type == schemas.ShopUnitType['offer']:
                    prices_sum += child.price
                    prices_count += 1
                else:
                    queue.append(child)

        if prices_count != 0:
            item.price = prices_sum // prices_count
            item.date = dt

    if not parent:
        return

    update_category_prices(parent.id, dt, db)


def find_by_id(id, db):
    return db.query(models.ShopUnit).filter(models.ShopUnit.id == id)


def create(id, name, type, price, parentId, date):
    return models.ShopUnit(id=id,
                           name=name,
                           type=type,
                           price=price,
                           parentId=parentId,
                           date=date)


def imports(item, update_date, db):
    ids = set(db.scalars(select(models.ShopUnit.id)).all())

    if item.parentId and item.parentId not in ids:
        raise InvalidRequestException(f"Parent {item.parentId} not found")

    parent_item = find_by_id(item.parentId, db).first()

    if parent_item and parent_item.type != schemas.ShopUnitType['category']:
        raise InvalidRequestException(
            f"Parent {item.parentId} is not a category")

    old_item = db.query(models.ShopUnit).filter(
        models.ShopUnit.id == item.id)

    if old_item.first():
        old_item.update(item.dict())
        old_item.first().date = update_date

    else:
        shop_item = create(id=item.id,
                           name=item.name,
                           type=models.ShopUnitType(item.type),
                           price=item.price,
                           parentId=item.parentId,
                           date=update_date,
                           )
        db.add(shop_item)

    db.commit()

    if item.price:
        update_category_prices(item.id, update_date, db)

    db.commit()


def delete(id, db):
    item = find_by_id(id, db).first()

    if item:
        db.delete(item)
        db.commit()
        return item


def nodes(id, db):
    return find_by_id(id, db).options(
        joinedload(models.ShopUnit.children)).first()
