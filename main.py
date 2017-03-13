from flask import Flask, request
from Crypter import Crypter
import Config

app = Flask(__name__)

@app.route('/hello')
def hello():
	return "Hello!"

@app.route('/encrypt', methods=['POST'])
def encrypt():
	request.get_data()
	data = request.data
	crypter = Crypter(Config.MASTER_SECRET)
	return crypter.encrypt(data)

@app.route('/decrypt', methods=['POST'])
def decrypt():
	request.get_data()
	crypter = Crypter(Config.MASTER_SECRET)
	return crypter.decrypt(request.data)

app.run(host=Config.HOST, port=Config.PORT)
