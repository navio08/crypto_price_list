from fastapi import FastAPI
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from typing import Dict

import logging
import concurrent.futures
from uuid import uuid4

from otelconfig import tracer

URL_COINMARKET = "http://localhost:8081/latest"
URL_CRYPTORANK = "http://localhost:8082/ranklatest"


class App:
    def __init__(self) -> None:
        self.api = FastAPI(debug=True)
        self.api.api_route("/")(self.get_data)

        self.parameters: Dict = {}
        self.headers: Dict = {
            "Accepts": "application/json",
            "Accept-Encoding": "deflate, gzip",
        }

    def get_data(self, limit: int):
        try:
            with tracer.start_as_current_span("FORTRIS::start_request"):
                return self.fetch_data_multithreaded(limit)
        except (ConnectionError, Timeout, TooManyRedirects) as error:
            logging.error(error)
        except Exception as error:
            logging.error(f"Unknown error. Try again later: {str(error)}")

    def fetch_data_multithreaded(self, limit):

        coinmarketUUID, cryptorankUUID = str(uuid4().hex), str(uuid4().hex)
        _my_futures = {coinmarketUUID: None, cryptorankUUID: None}
        with tracer.start_as_current_span("FORTRIS::sending multiple requests"):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(self.get_coinmarketcap, limit=limit, cid=coinmarketUUID),
                    executor.submit(self.get_cryptorank, limit=limit, cid=cryptorankUUID)
                ]
                for future in concurrent.futures.as_completed(futures):
                    with tracer.start_as_current_span("FORTRIS::processing_results"):
                        _my_futures[self.get_uuid(future.result())] = future.result().text

        print(_my_futures)
        return _my_futures

    def get_coinmarketcap(self, limit: int, cid: str):
        with tracer.start_as_current_span("FORTRIS::processing request to coinmarketFetcher"):
            return self.fetch(URL_COINMARKET, limit, cid)

    def get_cryptorank(self, limit: int, cid: str):
        with tracer.start_as_current_span("FORTRIS::processing request to cryptomarketFetcher"):
            return self.fetch(URL_CRYPTORANK, limit, cid)

    def fetch(self, url: str, limit: int, cid: str):
        session = Session()
        session.headers.update(self.headers)
        session.headers.update({"cid": cid})
        return session.get(url=url, params={"limit": limit})

    def get_uuid(self, future):
        return future.headers["cid"]


fortrisApi = App().api
fortrisApp = App()
