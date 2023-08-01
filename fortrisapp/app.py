import concurrent.futures
import datetime
import json
import logging
from typing import Dict
from uuid import uuid4

from aggregator import aggregate
from config import ENDPOINT_TIMEOUT, HOST_COINMARKET, HOST_CRYPTORANK
from fastapi import FastAPI
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

URL_COINMARKET = f"http://{HOST_COINMARKET}:8081/latest"
URL_CRYPTORANK = f"http://{HOST_CRYPTORANK}:8082/ranklatest"


class App:
    def __init__(self) -> None:
        self.api = FastAPI(debug=True)
        self.api.api_route("/")(self.get_data)

        self.parameters: Dict = {}
        self.headers: Dict = {
            "Accepts": "application/json",
            "Accept-Encoding": "deflate, gzip",
        }

    def get_data(self, limit: int, format: str = 'json'):
        logging.info(f"Starting request with variables limit:{limit}, format:{format}")
        try:
            return self.fetch_data_multithreaded(limit, format)
        except (ConnectionError, Timeout, TooManyRedirects, AssertionError) as error:
            logging.error(error)
            return str(error)
        except Exception as error:
            logging.error(f"Unknown error. Try again later: {str(error)}")
            return str(error)

    def fetch_data_multithreaded(self, limit: int, format: str = 'json'):
        timestamp: str = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ")
        coinmarketUUID, cryptorankUUID = str(uuid4().hex), str(uuid4().hex)
        _my_futures = {coinmarketUUID: None, cryptorankUUID: None}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_coinmarketcap, limit=limit, cid=coinmarketUUID, timestamp=timestamp),
                executor.submit(self.get_cryptorank, limit=limit, cid=cryptorankUUID, timestamp=timestamp),
            ]
            for future in concurrent.futures.as_completed(futures):
                _my_futures[self.get_uuid(future.result())] = future.result().text

        self.check_valid(_my_futures)
        logging.info(_my_futures)
        result = aggregate(_my_futures, coinmarketUUID, cryptorankUUID, format)

        logging.info(result)
        return result

    def get_coinmarketcap(self, limit: int, cid: str, timestamp: str):
        return self.fetch(URL_COINMARKET, limit, cid, timestamp)

    def get_cryptorank(self, limit: int, cid: str, timestamp: str):
        return self.fetch(URL_CRYPTORANK, limit, cid, timestamp)

    def fetch(self, url: str, limit: int, cid: str, timestamp: str):
        session = Session()
        session.headers.update(self.headers)
        session.headers.update({"cid": cid})
        session.headers.update({"timestamp": timestamp})
        logging.info(f"sending request to:{url}")
        return session.get(url=url, params={"limit": limit}, timeout=ENDPOINT_TIMEOUT)

    def get_uuid(self, future):
        return future.headers["cid"]

    def check_valid(self, result: Dict) -> bool:
        for v in result.values():
            if not isinstance(json.loads(v), dict):
                raise RuntimeError(result[v])


fortrisApi = App().api
fortrisApp = App()
