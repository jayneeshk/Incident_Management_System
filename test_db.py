from db import get_conn

conn=get_conn()
print(" Good")
conn.close()