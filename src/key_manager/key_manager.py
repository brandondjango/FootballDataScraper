import os

from cryptography.fernet import Fernet
import logging

from src.config_util.config_util import ConfigUtil


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

    def setup_chatgpt_key(self, local=True):
        try:
            if local:
                if('CHATGPT_KEY' in os.environ()):
                    KeyManager.log.info("Local CHATGPT_KEY exists")
                    return
            else:
                if not (ConfigUtil.get_current_configs("chatgpt")['chat_gpt_key'] == ''):
                    KeyManager.log.info("Config chat_gpt_key exists")
                    return
        except TypeError:
            print("No ChatGPT Key present, creating local key")

        cipher = Fernet(os.getenv('CIPHER_KEY'))

        #promt for chat_gpt_key
        chat_gpt_key_encrypted = cipher.encrypt(input("Enter your ChatGPT key:").encode())
        if local:
            os.environ['CHATGPT_KEY'] = chat_gpt_key_encrypted.decode()
            KeyManager.log.info("Local CHATGPT_KEY saved")
        else:
             ConfigUtil.add_config_value('chat_gpt_key', chat_gpt_key_encrypted, "chatgpt")

    def get_chat_gpt_key(self):
        KeyManager.setup_chatgpt_key()
        return








