from fastapi import FastAPI
from requests import Session, Request
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from typing import Dict, Any

import logging

from config import API_KEY, URL_RANKLATEST, URL_RANKHISTORICAL, URL_VERSION, ENDPOINT_TIMEOUT
from otelconfig import tracer


class AppV1:
    def __init__(self) -> None:
        self.api = FastAPI(debug=True)
        self.api.middleware('http')(self.add_correlationId)
        self.api.api_route("/ranklatest")(self.get_ranklatest)
        self.api.api_route("/rankhistorical")(self.get_rankhistorical)

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

    async def add_correlationId(self, request: Request, call_next):
        response = await call_next(request)
        if cid := request.headers.get("cid"):
            response.headers["cid"] = cid
        return response

    def get_ranklatest(self, limit: str):
        with tracer.start_as_current_span("CRYPTORANK::start_request"):
            return self.get_crytporank(URL_RANKLATEST, {"limit": limit})

    def get_rankhistorical(self, limit: int, time: str):
        return self.get_crytporank(URL_RANKHISTORICAL, {"limit": limit, "time": time})

    def get_crytporank(self, url: str, additional_query_params: Dict = None):
        try:
            additional_query_params = additional_query_params or {}
            # fmt: off
            with tracer.start_as_current_span("CRYPTORANK::request_api"):
                response = self.session.get(url, params={**self.parameters, **additional_query_params}, timeout=ENDPOINT_TIMEOUT)
                return self.clean(response.text)
            # fmt: on
        except (ConnectionError, Timeout, TooManyRedirects) as error:
            logging.error(error)

    def clean(self, response: str) -> Dict:
        with tracer.start_as_current_span("CRYPTORANK::cleaning_data"):
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
