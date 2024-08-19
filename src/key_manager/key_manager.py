import os

from cryptography.fernet import Fernet
import logging

from config.config_util import ConfigUtil


class KeyManager:

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    def __init__(self):
        if not (os.getenv('CIPHER_KEY') == 'None'):
            KeyManager.log.info("CIPHER_KEY exists")
            return
        else:
            KeyManager.log.info("CIPHER_KEY does not exist, creating new key")

    def setup_local_encryption(self):
        key = Fernet.generate_key()
        os.environ['CIPHER_KEY'] = key.decode()

    def setup_chatgpt_key(self):
        try:
            if not (ConfigUtil.get_current_configs("chatgpt")['chat_gpt_key'] == ''):
                KeyManager.log.info("chat_gpt_key exists")
            return
        except TypeError:
            print("No ChatGPT Key present, creating local key")

        cipher = Fernet(os.getenv('CIPHER_KEY'))

        #promt for chat_gpt_key
        chat_gpt_key_encrypted = cipher.encrypt(input("Enter your ChatGPT key:").encode())
        ConfigUtil.add_config_value('chat_gpt_key', chat_gpt_key_encrypted, "chatgpt")

    def get_chat_gpt_key(self):
        KeyManager.setup_chatgpt_key()
        return








