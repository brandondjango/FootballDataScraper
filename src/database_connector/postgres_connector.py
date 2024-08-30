import psycopg2
from google.cloud import secretmanager
from psycopg2 import OperationalError

import os
import ssl

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy

Base = sqlalchemy.orm.declarative_base()

class Player(Base):
    __tablename__ = 'players'

    player_id = Column(String, primary_key=True)
    player_name = Column(String)

    def __repr__(self):
        return f"<Player(player_id={self.player_id}, player_name={self.player_name})>"




class PostgresConnector:

    @staticmethod
    def create_connection_with_sqlalhemy() -> sqlalchemy.engine.base.Engine:
        #engine = sqlalchemy.create_engine(
        #    # Equivalent URL:
        #    # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        #    sqlalchemy.engine.url.URL.create(
        #        drivername="postgresql+pg8000",
        #        username="bdon_db",
        #        password=PostgresConnector.get_db_pass(),
        #        host="34.136.28.192",
        #        port=5432,
        #        database="premier_league_stats",
        #    ),
        #    # ...
        #)
        DATABASE_URL = "postgresql://bdon_db:" + PostgresConnector.get_db_pass() + "@34.136.28.192:5432/premier_league_stats"
        engine = create_engine(DATABASE_URL)
        return engine

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


#postgres_conn = PostgresConnector()
#postgres_conn.create_connection("asd")
# Example usage: Query all players
#Session = sessionmaker(bind=PostgresConnector.create_connection_with_sqlalhemy())
#session = Session()
#
#
#
#players = session.query(Player).all()
#
## Print the results
#for player in players:
#    print(player)