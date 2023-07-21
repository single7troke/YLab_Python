from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from api.v1 import menus, submenus, dishes
from core.config import Config

config = Config()


app = FastAPI(
    title=config.app_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    pass


@app.get("/")
async def root():
    return {"message": "Hello World"}


# app.include_router(menus.router, prefix="/api/v1/menus", tags=["menus"])
# app.include_router(submenus.router, prefix="/api/v1/submenus", tags=["submenus"])
# app.include_router(dishes.router, prefix="/api/v1/dishes", tags=["dishes"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
