import requests
from flask import Flask, request,jsonify
import json
import random

globvar = 0
TOKEN = '5529622158:AAHYUHjS8xoigtNWrXLGLxzTc5M6TSzGA18'
globallist = []
ids = []
intro = 0
game = 0
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
    def __init__(self):
        self.status = 0
        self.number = 0
        self.maximum = 0
        self.tries = 5
        self.advanced = 0
        self.qm = 0
        self.qt = 0

    def playing(self):
        self.status = 1

    def started(self):
        self.advanced = 1
    
    def number_guess(self,number):
        num = random.randint(0,self.maximum)
        self.number = num





number = Number()

"""def set_global_to_one():
    global globvar 
    globvar = 1"""

def add_player(objeto):
    global globallist
    global ids
    globallist.append(objeto)
    ids.append(objeto.id)

def stop_intro():
    global intro
    intro = 1


def print_list():
    global globallist
    s = ""
    for i in globallist:
        s+= i.username + "\n"
    return s

def welcome_message(item):
    print(item)
    global globvar
    global game
    global ids
    if 'text' in item:
        chat_id = item['chat']['id']
        global intro

        if intro == 0:       
            if item['text'] == "nuevo usuario":
                
                if item['from']['id'] not in ids:
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

                else:
                    msg = f'Usuario ya existe'
                    
                    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
                    resp = requests.get(to_url)                    
                

                msg = 'Seleccionar un juego'+"\n"+ "1 --> Number"+ "\n" + "2 --> Trivia"
                to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
                resp = requests.get(to_url)


            elif item['text'] == "1":
                stop_intro()
                global number
                number.started()
                msg = 'Inicio del juego Number' + "\n" + "Jugadores: " + "\n" + print_list()
        
                to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
                resp = requests.get(to_url)      
                game = "number"
                msg = "Diga un máximo"
            
                to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
                resp = requests.get(to_url)      
                game = "number"
                

            else:
                print("ID PERSONA MENSAJE: ",item['from']['id'])
        
                print("TABLA IDS", ids)
                if item['from']['id'] not in ids:   
                    msg = 'Escribir "Nuevo usuario" para ser agregado al juego'
                    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
                    resp = requests.get(to_url)

        else:
            if game == "number":
                if number.maximum == 0:
                    if item['text'].isnumeric():
                        number.maximum = int(item['text'])
                        number.number_guess()
                    else:
                        msg = 'El texto debe ser un número'
                        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
                        resp = requests.get(to_url) 

                elif number.qt == 0:
                        msg = "Diga el número de intentos por jugador"
                        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
                        resp = requests.get(to_url)  
                        number.qt = 1

                elif number.tries == 0:
                    if item['text'].isnumeric():
                        number.tries = int(item['text'])
                    else:
                        msg = 'El texto debe ser un número'
                        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
                        resp = requests.get(to_url)     
                print("DATOS DEL JUEGO")                  
                print(number.maximum,number.number,number.tries)
                print(print_list)
               


                



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