import pytest_asyncio

from methin.config import get_settings
from methin.db import make_engine


@pytest_asyncio.fixture(scope="session")
async def engine():
    """Silnik do bazy testowej (methin_test). Testy współbieżności muszą iść na prawdziwy Postgres."""
    eng = make_engine(get_settings().test_database_url)
    yield eng
    await eng.dispose()
