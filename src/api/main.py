from loguru import logger
from fastapi import Depends, FastAPI

from src.api.core.authentication_middleware import authenticate_user
from src.api.core.config import get_config
from src.api.routes import health, items

get_config()

app = FastAPI()

app.include_router(items.router, dependencies=[Depends(authenticate_user)])
app.include_router(health.router)

@app.get("/")
async def read_root():
    logger.debug("This is a debug log")
    logger.info("This is an info log")
    return {"Hello": "World"}
