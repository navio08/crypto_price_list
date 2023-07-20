from fastapi import FastAPI
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime
from typing import Dict, Any

import logging

from config import API_KEY, URL_LATEST, URL_HISTORICAL, URL_VERSION, ENDPOINT_TIMEOUT


class AppV1:
    def __init__(self, limit: int = 5000, datetime: datetime = datetime.datetime.now()) -> None:
        self.api = FastAPI(debug=True)
        self.api.get("/latest")(self.get_latest)

        self.parameters: Dict = {
            'start': '1',
            'limit': limit,
            'convert': 'USD'
        }

        self.session = Session()
        self.session.headers.update({
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': API_KEY,
        })

    def get_latest(self):
        return self.get_coinmarketcap(URL_LATEST)

    def get_coinmarketcap(self, url: str):
        try:
            response = self.session.get(url, params=self.parameters, timeout=ENDPOINT_TIMEOUT)
            return json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as error:
            logging.error(error)


class AppV2:
    def __init__(self):
        raise NotImplementedError


coinmarketApp: Dict[str, Any] = {
    "v1": AppV1,
    "v2": AppV2
}.get(URL_VERSION)().api
