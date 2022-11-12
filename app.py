import telegram
import telegram.ext
import re
from random import randint
import telebot
from config import USER_LOCK
from flask import Flask, request, jsonify
import json

web_server = Flask(__name__)



#from pyrogram import Client, filters


# The API Key we received for our bot
#Mi bot
#API_KEY = '5707149316:AAHFQ-XY23rwGgZ9RNECy6TgPDTVtbmCQeE'

#Bot de Sofi
#API_KEY = '5607369368:AAHEBTuVYxEGuyyBp2gZeP5vqOcMyhkkt4M'

#Bot mas nuevo
API_KEY = '5529622158:AAHYUHjS8xoigtNWrXLGLxzTc5M6TSzGA18'


bot = telebot.TeleBot(API_KEY)


# Create an updater object with our API Key
updater = telegram.ext.Updater(API_KEY)
# Retrieve the dispatcher, which will be used to add handlers
dispatcher = updater.dispatcher
# Our states, as integers
WELCOME = 0
MINIMO = 1
MAXIMO = 2
INTENTOS = 3
QUESTION = 4
CANCEL = 5
CORRECT = 6
OPTIONS = 7
ESTADISTICAS = 8

USER_LOCK = 0

# The entry function
def start(update_obj, context):
    msg = update_obj.message
    global USER_LOCK
    lock = USER_LOCK

    if lock != 0:
        update_obj.message.reply_text(f"Estoy ocupado!, chau")
        return telegram.ext.ConversationHandler.END

    
    USER_LOCK =  update_obj.message.from_user['id']
    update_obj.message.reply_text('Hola ' +  update_obj.message.from_user['first_name'] + ', bienvenido!! Selecciona una opción para comenzar: \n')

    """
    update_obj.message.reply_text('En este bot de telegram podrás jugar a varios juegos (en proceso). Sólo selecciona el que más te guste, y comienza a jugar!!\n')
    update_obj.message.reply_text('También, si te interesa, puedes ver las estadísticas de todos los miembros del grupo.')
    """
    """
    text_html += 'Number  →'+ " Adivina el número que eligió el bot, eligiendo el máximo y el mínimo. ¡Trata de adivinar con la menor cantidad de intentos posibles!" + '\n'
    # send the question, and show the keyboard markup (suggested answers)
    update_obj.message.reply_text(text_html)
    update_obj.message.reply_text("¿Quieres jugar?",
        reply_markup=telegram.ReplyKeyboardMarkup([['Si', 'No']], one_time_keyboard=True)
    )
    """

    update_obj.message.reply_text("1 --> ver estadísticas" + "\n" + "2 --> Jugar Number"+ "\n" + "3 --> Salir del bot",
            reply_markup=telegram.ReplyKeyboardMarkup([['1', '2','3']], one_time_keyboard=True)
        )
    # go to the WELCOME state
    return OPTIONS

# helper function, generates new numbers and sends the question
def randomize_numbers(update_obj, context):
    # store the numbers in the context
    update_obj.message.reply_text("Di el minimo")
    return MINIMO

def randomize_numbers2(update_obj, context):
    # store the numbers in the context
    update_obj.message.reply_text("Di el maximo")
    return MAXIMO

# in the WELCOME state, check if the user wants to answer a question
def welcome(update_obj, context):
    if update_obj.message.text.lower() in ['si', 's']:
        # send question, and go to the QUESTION state
        context.user_data['tries'] = 0
        update_obj.message.reply_text("Di el mínimo")
        return MINIMO
    else:
        update_obj.message.reply_text("1 --> ver estadísticas" + "\n" + "2 --> Jugar Number"+ "\n" + "3 --> Salir del bot",
            reply_markup=telegram.ReplyKeyboardMarkup([['1', '2','3']], one_time_keyboard=True)
        )
        # go to the CANCEL state
        return OPTIONS

def minimo(update_obj,context):
    user = update_obj.message.from_user
    context.user_data['minimo'] =  int(update_obj.message.text)
    update_obj.message.reply_text("Ahora dime el máximo")
    return MAXIMO
    

def maximo(update_obj,context):
    user = update_obj.message.from_user
    context.user_data['maximo'] =  int(update_obj.message.text)
    context.user_data['random'] = randint(context.user_data['minimo'],context.user_data['maximo'])
    update_obj.message.reply_text("Guess "+ str(context.user_data['random']))
    update_obj.message.reply_text("Ingrese la cantidad de intentos permitidos")
    return INTENTOS

def intentos(update_obj,context):
    user = update_obj.message.from_user
    context.user_data['tries'] =  int(update_obj.message.text)
    update_obj.message.reply_text("Comience a jugar. Adivine un número del "+ str(context.user_data['minimo'])+" al "+str(context.user_data['maximo']))
    update_obj.message.reply_text("Tiene "+ str(context.user_data['tries']) + " intentos")
    context.user_data['ronda'] = 1
    return QUESTION


