import requests
from flask import Flask, request,jsonify
import json

globvar = 0
TOKEN = '5529622158:AAHYUHjS8xoigtNWrXLGLxzTc5M6TSzGA18'
globallist = []

"""https://api.telegram.org/bot5529622158:AAHYUHjS8xoigtNWrXLGLxzTc5M6TSzGA18/setWebhook?url=https://bot-wcsg.herokuapp.com/"""

app = Flask(__name__)
'''{'message_id': 14, 
'from': {'id': 5667263033, 'is_bot': False, 'first_name': 'Sofia', 'last_name': 'Gadea', 'username': 'sofigadea', 'language_code': 'es'}, 
 'chat': {'id': 5667263033, 'first_name': 'Sofia', 'last_name': 'Gadea', 'username': 'sofigadea', 
 'type': 'private'}, 
 'date': 1667819834, 'text': 'hi'}'''

"""
class ListUsers():
    def __init__(self):
        self.users = []

    def add_player(self,Player):
        self.users.append(Player)

    def print_players(self):
        s = ""
        for i in self.users:
            s+= i.username
        return s
    """

class Player():
    def __init__(self,id,username,points,tries_left):
        self.id = id
        self.username = username
        self.points = points
        self.tries_left = tries_left

class Number():
    def __init__(self,status, number, maximum,minimum,winner,tries):
        self.status = 0
        self.number = 10
        self.maximum = maximum
        self.minomum = minimum
        self.winner = winner
        self.tries = tries



"""def set_global_to_one():
    global globvar 
    globvar = 1"""

def add_player(objeto):
    global globallist
    globallist.append(objeto)

def check_if_user_exists():
    ids = []
    global globallist
    for i in globallist:
        ids.append(i.id) 
    return ids

def print_list():
    global globallist
    s = ""
    for i in globallist:
        s+= i.username + "\n"
        print(i.username)
    return s

def welcome_message(item):
    print(item)
    global globvar

    if 'text' in item:
        chat_id = item['chat']['id']

        if item['text'] == "Nuevo usuario":
            user_id = item['from']['id']
            if 'username' in item['from']:
                username = item['from']['username']
                add_player(Player(user_id ,username,0,100))
   
                

            else:
                username = item['from']['first_name'] 
          
                add_player(Player(user_id ,username,0,100))
                
            msg = f'Bienvenido {username}'
            
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
            resp = requests.get(to_url)
            msg = 'Seleccionar un juego'+"\n"+ "1 --> Number"+ "\n" + "2 --> Trivia"
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
            resp = requests.get(to_url)

        elif item['text'] == "1":
            
            msg = 'Inicio del juego Number' + "\n" + "Jugadores: " + "\n" + print_list()
       
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
            resp = requests.get(to_url)      

        else:
            if item['from']['id'] not in check_if_user_exists():
                msg = 'Escribir "Nuevo usuario" para ser agregado al juego'
                to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={welcome_msg}&parse_mode=HTML'
                resp = requests.get(to_url)
    else:
        print("No hay text")
        

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