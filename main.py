from flask import Flask, request
from Crypter import Crypter
import Config

app = Flask(__name__)

# Encrypt
# POST /encrypt with raw data with content type multipart/form-data
#
# Example string:
#     this is a string to be encrypted

# Which might return (for some particular master secret and state of the 
# operating system secure pseudo random generator):
#     +AZe95Ortdj93jv93toyJ+phI7m992MyYrg6d7JGG28=;BOJc/IzGS5giv8OvvYihSAMvcq/GvuJPfxL60gNgDK0=;X3A2FCd29YQ/lctBy/OGZA==
@app.route('/encrypt', methods=['POST'])
def encrypt():
	# get the raw post data
	request.get_data()
	data = request.data

	# create the crypter object
	crypter = Crypter(Config.MASTER_SECRET)

	# encrypt and return a string holding the ciphertext, iv and salt 
	return crypter.encrypt(data)

# Decrypt
# POST /decrypt with raw data with content type multipart/form-data
#
# Example string: 
#     +AZe95Ortdj93jv93toyJ+phI7m992MyYrg6d7JGG28=;BOJc/IzGS5giv8OvvYihSAMvcq/GvuJPfxL60gNgDK0=;X3A2FCd29YQ/lctBy/OGZA==
# 
# Which (using the same master secret as above) will return:
#     this is a string to be encrypted
@app.route('/decrypt', methods=['POST'])
def decrypt():
	# get the raw post data (it will be parsed in decrypt below)
	request.get_data()
	data = request.data

	# create the crypter object
	crypter = Crypter(Config.MASTER_SECRET)

	# decrypt and return the plaintext
	return crypter.decrypt(data)

# run the app
app.run(host=Config.HOST, port=Config.PORT)
