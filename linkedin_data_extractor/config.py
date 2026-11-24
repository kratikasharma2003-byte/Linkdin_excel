
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.getenv(
    "INPUT_FILE",
    os.path.join(BASE_DIR, "data", "input.xlsx")
)

OUTPUT_FILE = os.getenv(
    "OUTPUT_FILE",
    os.path.join(BASE_DIR, "data", "output.json")
)

ERROR_FILE = os.getenv(
    "ERROR_FILE",
    os.path.join(BASE_DIR, "data", "errors.json")
)

API_URL = os.getenv("PROFILE_API_URL", "")
API_KEY = os.getenv("PROFILE_API_KEY", "")

URL_COLUMN = os.getenv("URL_COLUMN", "")

LIMIT = int(os.getenv("LIMIT", "0"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "500"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "1"))
