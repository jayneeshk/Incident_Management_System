import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("db_password"),
        database=os.getenv("db_name")
    )
    if conn.is_connected():
        print("Connected to MySQL successfully")
        return conn

