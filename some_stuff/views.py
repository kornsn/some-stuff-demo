from fastapi import APIRouter, HTTPException
from fastapi import status

from some_stuff import models, repo

router = APIRouter()


@router.post(
    "/",
    response_model=models.SomeStuff,
    response_description="Created instance of SomeStuff",
    status_code=status.HTTP_201_CREATED,
)
async def create_some_stuff(params: models.CreateSomeStuffRequest):
    return await repo.create_item(params)


@router.get(
    "/",
    summary="List Some Stuff",
    response_model=models.SomeStuffList,
    response_description="Instances of SomeStuff",
)
async def list_some_stuff(name: str = None, limit: int = 10, offset: int = 0):
    if not name:
        items = await repo.get_all(limit=limit, offset=offset)
    else:
        items = await repo.filter_by_name(name, limit=limit, offset=offset)
    return models.SomeStuffList(
        items=items,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{item_id}",
    response_model=models.SomeStuff,
    response_description="Instance of SomeStuff",
)
async def get_some_stuff(item_id: int):
    rv = await repo.get_item(item_id)
    if not rv:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return rv


@router.put(
    "/{item_id}",
    response_model=models.SomeStuff,
    response_description="Updated instance of SomeStuff",
)
async def update_some_stuff(item_id: int, params: models.UpdateSomeStuffRequest):
    rv = await repo.update_item(item_id, params)
    if not rv:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return rv


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_some_stuff(item_id: int):
    await repo.delete_item(item_id)
