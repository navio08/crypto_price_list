import os

import uvicorn
import logging

from app import coinmarketApp  # noqa
from config import WEB_HOST, WEB_PORT, DEBUG

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    for k, v in os.environ.items():
        logging.info(f'{k}={v}')
    uvicorn.run("main:coinmarketApp", reload=bool(DEBUG), host=WEB_HOST, port=WEB_PORT)
