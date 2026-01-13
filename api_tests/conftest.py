import pytest
import logging
import random
import threading
from typing import Generator

from api_tests.api.pet_client import PetClient
from api_tests.models.pet import Pet, Category, Tag

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def api_client() -> Generator[PetClient, None, None]:
    client = PetClient()
    yield client
    client.close()


@pytest.fixture
def sample_pet():
    thread_id = threading.get_ident()
    random_id = random.randint(100000, 999999)
    unique_id = int(f"{thread_id % 10000}{random_id % 10000}")
    
    return Pet(
        id=unique_id,
        category=Category(id=random.randint(1, 1000), name="Dogs"),
        name=f"Test Dog {unique_id}",
        photoUrls=["https://example.com/photo.jpg"],
        tags=[Tag(id=random.randint(1, 1000), name="test-tag")],
        status="available"
    )


@pytest.fixture(autouse=True)
def log_test_start(request):
    logger.info(f"Starting test: {request.node.name}")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: Smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: Regression tests"
    )
