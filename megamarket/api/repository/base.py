import datetime

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from megamarket import schemas, models
from megamarket.utils import InvalidRequestException


def find_shop_unit_by_id(id, db):
    return db.query(models.ShopUnit).filter(models.ShopUnit.id == id)


def find_statistic_units_by_item_id(id, db):
    return db.query(models.ShopUnitStatistic).filter(
        models.ShopUnitStatistic.item_id == id)


def get_all_categories(db):
    return db.query(models.ShopUnit).filter(
        models.ShopUnit.type == schemas.ShopUnitType['category']).all()


def create_shop_unit(id, name, type, price, parent_id, date):
    return models.ShopUnit(id=id,
                           name=name,
                           type=type,
                           price=price,
                           parentId=parent_id,
                           date=date)


def create_statistic_unit(item, parent_id, date):
    return models.ShopUnitStatistic(
        item_id=item.id,
        name=item.name,
        type=schemas.ShopUnitType(item.type),
        price=item.price,
        parent_id=parent_id,
        item_parent_id=item.parentId,
        date=date)


def imports(item, update_date, db):
    ids = set(db.scalars(select(models.ShopUnit.id)).all())

    if item.parentId and item.parentId not in ids:
        raise InvalidRequestException(f"Parent {item.parentId} not found")

    parent_item = find_shop_unit_by_id(item.parentId, db).first()

    if parent_item and parent_item.type != schemas.ShopUnitType['category']:
        raise InvalidRequestException(
            f"Parent {item.parentId} is not a category")

    old_item = db.query(models.ShopUnit).filter(
        models.ShopUnit.id == item.id)

    if old_item.first():
        old_item.update(item.dict())
        old_item.first().date = update_date

    else:
        shop_item = create_shop_unit(id=item.id,
                                     name=item.name,
                                     type=schemas.ShopUnitType(item.type),
                                     price=item.price,
                                     parent_id=item.parentId,
                                     date=update_date)
        db.add(shop_item)

    db.commit()


def delete(id, db):
    item = find_shop_unit_by_id(id, db).first()
    statistic_items = find_statistic_units_by_item_id(id, db)

    if item:
        for i in statistic_items.all():
            db.delete(i)

        db.delete(item)
        db.commit()
        return item


def nodes(id, db):
    return find_shop_unit_by_id(id, db).options(
        joinedload(models.ShopUnit.children)).first()


def sales(date, db):
    return db.query(models.ShopUnitStatistic).filter(
        and_(
            models.ShopUnitStatistic.date.between(
                date - datetime.timedelta(hours=24),
                date),
            models.ShopUnitStatistic.type == schemas.ShopUnitType['offer'])
    ).order_by(models.ShopUnitStatistic.date).all()


def statistics(id, date_start, date_end, db):
    return db.query(models.ShopUnitStatistic).filter(and_(
        models.ShopUnitStatistic.date.between(date_start, date_end),
        models.ShopUnitStatistic.item_id == id)).order_by(
        models.ShopUnitStatistic.date).all()
