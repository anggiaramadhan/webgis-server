import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="webgis_development",
    user=os.environ["DB_USERNAME"],
)

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS uploaded_files;")
cur.execute(
    "CREATE TABLE uploaded_files (id serial PRIMARY KEY,"
    "filename varchar (50) NOT NULL,"
    "file_url varchar (100) NOT NULL,"
    "created_at date DEFAULT CURRENT_TIMESTAMP);"
)

cur.execute("DROP TABLE IF EXISTS geodata;")
cur.execute(
    "CREATE TABLE geodata (id serial PRIMARY KEY,"
    "name varchar (50) NOT NULL,"
    "data JSONB NOT NULL,"
    "created_at date DEFAULT CURRENT_TIMESTAMP);"
)

conn.commit()

cur.close()
conn.close()
