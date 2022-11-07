import requests
from flask import Flask, request,jsonify
import json


TOKEN = '5607369368:AAHEBTuVYxEGuyyBp2gZeP5vqOcMyhkkt4M'

app = Flask(__name__)

'''{'message_id': 14, 
'from': {'id': 5667263033, 'is_bot': False, 'first_name': 'Sofia', 'last_name': 'Gadea', 'username': 'sofigadea', 'language_code': 'es'}, 
 'chat': {'id': 5667263033, 'first_name': 'Sofia', 'last_name': 'Gadea', 'username': 'sofigadea', 
 'type': 'private'}, 
 'date': 1667819834, 'text': 'hi'}'''


def welcome_message(item):
    print(item)

    if item['text'].lower() == 'hi':
        msg = 'hello '
        chat_id = item['chat']['id']
        user_id = item['from']['id']
        username = item['from']['username']
        welcome_msg = f'{msg}{username}'
        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={welcome_msg}&parse_mode=HTML'
        resp = requests.get(to_url)


@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        data = request.get_json()
        print(f'DATA: {data}')
        if 'message' in data:
            data = data['message']
            welcome_message(data)
            return {'statusCode': 200, 'body': 'Success', 'data': data}
        else:
            return {'statusCode': 404, 'body': 'User has left the chat room and deleted the chat', 'data': data}
    else:
        return {'statusCode': 200, 'body': 'Success'}

if __name__ == '__main__':
    app.run(debug=True)