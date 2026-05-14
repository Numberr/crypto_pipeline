import psycopg2
import os
from pathlib import Path
from dotenv import load_dotenv
from contextlib import contextmanager


load_dotenv()

@contextmanager
def get_conn():
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        yield conn
    finally:
        if conn:
            conn.close()