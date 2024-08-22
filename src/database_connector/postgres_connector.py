import psycopg2
from psycopg2 import OperationalError

class PostgresConnector:

    def create_connection(self, db_name):
        try:
            self.connection = psycopg2.connect(
                    host="localhost",
                    database=db_name,
                    user="pyai",
                    password="Brandon123",
                    port=5432  # default port for PostgreSQL
                )
        except OperationalError as e:
            print(f"The error '{e}' occurred")
            return None

    def open_connection_cursor(self, db_name):
        self.create_connection(db_name)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()

    def execute_parameterized_select_query(self, db_name, query, params):
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()  # Fetch all rows from the last executed statement
            self.cursor.close()
            return result
        except OperationalError as e:
            self.cursor.close()
            print(f"The error '{e}' occurred")
            return None

    def execute_parameterized_insert_query(self, query, params):
        try:
            self.cursor.execute(query, params)
        except OperationalError as e:
            self.connection.rollback()
            print(f"The error '{e}' occurred")
            return
        self.connection.commit()


    def insert_into_keys_table(self, key_name, key_value):
        self.execute_parameterized_insert_query("keys",
            "INSERT INTO keys(key_name, key_value) VALUES (%s, %s)", (key_name, key_value)
        )