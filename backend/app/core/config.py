from starlette.config import Config
from pydantic_settings import BaseSettings

config = Config(".env")

class Cfg(BaseSettings):
    APP_NAME: str = "Home Agent: Multi-Agent System for Home Automation"
    APP_VERSION: str = "0.0.1"
    API_PREFIX: str = "/api"
    DEBUG: bool = config("DEBUG", cast=bool, default=False)


cfg = Cfg()
