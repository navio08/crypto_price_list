from fastapi import FastAPI, Header
from requests import Session, Request, Response
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from typing import Dict, Any, Annotated
import logging
from config import API_KEY, URL_LATEST, URL_HISTORICAL, URL_VERSION, ENDPOINT_TIMEOUT


class AppV1:
    def __init__(self) -> None:
        self.api = FastAPI(debug=True)
        self.api.middleware('http')(self.add_correlationId)
        self.api.api_route("/latest")(self.get_latest)
        self.api.api_route("/historical")(self.get_historical)

        self.parameters: Dict = {}
        self.session = Session()
        self.session.headers.update(
            {
                "Accepts": "application/json",
                "Accept-Encoding": "deflate, gzip",
                "X-CMC_PRO_API_KEY": API_KEY,
            }
        )

    async def add_correlationId(self, request: Request, call_next):
        response = await call_next(request)
        if cid := request.headers.get("cid"):
            response.headers["cid"] = cid
        return response

    def get_latest(self, limit: str, cid: Annotated[str | None, Header()] = "test_cid"):
        return self.get_coinmarketcap(URL_LATEST, cid, {"limit": limit})

    def get_historical(self, limit: int, date: str):
        return self.get_coinmarketcap(URL_HISTORICAL, {"limit": limit, "date": date})

    def get_coinmarketcap(self, url: str, cid: str, additional_query_params: Dict = None):
        try:
            additional_query_params = additional_query_params or {}
            # fmt: off
            response = self.session.get(url, params={**self.parameters, **additional_query_params}, timeout=ENDPOINT_TIMEOUT)
            response.headers.update({"cid": cid})
            return self.clean(response)
            # fmt: on
        except (ConnectionError, Timeout, TooManyRedirects) as error:
            logging.error(error)

    def clean(self, response: Response) -> Dict:
        response_json = json.loads(response.text)
        if "data" not in response_json or response.status_code != 200:
            logging.error(response_json)
            return response_json["status"]["error_message"]

        return {
            item["symbol"]: item["quote"]["USD"]["price"]
            for item in response_json["data"]
        }


class AppV2:
    def __init__(self):
        raise NotImplementedError


# fmt: off
coinmarketApi: Dict[str, Any] = {
    "v1": AppV1,
    "v2": AppV2
}.get(URL_VERSION)().api

coinmarketApp: Dict[str, Any] = {
    "v1": AppV1,
    "v2": AppV2
}.get(URL_VERSION)
# fmt: on
