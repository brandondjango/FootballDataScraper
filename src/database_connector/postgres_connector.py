import psycopg2
from psycopg2 import OperationalError


def create_connection():
    try:
        conn = psycopg2.connect(
                host="localhost",
                database="keys",
                user="pyai",
                password="Brandon123",
                port=5432  # default port for PostgreSQL
            )
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()  # Fetch all rows from the last executed statement
        for row in result:
            print(row)
        cursor.close()
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

con = create_connection()
query = 'SELECT * from keys;'

execute_query(con, query)