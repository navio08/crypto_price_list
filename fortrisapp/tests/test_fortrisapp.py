import os
import sys

import pytest
from httpx import AsyncClient

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from app import fortrisApi  # noqa: E402


class TestLatest:
    @pytest.mark.anyio
    async def test_get_latest(self):
        async with AsyncClient(app=fortrisApi, base_url="http://test") as ac:
            response = await ac.get("/?limit=3")
        assert response.status_code == 200
        assert "BTC" in response.text

    @pytest.mark.anyio
    async def test_missing_limit_mandatory_parameter(self):
        async with AsyncClient(app=fortrisApi, base_url="http://test") as ac:
            response = await ac.get("/")
        assert response.status_code == 422


# class TestHistorical:
#     @pytest.mark.anyio
#     async def test_get_historical(self):
#         async with AsyncClient(app=fortrisApi, base_url="http://test") as ac:
#             response = await ac.get("/historical?limit=2&date=2023-31-01")

#         assert response.status_code == 200
#         assert (
#             "Your API Key subscription plan doesn't support this endpoint."
#             in response.text
#         )
