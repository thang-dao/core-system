import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="env/.env")


MYSQL_URL = os.getenv("MYSQL_URL")
POOL_SIZE = int(os.getenv("POOL_SIZE", "20"))
POOL_RECYCLE = int(os.getenv("POOL_RECYCLE", "3600"))
POOL_TIMEOUT = int(os.getenv("POLL_TIMEOUT", "2"))
MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", 2))
CONNECT_TIMEOUT = int(os.getenv("CONNECT_TIMEOUT", 60))