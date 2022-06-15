from megamarket.api.repository import base


def imports(item, update_date, db):
    return base.imports(item, update_date, db)


def delete(id, db):
    return base.delete(id, db)


def nodes(id, db):
    return base.nodes(id, db)
