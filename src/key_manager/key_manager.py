import os

from cryptography.fernet import Fernet
import logging

from src.database_connector.postgres_connector import PostgresConnector


class KeyManager:

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    def setup_local_encryption(self):
        key = Fernet.generate_key()
        os.environ['CIPHER_KEY'] = key.decode()

    def setup_chatgpt_key(self):
        try:
            db_connector = PostgresConnector()
            os.environ['CHATGPT_KEY'] = db_connector.execute_parameterized_select_query("select key_value from keys where key_name = \'chatgpt_key\'", ())[0][0]
        except:
            raise Exception("Could not fetch ChatGPT key")

    def get_chat_gpt_key(self):
        if(os.environ.get('CHATGPT_KEY', None) == None):
            self.setup_chatgpt_key()
        return os.environ['CHATGPT_KEY']

    def setup_cipher_key(self):
        key = Fernet.generate_key()
        os.environ['CIPHER_KEY'] = key.decode()
        try:
            db_connector = PostgresConnector()
            db_connector.insert_into_keys_table( "cipher_key", os.environ['CIPHER_KEY'])
        except Exception as e:
            raise Exception("Error creating CIPHER_KEY:" + str(e))

    def get_cipher_key(self):
        db_connector = PostgresConnector()
        os.environ['CIPHER_KEY'] = db_connector.execute_parameterized_select_query("select key_value from keys where key_name = \'cipher_key\'", ())[0][0]
        if(os.environ.get('CIPHER_KEY', None) == None):
            self.setup_cipher_key()
        return os.environ['CIPHER_KEY']

    def get_all_keys(self):
        db_connector = PostgresConnector()
        print(db_connector.execute_parameterized_select_query("select * from keys", ()))






