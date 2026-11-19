from methin.db import check_connection


async def test_database_reachable(engine):
    await check_connection(engine)
