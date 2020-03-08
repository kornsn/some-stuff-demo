from fastapi import FastAPI, Depends, status, responses

from settings import settings
from some_stuff import views, db, auth

app = FastAPI(
    title="Some Stuff Demo",
    debug=settings.debug,
)
app.include_router(
    views.router,
    prefix="/some-stuff",
    tags=["SomeStuff"],
    dependencies=[Depends(auth.check_api_key)],
)


@app.get("/", include_in_schema=False)
async def home():
    return responses.RedirectResponse('/docs')


@app.on_event("startup")
async def startup():
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()
