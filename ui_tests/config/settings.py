import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:

    BASE_URL: str = os.getenv("BASE_URL", "https://insiderone.com")
    HOME_PAGE_URL: str = f"{BASE_URL}/"
    QA_JOBS_PAGE_URL: str = f"{BASE_URL}/careers/quality-assurance/"
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))

settings = Settings()
