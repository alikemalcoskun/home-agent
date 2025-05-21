from fastapi import APIRouter, status

from app.models.key import CheckKeyResponse

import os
from dotenv import load_dotenv
from loguru import logger


router = APIRouter()

@router.get(
        path="/check",
        name="Check API Key",
        description=(
            "Check the API key to see if it is valid."
        ),
        status_code=status.HTTP_200_OK,
        response_model=CheckKeyResponse)
def check_api_key():
    logger.info("Checking API key.")
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
    if OPENAI_API_KEY is None:
        logger.error("OPENAI_API_KEY environment variable is not set")
        return CheckKeyResponse(ok=False)
    logger.info("API key is valid.")
    return CheckKeyResponse(ok=True)

