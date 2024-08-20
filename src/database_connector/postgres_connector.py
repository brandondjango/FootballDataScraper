import psycopg2
from psycopg2 import OperationalError

class PostgresConnector:

    def create_connection(self):
        try:
            self.connection = psycopg2.connect(
                    host="localhost",
                    database="keys",
                    user="pyai",
                    password="Brandon123",
                    port=5432  # default port for PostgreSQL
                )
        except OperationalError as e:
            print(f"The error '{e}' occurred")
            return None

    def execute_parameterized_select_query(self, query, params):
        self.create_connection()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()  # Fetch all rows from the last executed statement
            cursor.close()
            return result
        except OperationalError as e:
            cursor.close()
            print(f"The error '{e}' occurred")
            return None

    def execute_parameterized_insert_query(self, query, params):
        self.create_connection()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
        except OperationalError as e:
            cursor.close()
            print(f"The error '{e}' occurred")
            return None



    def insert_into_keys_table(self, key_name, key_value):
        self.execute_parameterized_insert_query(
            "INSERT INTO keys(key_name, key_value) VALUES (%s, %s)", (key_name, key_value)
        )