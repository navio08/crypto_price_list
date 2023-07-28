from fastapi import FastAPI, Header
from requests import Session, Request, Response
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from typing import Dict, Any, Annotated
import logging
from config import API_KEY, URL_LATEST, URL_HISTORICAL, URL_VERSION, ENDPOINT_TIMEOUT
from database import mongo


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
        cid = request.headers.get("cid")
        # timestap = request.headers.get("timestamp")
        response = await call_next(request)
        if cid:
            response.headers["cid"] = cid
        return response

    def get_latest(self, limit: str, cid: Annotated[str | None, Header()] = "cid", timestamp: Annotated[str | None, Header()] = "timestamp"):
        return self.get_coinmarketcap(URL_LATEST, cid, timestamp, {"limit": limit})

    def get_historical(self, limit: int, date: str):
        return self.get_coinmarketcap(URL_HISTORICAL, {"limit": limit, "date": date})

    def get_coinmarketcap(self, url: str, cid: str = None, timestamp: str = None, additional_query_params: Dict = None):
        try:
            additional_query_params = additional_query_params or {}
            # fmt: off
            response = self.session.get(url, params={**self.parameters, **additional_query_params}, timeout=ENDPOINT_TIMEOUT)
            response.headers.update({"cid": cid})
            cleaned_response = self.clean(response)
            self.save_in_database(cleaned_response, timestamp)
            return cleaned_response
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

    def save_in_database(self, response: Dict, timestamp: str) -> None:
        for k, v in response.items():
            item = {"ticker": k, "price": v, "timestamp": timestamp}
            res = mongo.find_one_and_update({"timestamp": timestamp}, {"$set": item}, upsert=True)
            if not res:
                logging.error(f"Error while inserting data: {res} in coinmarketcap")


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
