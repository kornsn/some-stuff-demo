import functools

from some_stuff import models
from some_stuff.db import database, some_stuff_tbl


def convert_result(convert_fn):
    def deco(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            rv = await fn(*args, **kwargs)
            return convert_fn(rv)

        return wrapper

    return deco


def to_some_stuff(row):
    if row is None:
        return None
    return models.SomeStuff(id=row["id"], name=row["name"])


def to_some_stuff_list(rows):
    return models.SomeStuffList(items=[to_some_stuff(row) for row in rows])


# @convert_result(to_some_stuff)
async def create_item(params: models.CreateSomeStuffRequest) -> models.SomeStuff:
    query = some_stuff_tbl.insert(values=params.dict()).returning(*some_stuff_tbl.c)
    return await database.fetch_one(query)


# @convert_result(to_some_stuff)
async def get_item(item_id: int) -> models.SomeStuff:
    query = some_stuff_tbl.select(some_stuff_tbl.c.id == item_id)
    return await database.fetch_one(query)


# @convert_result(to_some_stuff_list)
async def get_all(limit: int, offset: int) -> models.SomeStuffList:
    query = some_stuff_tbl.select().limit(limit).offset(offset)
    return await database.fetch_all(query)


# @convert_result(to_some_stuff_list)
async def filter_by_name(name: str, limit: int, offset: int) -> models.SomeStuffList:
    query = some_stuff_tbl.select(some_stuff_tbl.c.name == name).limit(limit).offset(offset)
    return await database.fetch_all(query)


# @convert_result(to_some_stuff)
async def update_item(item_id: int, params: models.UpdateSomeStuffRequest) -> models.SomeStuff:
    query = some_stuff_tbl.update(some_stuff_tbl.c.id == item_id).values(params.dict()).returning(*some_stuff_tbl.c)
    return await database.fetch_one(query)


async def delete_item(item_id: int) -> None:
    query = some_stuff_tbl.delete(some_stuff_tbl.c.id == item_id)
    await database.execute(query)
