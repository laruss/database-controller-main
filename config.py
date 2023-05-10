import os

from dotenv import load_dotenv
load_dotenv()


Config = {
    "db": os.getenv("DB"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "alias": os.getenv("DB_ALIAS")
}
