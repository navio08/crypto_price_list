import os
import sys

import pytest
from httpx import AsyncClient

from data.responses import response200

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from app import cryptorankApi, cryptorankApp  # noqa: E402


class TestRank:
    @pytest.mark.anyio
    async def test_get_ranklatest(self):
        async with AsyncClient(app=cryptorankApi, base_url="http://test") as ac:
            response = await ac.get("/ranklatest?limit=1")

        assert response.status_code == 200
        assert "BTC" in response.text

    @pytest.mark.anyio
    async def test_missing_limit_mandatory_parameter(self):
        async with AsyncClient(app=cryptorankApi, base_url="http://test") as ac:
            response = await ac.get("/ranklatest")

        assert response.status_code == 422


class TestCleaningResponses:
    @pytest.mark.anyio
    async def test_clean_good_data(self):
        app = cryptorankApp()
        clean_data = app.clean(response200)
        assert clean_data == {"BTC": 1, "ETH": 2, "USDT": 3, "XRP": 4, "BNB": 5}


