import os
import sys

import pytest
from httpx import AsyncClient

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from app import coinmarketApp  # noqa: E402


@pytest.mark.anyio
async def test_get_latest():
    async with AsyncClient(app=coinmarketApp, base_url="http://test") as ac:
        response = await ac.get("/latest")

    assert response.status_code == 200
    assert "data" in response.json()

