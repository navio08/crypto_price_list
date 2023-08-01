import json
import logging
from typing import Annotated, Any, Dict

from config import (API_KEY, ENDPOINT_TIMEOUT, URL_RANKHISTORICAL,
                    URL_RANKLATEST, URL_VERSION)
from database import connection, mongo
from fastapi import FastAPI, Header
from requests import Request, Response, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


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

    def get_ranklatest(self, limit: str, cid: Annotated[str | None, Header()] = "cid", timestamp: Annotated[str | None, Header()] = "timestamp"):
        return self.get_crytporank(URL_RANKLATEST, cid, timestamp, {"limit": limit})

    def get_rankhistorical(self, limit: int, time: str):
        return self.get_crytporank(URL_RANKHISTORICAL, {"limit": limit, "time": time})

    def get_crytporank(self, url: str, cid: str = None, timestamp: str = None, additional_query_params: Dict = None):
        try:
            additional_query_params = additional_query_params or {}
            # fmt: off
            response = self.session.get(url, params={**self.parameters, **additional_query_params}, timeout=ENDPOINT_TIMEOUT)
            cleaned_response = self.clean(response)
            logging.info(f"Mongo connection:{connection}")
            logging.info(f"Mongo:{mongo}")
            if isinstance(cleaned_response, dict):
                self.save_in_database(cleaned_response, timestamp)
            return cleaned_response
            # fmt: on
        except (ConnectionError, Timeout, TooManyRedirects) as error:
            logging.error(error)

    def clean(self, response: Response) -> Dict:
        response_json = json.loads(response.text)
        if "data" not in response_json or response.status_code != 200:
            logging.error(response_json)
            return response_json["status"]["message"]

        return {item["symbol"]: item.get("rank", "Unknown") for item in response_json["data"]}

    def save_in_database(self, response: Dict, timestamp: str) -> None:
        for k, v in response.items():
            item = {"ticker": k, "rank": v, "timestamp": timestamp}
            logging.info(f"Inserting:{item}")
            res = mongo.find_one_and_update({"timestamp": timestamp, "ticker": k}, {"$set": item}, upsert=True)
            if not res:
                logging.error(f"Error while inserting data: {item} in cryptorank")


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
