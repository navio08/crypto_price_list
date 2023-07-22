import uvicorn
import logging
from app import cryptorankApi  # noqa
from config import WEB_HOST, WEB_PORT, DEBUG

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    uvicorn.run("main:cryptorankApi", reload=bool(DEBUG), host=WEB_HOST, port=WEB_PORT)
