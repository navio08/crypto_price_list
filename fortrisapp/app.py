from fastapi import FastAPI
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from typing import Dict

import logging
import concurrent.futures
from uuid import uuid4

from otelconfig import tracer
from config import HOST_COINMARKET, HOST_CRYPTORANK, ENDPOINT_TIMEOUT
from aggregator import aggregate

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
        print(f"Starting request with variables limit:{limit}, format:{format}")
        try:
            with tracer.start_as_current_span("FORTRIS::start_request"):
                return self.fetch_data_multithreaded(limit, format)
        except (ConnectionError, Timeout, TooManyRedirects) as error:
            logging.error(error)
            return str(error)
        except Exception as error:
            logging.error(f"Unknown error. Try again later: {str(error)}")

    def fetch_data_multithreaded(self, limit: int, format: str = 'json'):
        coinmarketUUID, cryptorankUUID = str(uuid4().hex), str(uuid4().hex)
        _my_futures = {coinmarketUUID: None, cryptorankUUID: None}
        with tracer.start_as_current_span("FORTRIS::sending multiple requests"):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(self.get_coinmarketcap, limit=limit, cid=coinmarketUUID),
                    executor.submit(self.get_cryptorank, limit=limit, cid=cryptorankUUID),
                ]
                for future in concurrent.futures.as_completed(futures):
                    with tracer.start_as_current_span("FORTRIS::processing_results"):
                        _my_futures[self.get_uuid(future.result())] = future.result().text

        print(_my_futures)
        with tracer.start_as_current_span("FORTRIS::aggregating data"):
            result = aggregate(_my_futures, coinmarketUUID, cryptorankUUID, format)

        print(result)
        return result

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
        print(f"sending request to:{url}")
        return session.get(url=url, params={"limit": limit}, timeout=ENDPOINT_TIMEOUT)

    def get_uuid(self, future):
        return future.headers["cid"]


fortrisApi = App().api
fortrisApp = App()
