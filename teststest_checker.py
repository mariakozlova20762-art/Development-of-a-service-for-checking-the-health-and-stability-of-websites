import pytest

from src.checker import check_website


@pytest.mark.asyncio
async def test_google_is_healthy():
    status_code, response_time, healthy = await check_website(
        "https://www.google.com"
    )

    assert status_code == 200
    assert response_time > 0
    assert healthy is True