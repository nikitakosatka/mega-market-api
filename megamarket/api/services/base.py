from collections import deque

from megamarket import schemas
from megamarket.api.repository import base
from megamarket.utils import InvalidRequestException


def update_category_prices(id, dt, db):
    item = base.find_by_id(id, db).first()

    if not item:
        return

    parent = base.find_by_id(item.parentId, db).first()

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

    db.commit()


def imports(items, datetime, db):
    exist_ids = set(i.id for i in base.get_all_categories(db))

    new_ids = set(
        i.id for i in items if i.type == schemas.ShopUnitType['category']
    )

    items_without_new_parent_id = []
    items_with_new_parent_id = []

    for item in items:
        if not item.parentId or item.parentId in exist_ids:
            items_without_new_parent_id.append(item)

        elif item.parentId in new_ids:
            items_with_new_parent_id.append(item)

        else:
            raise InvalidRequestException

    for item in items_without_new_parent_id:
        _import(item, datetime, db)
        update_category_prices(item.id, datetime, db)

    for item in items_with_new_parent_id:
        new_item = item.copy()
        new_item.parentId = None
        _import(new_item, datetime, db)

    for item in items_with_new_parent_id:
        new_item = base.find_by_id(item.id, db)
        new_item.update(item.dict())
        db.commit()
        update_category_prices(item.id, datetime, db)


def _import(item, update_date, db):
    base.imports(item, update_date, db)


def delete(id, db):
    return base.delete(id, db)


def nodes(id, db):
    return base.nodes(id, db)


def sales(date, db):
    return schemas.ShopUnitStatisticResponse(
        items=[u.__dict__ for u in base.sales(date, db)])
