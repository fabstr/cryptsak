from flask import Flask, request
from Crypter import Crypter
import Config

app = Flask(__name__)

@app.route('/hello')
def hello():
	return "Hello!"

@app.route('/encrypt', methods=['POST'])
def encrypt():
	data = request.json.get('plaintext')
	crypter = Crypter(Config.MASTER_SECRET)
	return crypter.encrypt(data)

@app.route('/decrypt', methods=['POST'])
def decrypt():
	crypter = Crypter(Config.MASTER_SECRET)
	return crypter.decrypt({
		'ciphertext': request.json.get('ciphertext'),
		'salt': request.json.get('salt'),
		'iv': request.json.get('iv'),
	})

app.run(host=Config.HOST, port=Config.PORT)
