import psycopg2
from google.cloud import secretmanager
from psycopg2 import OperationalError

class PostgresConnector:

    def create_connection(self, db_name):
        try:
            self.connection = psycopg2.connect(
                    host="34.136.28.192",
                    database="premier_league_stats",
                    user="bdon_db",
                    password=PostgresConnector.get_db_pass(),
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
        self.connection.close()

    def execute_insert_query(self, query):
        try:
            self.cursor.execute(query)
        except OperationalError as e:
            self.connection.rollback()
            print(f"The error '{e}' occurred")
            return
        self.connection.commit()

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

    def execute_many_parameterized_insert_query(self, query, data_array):
        try:
            self.cursor.executemany(query, data_array)
        except OperationalError as e:
            self.connection.rollback()
            print(f"The error '{e}' occurred")
            return
        self.connection.commit()

    def insert_into_keys_table(self, key_name, key_value):
        self.execute_parameterized_insert_query("keys",
            "INSERT INTO keys(key_name, key_value) VALUES (%s, %s)", (key_name, key_value)
        )
    @staticmethod
    def get_db_pass():
        client = secretmanager.SecretManagerServiceClient()
        secret_name = "projects/kinetic-genre-433414-h4/secrets/db_pass2/versions/latest"
        # Access the secret version
        response = client.access_secret_version(name=secret_name)

        # Decode the secret value
        secret_value = response.payload.data.decode("UTF-8")

        return secret_value


print(PostgresConnector.get_db_pass())