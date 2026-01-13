import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:

    BASE_URL: str = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30"))
    VERIFY_SSL: bool = os.getenv("VERIFY_SSL", "true").lower() == "true"
        
    @classmethod
    def get_base_url(cls) -> str:
        return cls.BASE_URL
    
settings = Settings()
