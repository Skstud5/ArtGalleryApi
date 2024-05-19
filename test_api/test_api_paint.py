import pytest
from httpx import AsyncClient, ASGITransport
from logger.logger import log_tests_info

from main import app


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200


@pytest.fixture
async def async_client():
    """Fixture to create a FastAPI test client."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_test_client:
        yield async_test_client


@pytest.mark.asyncio
async def test_404_get_paint(async_client):
    log_tests_info("Поиск картины с ID 123...")
    response = await async_client.get("/paint/-5")  # Предполагается, что "-5" - это несуществующий идентификатор
    log_tests_info("Код статуса ответа: %s" % response.status_code)
    assert response.status_code == 404
