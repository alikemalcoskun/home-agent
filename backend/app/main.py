from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router as api_router
from app.core.config import cfg


def create_app() -> FastAPI:
    app = FastAPI(
        title=cfg.APP_NAME,
        version=cfg.APP_VERSION,
        debug=cfg.DEBUG,
    )
    app.include_router(api_router, prefix=cfg.API_PREFIX)

    # Add CORS middleware with WebSocket support
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
        expose_headers=["*"],  # Exposes all headers
    )

    # Mount static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    return app


app = create_app()
