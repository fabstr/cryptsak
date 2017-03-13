from hashlib import pbkdf2_hmac, sha256
from os import urandom
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from json import dumps

class Crypter:
	def __init__(self, master_secret):
		self.__master_secret = master_secret

	def __get_salt(self):
		return urandom(32)

	def __get_iv(self):
		return urandom(16)

	def __get_encryption_key(self, salt):
		encryption_key = pbkdf2_hmac('sha256', bytearray(self.__master_secret, 'latin1'), salt, 10000)
		return encryption_key

	def __to_text(self, cryptdata):
		text = ""
		text += b64encode(cryptdata.get('ciphertext')).decode('latin1')
		text += ";"
		text += b64encode(cryptdata.get('salt')).decode('latin1')
		text += ";"
		text += b64encode(cryptdata.get('iv')).decode('latin1')

		return text

	def encrypt(self, data):
		salt = self.__get_salt()
		iv = self.__get_iv()
		encryption_key = self.__get_encryption_key(salt)

		cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
		ciphertext = cipher.encrypt(data)

		cryptdata = {
			'iv':iv,
			'salt':salt,
			'ciphertext':ciphertext
		}

		return self.__to_text(cryptdata) 

	def decrypt(self, text):
		fields = text.decode('latin1').split(';');

		ciphertext = b64decode(fields[0])
		salt = b64decode(fields[1])
		iv = b64decode(fields[2])

		encryption_key = self.__get_encryption_key(salt)

		cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
		plaintext = cipher.decrypt(ciphertext)
		return plaintext
