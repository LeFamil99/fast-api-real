from fastapi import HTTPException, Security
from fastapi.params import Depends
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from src.api.core.config import Config, get_config


async def authenticate_user(
    config: Config = Depends(get_config),
    api_key_header: str = Security(
        APIKeyHeader(name="Authorization", auto_error=False)
    ),
) -> str:
    if api_key_header == config.api_key:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate API KEY"
    )
