import logging
from pprint import pprint

import requests

#from telebot.db import SQL
#from telebot.models import Message
#from telebot.telegram import send_message
# from telebot.telegram import download_image
from telebot import telegram

'''
class Clase():
    def __init__(self, arg):
        #codigo que se ejecuta cuando se instancia un objeto de la clase
        print(f"Estoy inicializando la clase")
        print(f"Recibi el argumento {arg}")
        self.name = arg

    def print_something(self):
        print(f"Hola {self.name}")


def test_main():
    objeto = Clase("Tomas")
    objeto.print_something()

'''
bot_token = "1997016618:AAFyB0L5CDG44dFjIj5pkjboJNBJZJNamGg"
file_id = "AgACAgEAAxkBAAMgYSvaregAAetuoic-Im2GEDepRDOtAAJKqjEb-txgRX_q-gMNaljYAQADAgADeAADIAQ"
print(f"downlaod_image return: {telegram.download_image(file_id, bot_token)}")

 
# https://www.dustloop.com/wiki/images/thumb/5/5f/DBFZ_SS4Gogeta_x100BigBangKamehameha.png/800px-DBFZ_SS4Gogeta_x100BigBangKamehameha.png
# Probando imagenes

