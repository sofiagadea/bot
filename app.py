import requests
from flask import Flask, request,jsonify
import json


TOKEN = '5607369368:AAHEBTuVYxEGuyyBp2gZeP5vqOcMyhkkt4M'
LINK = 'https://api.telegram.org/bot5607369368:AAHEBTuVYxEGuyyBp2gZeP5vqOcMyhkkt4M/setWebhook?url=https://com-bot'
app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        data = request.get_json()
        print(f'DATA: {data}')
        return {'statusCode': 200, 'body': 'Success', 'data': data}
    else:
        return {'statusCode': 200, 'body': 'Success'}

if __name__ == '__main__':
    app.run(debug=True)