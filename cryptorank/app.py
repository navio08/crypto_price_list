from fastapi import FastAPI
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from typing import Dict, Any

import logging

from config import API_KEY, URL_RANKLATEST, URL_RANKHISTORICAL, URL_VERSION, ENDPOINT_TIMEOUT


class AppV1:
    def __init__(self) -> None:
        self.api = FastAPI(debug=True)
        self.api.api_route("/ranklatest")(self.get_ranklatest)

        self.parameters: Dict = {
            "convert": "USD",
            "api_key": API_KEY,
        }

        self.session = Session()
        self.session.headers.update(
            {
                "Accepts": "application/json",
                "Accept-Encoding": "deflate, gzip",
            }
        )

    def get_ranklatest(self, limit: str):
        return self.get_crytporank(URL_RANKLATEST, {"limit": limit})

    def get_crytporank(self, url: str, additional_query_params: Dict = None):
        try:
            additional_query_params = additional_query_params or {}
            # fmt: off
            response = self.session.get(url, params={**self.parameters, **additional_query_params}, timeout=ENDPOINT_TIMEOUT)
            return self.clean(response.text)
            # fmt: on
        except (ConnectionError, Timeout, TooManyRedirects) as error:
            logging.error(error)

    def clean(self, response: str) -> Dict:
        response_json = json.loads(response)
        if "data" not in response_json:
            return response_json

        return {item["symbol"]: item["rank"] for item in response_json["data"]}


class AppV2:
    def __init__(self):
        raise NotImplementedError


# fmt: off
cryptorankApi: Dict[str, Any] = {
    "v1": AppV1,
    "v2": AppV2
}.get(URL_VERSION)().api

cryptorankApp: Dict[str, Any] = {
    "v1": AppV1,
    "v2": AppV2
}.get(URL_VERSION)
# fmt: on
