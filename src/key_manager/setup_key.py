from cryptography.fernet import Fernet

import key_manager
import os

key_setup = key_manager.KeyManager()

print(os.getenv('CIPHER_KEY'))
os.get
#key_setup.setup_local_encryption()
#key_setup.setup_chatgpt_key()
#
#print(os.getenv('CIPHER_KEY'))
#cipher = Fernet(os.getenv('CIPHER_KEY'))
#
#print(os.getenv('CHATGPT_KEY'))
#print("\n" + cipher.decrypt(os.getenv('CHATGPT_KEY')).decode())