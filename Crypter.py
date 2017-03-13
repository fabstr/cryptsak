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

	def __to_json(self, cryptdata):
		base64_encoded_cryptdata = {}
		for key, value in cryptdata.items():
			base64_encoded_cryptdata[key] = b64encode(value).decode('latin1')

		return dumps(base64_encoded_cryptdata)

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

		return self.__to_json(cryptdata) 

	def decrypt(self, base64_encoded_cryptdata):
		cryptdata = {}
		for key, value in base64_encoded_cryptdata.items():
			cryptdata[key] = b64decode(value)

		encryption_key = self.__get_encryption_key(cryptdata.get('salt'))
		iv = cryptdata.get('iv')

		cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
		plaintext = cipher.decrypt(cryptdata.get('ciphertext'))
		return plaintext
