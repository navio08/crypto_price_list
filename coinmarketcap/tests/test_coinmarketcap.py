import os
import sys

import pytest
from httpx import AsyncClient

from data.responses import response200

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from app import coinmarketApi, coinmarketApp  # noqa: E402


class TestLatest:
    @pytest.mark.anyio
    async def test_get_latest(self):
        async with AsyncClient(app=coinmarketApi, base_url="http://test") as ac:
            response = await ac.get("/latest?limit=3")

        assert response.status_code == 200
        assert "BTC" in response.text

    @pytest.mark.anyio
    async def test_missing_limit_mandatory_parameter(self):
        async with AsyncClient(app=coinmarketApi, base_url="http://test") as ac:
            response = await ac.get("/latest")

        assert response.status_code == 422


class TestCleaningResponses:
    @pytest.mark.anyio
    async def test_clean_good_data(self):
        app = coinmarketApp()
        clean_data = app.clean(response200)
        assert clean_data == {
            "BTC": 29944.583658299423,
            "ETH": 1893.1278458807567,
            "USDT": 1.0001895148353193,
        }


class TestHistorical:
    @pytest.mark.anyio
    async def test_get_historical(self):
        async with AsyncClient(app=coinmarketApi, base_url="http://test") as ac:
            response = await ac.get("/historical?limit=2&date=2023-31-01")

        assert response.status_code == 200
        assert (
            "Your API Key subscription plan doesn't support this endpoint."
            in response.text
        )


class TestCorrelationId:
    @pytest.mark.anyio
    async def test_get_ranklatest(self):
        async with AsyncClient(app=coinmarketApi, base_url="http://test") as ac:
            response = await ac.get("/ranklatest?limit=1", headers={"cid": "testcid"})

        assert response.headers["cid"] == "testcid"
