import os

from dotenv import load_dotenv

load_dotenv()

ENDPOINT_TIMEOUT = int(os.getenv("ENDPOINT_TIMEOUT"))

WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("WEB_PORT", 8080))
DEBUG = os.getenv("DEBUG", "1")

MY_SERVICE_NAME = "fortrisApp"
