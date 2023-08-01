import os
import sys

import pytest
from data.responses import response200
from httpx import AsyncClient

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from app import coinmarketApi, coinmarketApp  # noqa: E402


class ResponseMockOK:
    text = response200
    status_code = 200


class TestLatest:
    @pytest.mark.anyio
    async def test_missing_limit_mandatory_parameter(self):
        async with AsyncClient(app=coinmarketApi, base_url="http://test") as ac:
            response = await ac.get("/latest")

        assert response.status_code == 422


class TestCleaningResponses:
    @pytest.mark.anyio
    async def test_clean_good_data(self):
        app = coinmarketApp()

        clean_data = app.clean(ResponseMockOK)
        assert clean_data == {
            "BTC": 29944.583658299423,
            "ETH": 1893.1278458807567,
            "USDT": 1.0001895148353193,
        }


class TestCorrelationId:
    @pytest.mark.anyio
    async def test_get_ranklatest(self):
        async with AsyncClient(app=coinmarketApi, base_url="http://test") as ac:
            response = await ac.get("/ranklatest?limit=1", headers={"cid": "testcid"})

        assert response.headers["cid"] == "testcid"
