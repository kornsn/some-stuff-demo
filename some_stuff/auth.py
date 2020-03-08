from fastapi import Security, HTTPException
from fastapi import status
from fastapi.security import APIKeyQuery, APIKeyHeader, APIKeyCookie

from settings import settings

api_key = settings.api_key
api_key_name = settings.api_key_name

api_key_query = APIKeyQuery(name=api_key_name, auto_error=False)
api_key_header = APIKeyHeader(name=api_key_name, auto_error=False)
api_key_cookie = APIKeyCookie(name=api_key_name, auto_error=False)


async def check_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):
    if api_key not in (api_key_query, api_key_header, api_key_cookie):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials",
        )
