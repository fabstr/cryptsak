from hashlib import pbkdf2_hmac, sha256
from os import urandom
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from json import dumps

class Crypter:
	# Constructor, take the master secret as the only argument
	def __init__(self, master_secret):
		# set the master secret
		self.__master_secret = master_secret

	# Generate a salt of 256 bits
	def __get_salt(self):
		# generate 32 random bytes
		return urandom(32)

	# Generate an AES initializtion vector of 128 bits
	def __get_iv(self):
		return urandom(16)

	# Get an instance of the AES cipher.
	# Compute the encryption key from the salt before createing the 
	# instance.
	def __get_cipher(self, salt, iv):
		# compute the encryption key
		encryption_key = self.__get_encryption_key(salt)

		# create the aes cipher object and return it
		cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
		return cipher

	# Use PBKDF2 to derive an encryption key from the master secret and salt.
	# 10000 iterations are used and the hash function is Sha256.
	def __get_encryption_key(self, salt):
		encryption_key = pbkdf2_hmac('sha256', bytearray(self.__master_secret, 'latin1'), salt, 10000)
		return encryption_key

	# Create the string which is to be sent to the client.
	# The string contains the ciphertext, salt and iv (in that order) 
	# encoded with base64 and delimited by a semicolon.
	def __to_text(self, ciphertext, salt, iv):
		text = ""
		text += b64encode(ciphertext).decode('latin1')
		text += ";"
		text += b64encode(salt).decode('latin1')
		text += ";"
		text += b64encode(iv).decode('latin1')
		return text

	# Encrypt the data:
	# Randomly generate a salt and an iv, compute the encryption key and 
	# encrypt data. Fetch the text representation of the ciphertext (with iv 
	# and salt).
	# 
	# Cipher feedback mode is used with AES256.
	def encrypt(self, data):
		# get the salt and iv
		salt = self.__get_salt()
		iv   = self.__get_iv()

		# get the cipher object and perform the encryption
		cipher     = self.__get_cipher(salt, iv)
		ciphertext = cipher.encrypt(data)

		# create the text representation and return it
		return self.__to_text(ciphertext, salt, iv)

	# Parse the text and decode the base64.
	# Text is a string of 3 base64 encoded strings, delimited by a 
	# semicolon in the order ciphertext, salt, iv.
	def __parse_text(self, text):
		fields = text.decode('latin1').split(';');

		ciphertext = b64decode(fields[0])
		salt       = b64decode(fields[1])
		iv         = b64decode(fields[2])

		return (ciphertext, salt, iv)

	# Decrypt the data.
	# Parse the text and extract ciphertext, salt and iv, then decrypt and
	# return the plaintext.
	def decrypt(self, text):
		(ciphertext, salt, iv) = self.__parse_text(text)

		# get the cipher object and perform the decryption
		cipher    = self.__get_cipher(salt, iv)
		plaintext = cipher.decrypt(ciphertext)

		# return the plaintext
		return plaintext
