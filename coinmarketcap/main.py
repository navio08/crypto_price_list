import logging

import uvicorn
from app import coinmarketApi  # noqa
from config import DEBUG, WEB_HOST, WEB_PORT

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    uvicorn.run("main:coinmarketApi", reload=bool(DEBUG), host=WEB_HOST, port=WEB_PORT)
