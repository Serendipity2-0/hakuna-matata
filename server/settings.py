import logging
import pathlib
from datetime import UTC, timezone
from typing import Optional

from dotenv import load_dotenv
from pydantic import ValidationError
from pydantic_settings import BaseSettings

load_dotenv(verbose=True, override=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
log_format = "%(levelname) -10s %(funcName) " "-25s %(lineno) -1d: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)


class Settings(BaseSettings):
    ASSEMBLYAI_API_KEY: str
    ASSEMBLYAI_BASE_URL: str
    OPENAI_ORG_KEY: str
    OPENAI_API_KEY: str

    # OPTIONAL SETTINGS
    FILE_DELETE_TIME: int = 60
    LOGGER: Optional[logging.Logger] = logging.getLogger(__name__)
    UPLOAD_DIR: str = f"{ROOT}/uploads"

    class Config:
        case_sensitive = False
        env_file = f"{ROOT}/.env"


try:
    settings = Settings()
except ValidationError as exc:
    logging.getLogger(__name__).error(repr(exc.errors()))
