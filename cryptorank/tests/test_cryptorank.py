import os
import sys

import pytest
from data.responses import response200
from httpx import AsyncClient

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from app import cryptorankApi, cryptorankApp  # noqa: E402


class ResponseMockOK:
    text = response200
    status_code = 200


class TestRank:
    @pytest.mark.anyio
    async def test_missing_limit_mandatory_parameter(self):
        async with AsyncClient(app=cryptorankApi, base_url="http://test") as ac:
            response = await ac.get("/ranklatest")

        assert response.status_code == 422


class TestCleaningResponses:
    def test_clean_good_data(self):
        app = cryptorankApp()
        clean_data = app.clean(ResponseMockOK)
        assert clean_data == {"BTC": 1, "ETH": 2, "USDT": 3, "XRP": 4, "BNB": 5}
