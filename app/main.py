from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
import uvicorn

from api import router as api_router
from core.config import Config

config = Config()
ROUTERS = (api_router,)


def prepare_app(routers: tuple[APIRouter]):
    app = FastAPI(
        title=config.app_name,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )
    for router in routers:
        app.include_router(router)

    return app


app = prepare_app(ROUTERS)


@app.on_event('startup')
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
