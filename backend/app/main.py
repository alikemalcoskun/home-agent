from fastapi import FastAPI
from app.core.config import cfg
from app.api.router import router
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title=cfg.APP_NAME,
        version=cfg.APP_VERSION,
        debug=cfg.DEBUG,
    )
    app.include_router(router, prefix=cfg.API_PREFIX)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()
