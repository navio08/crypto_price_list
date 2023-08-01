import os

from dotenv import load_dotenv

load_dotenv()

URL_LATEST = "/".join([os.getenv(path) for path in ["URL", "VERSION", "ENDPOINT_LATEST"]])
URL_HISTORICAL = "/".join([os.getenv(path) for path in ["URL", "VERSION", "ENDPOINT_HISTORICAL"]])
URL_VERSION = os.getenv("VERSION")
API_KEY = os.getenv('API_KEY')
ENDPOINT_TIMEOUT = int(os.getenv("ENDPOINT_TIMEOUT"))

WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("WEB_PORT", 8081))
DEBUG = os.getenv("DEBUG", "1")

MY_SERVICE_NAME = "coinmarketcapFetcher"
HOST_MONGO = os.getenv("HOST_MONGO", "0.0.0.0")
