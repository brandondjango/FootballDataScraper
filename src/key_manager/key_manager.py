import os

import yaml
from cryptography.fernet import Fernet
import logging



class KeyManager:

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    config_yaml_path = 'config/config.yaml'

    def __init__(self):
        if not (os.getenv('CIPHER_KEY') == 'None'):
            KeyManager.log.info("CIPHER_KEY exists")
            return
        else:
            KeyManager.log.info("CIPHER_KEY does not exist, creating new key")


    def setup_local_encryption(self):
        key = Fernet.generate_key()
        os.environ['CIPHER_KEY'] = key.decode()

    def get_current_configs(self):
        config_yaml_path = KeyManager.config_yaml_path
        with open(config_yaml_path, 'r') as file:
            config = config_yaml_path.safe_load(file)
        return config


    def add_config_value(self, key, value):
        configs_to_change = KeyManager.get_current_configs()
        configs_to_change[key] = value
        with open(KeyManager.get_current_configs(), 'w') as file:
            yaml.dump(configs_to_change, file, default_flow_style=False)

    def setup_chatgpt_key(self):
        if not (KeyManager.get_current_configs['chat_gpt_key'] == ''):
            KeyManager.log.info("chat_gpt_key exists")
            return

        cipher = Fernet(os.getenv('CIPHER_KEY'))

        #promt for chat_gpt_key
        chat_gpt_key_encrypted = cipher.encrypt(input("Enter your ChatGPT key:"))
        KeyManager.add_config_value('chat_gpt_key', chat_gpt_key_encrypted)

    def get_chat_gpt_key(self):
        KeyManager.setup_chatgpt_key()
        return