# in the QUESTION state
def question(update_obj, context):
    # expected solution
    solution = int(context.user_data['random'])

    #provided answer
    answer = int(update_obj.message.text)

    update_obj.message.reply_text(f"Ronda {int(context.user_data['ronda']) + 1}, Respuesta dada: {answer} ")

    # check if the solution was correct
    if context.user_data['tries'] > 1:
        if solution == answer:
            # correct answer, ask the user if he found tutorial helpful, and go to the CORRECT state
            update_obj.message.reply_text("Respuesta correcta!")
            context.user_data['tries'] -= 1
            update_obj.message.reply_text(f"Cantidad de intentos: {context.user_data['tries']}")
            update_obj.message.reply_text("Quieres seguir jugando?",
            reply_markup=telegram.ReplyKeyboardMarkup([['Si', 'No']], one_time_keyboard=True)
            )
            return WELCOME
        elif solution < answer < context.user_data['maximo']:
            # wrong answer, reply, send a new question, and loop on the QUESTION state
            update_obj.message.reply_text("La respuesta es un número menor..." + '\n' + "Trata otra vez")
            context.user_data['tries'] -= 1
            
            update_obj.message.reply_text(f"Intentos: {context.user_data['tries']}")
            # send another random numbers calculation
    
        elif solution > answer > context.user_data['minimo']:
            # wrong answer, reply, send a new question, and loop on the QUESTION state
            update_obj.message.reply_text("La respuesta es un número mayor..." + '\n' + "Trata otra vez")
            context.user_data['tries'] -= 1
            update_obj.message.reply_text(f"Intentos: {context.user_data['tries']}")
            # send another random numbers calculation
        
        else:
            # wrong answer, reply, send a new question, and loop on the QUESTION state
            update_obj.message.reply_text("La respuesta que has dado está fuera del rango..." + '\n' + "Trata otra vez")
            context.user_data['tries'] -= 1
            update_obj.message.reply_text(f"Intentos: {context.user_data['tries']}")
            # send another random numbers calculation
        return QUESTION
    else:
        first_name = update_obj.message.from_user['first_name']
        update_obj.message.reply_text(f"Perdiste. Nos vemos {first_name}!, chau")
        USER_LOCK = 0
        return telegram.ext.ConversationHandler.END



# in the CORRECT state
def correct(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        update_obj.message.reply_text(f"Continuar jugando al juego Number?")
        return WELCOME
    else:
        return CANCEL


def cancel(update_obj, context):
    update_obj.message.reply_text("1 --> ver estadísticas" + "\n" + "2 --> Jugar Number"+ "\n" + "3 --> Salir del bot",
        reply_markup=telegram.ReplyKeyboardMarkup([['1', '2','3']], one_time_keyboard=True)
    )
    return OPTIONS


def options(update_obj, context):
    global USER_LOCK
    
    first_name = update_obj.message.from_user['first_name']

    if update_obj.message.text == str(1):
        chatId = update_obj.message.chat.id
        update_obj.message.reply_text(f"ID del chat: {chatId}")

       
        
        memberCount = bot.get_chat_member_count(chat_id=chatId)
        update_obj.message.reply_text(f"{memberCount}")
        update_obj.message.reply_text(f"funciono")

        
        
        
        #update_obj.message.reply_text(f"Miembros en el grupo: {member_total}")
        return ESTADISTICAS

    elif update_obj.message.text == str(2):
        msg = update_obj.message
        text_html = 'Number  →'+ " Adivina el número que eligió el bot, eligiendo el máximo y el mínimo. ¡Trata de adivinar con la menor cantidad de intentos posibles!" + '\n'
        # send the question, and show the keyboard markup (suggested answers)
        update_obj.message.reply_text(text_html)
        update_obj.message.reply_text("¿Quieres jugar?",
            reply_markup=telegram.ReplyKeyboardMarkup([['Si', 'No']], one_time_keyboard=True)
        )       
        return WELCOME
    elif update_obj.message.text == str(3):
        update_obj.message.reply_text(f"Nos vemos {first_name}!, chau")
        USER_LOCK = 0
        return telegram.ext.ConversationHandler.END
    else:
        update_obj.message.reply_text("Comando no disponible")

        return CANCEL

def estadisticas(update_obj,context):
    update_obj.message.reply_text("ESTADÍSTICAS")

    #TELEGRAM_URL = "https://api.telegram.org/bot" + API_KEY


    return OPTIONS


# a regular expression that matches yes or no
yes_no_regex = re.compile(r'^(si|no|s|n)$', re.IGNORECASE)
yes_no_regex_2 = re.compile(r'^(si|no|s|n|1|2|3)$', re.IGNORECASE)
# Create our ConversationHandler, with only one state
handler = telegram.ext.ConversationHandler(
      entry_points=[telegram.ext.CommandHandler('start', start)],
      states={
            WELCOME: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), welcome)],
            MINIMO: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^\d+$'), minimo)],
            MAXIMO: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^\d+$'), maximo)],
            INTENTOS: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^\d+$'), intentos)],
            QUESTION: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^\d+$'), question)],
            CANCEL: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), cancel)],
            CORRECT: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), correct)],
            OPTIONS: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^(1|2|3)+$'), options)],
            ESTADISTICAS: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), estadisticas)],
          
      },
      fallbacks=[telegram.ext.CommandHandler('cancel', cancel)],
      )


# add the handler to the dispatcher
dispatcher.add_handler(handler)
# start polling for updates from Telegram
updater.start_polling()
# block until a signal (like one sent by CTRL+C) is sent
updater.idle()

