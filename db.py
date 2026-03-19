import time
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_conn(retries=5, delay=3):
    for i in range(retries):
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST","mysql"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                port=3306
            )
            return conn
        except Exception as e:
            print(f"DB not ready, retry {i+1}/{retries}: {e}")
            time.sleep(delay)
    raise Exception("Cannot connect to DB after retries")