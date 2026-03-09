import mysql.connector
import os

def get_conn():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST","mysql"),
        user=os.getenv("DB_USER","root"),                    
        password=os.getenv("DB_PASSWORD","root@123"),  
        database=os.getenv("DB_NAME","incident_db"),
        port=3306   
    )
    return conn