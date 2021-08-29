import json
import logging
from pprint import pprint

import requests
import sqlite3

# from test import get_updates_id
from telebot.db import SQL
from telebot.models import Message
from PIL import Image

TELEGRAM_TOKEN= "1997016618:AAFyB0L5CDG44dFjIj5pkjboJNBJZJNamGg"


def send_message(msg, chatid, token):
    """ Manda mensaje a un usuario

    token: es lo que debe estar en el .env
    """
    assert type(chatid) == int
    assert type(msg) == str
    assert type(token) == str

    BASE_URL = f"https://api.telegram.org/bot{token}"
    fullmsg = f"sendMessage?text={msg}&chat_id={chatid}"
    # query params
    rsp = requests.get(f"{BASE_URL}/{fullmsg}")
    logging.debug("Message sent %s", rsp.text)


def get_chat_id(username, token):
    """ have pull en base a un username
    token: es lo que debe estar en el .env
    """

    BASE_URL = f"https://api.telegram.org/bot{token}"
    rsp = requests.get(f"{BASE_URL}/getUpdates")
    for r in rsp.json()["result"]:
        msg = r.get("message")
        if msg["from"]["username"] == username:
            id_ = msg["chat"]["id"]
            print(f"Chatid is: {id_}")
            return


def get_updates_id(database, table):
    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    fetch = cursor.fetchall()
    update_ids = []

    for fila in fetch:
        update_ids.append(fila[0])

    conn.close()
    return update_ids


#print (get_updates_id("telegram.db","tlg_update")) #debug

def get_updates(token):
    """ Obtiene todos los mensajes desde telegram
    API information: https://core.telegram.org/bots/api#getupdates
    Ejemplo de rsp.json()["result"]:
    [
    {'message': {'chat': {'first_name': 'Xavier',
                        'id': 222,
                        'last_name': 'Petit',
                        'type': 'private',
                        'username': 'xpetit'},
                'date': 1628086187,
                'from': {'first_name': 'Xavier',
                        'id': 3333,
                        'is_bot': False,
                        'language_code': 'en',
                        'last_name': 'Petit',
                        'username': 'xpetit'},
                'message_id': 7,
                'text': 'pepe'},
    'update_id': 478400752},
    ...
    ...
    ]
    """
    BASE_URL = f"https://api.telegram.org/bot{token}"
    updates_id = get_updates_id("telegram.db","tlg_update")
    parametros = {"offset": 0, "limit": 100}
    try:
        parametros ["offset"] = updates_id[-1] + 1
    except IndexError:
        pass
    print (parametros)
    rsp = requests.get(f"{BASE_URL}/getUpdates", params=parametros)

    #pprint(rsp.json()["result"]) # debug
    return rsp.json()["result"]

#debug1 = get_updates(TELEGRAM_TOKEN)
#print (type(debug1))
#print (debug1)

def register_message(sql: SQL, data, tkn):
    """
    Recibe un mensaje, lo guarda en la base y envia
    un response.
    {'chat': {'first_name': 'Xavier',
                      'id': 44444,
                      'last_name': 'Petit',
                      'type': 'private',
                      'username': 'xpetit'
             },
     'date': 1628087051,
     'from': {'first_name': 'Xavier',
                      'id': 4444,
                      'is_bot': False,
                      'language_code': 'en',
                      'last_name': 'Petit',
                      'username': 'xpetit'},
     'message_id': 15,
     'text': 'dame info'}
    """
    msg = Message(sql)
    print(f"data:: {data}")
    try:
        msg.add(data["chat"]["id"], data["message_id"], data["text"])
    except KeyError:
        file_id = data["photo"][0]["file_id"]
        print(f"downlaod_image return: {download_image(file_id, TELEGRAM_TOKEN)}")


def respond_message(data, tkn):
    send_message(f"👋 Hola {data['chat']['first_name']}! en que te puedo ayudar?",
        data["chat"]["id"], tkn
        )


def continuar_interaccion(data, tkn):
    cant_interacciones = len(get_updates_id("telegram.db","tlg_update"))
    print (cant_interacciones)
    while True:
        send_message(
            f"Genial! Que informacion quieres que te de hoy?",
            data["chat"]["id"], tkn
        )
        break

def peticion_del_usuario (database,data,tkn):
    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute(f"SELECT text FROM message")
    fetch = cursor.fetchall()
    mensajes = []
    for fila in fetch:
        mensajes.append(fila[0])

    conn.close()
    print (mensajes)

    while True:
        try:
            return str(mensajes[-1])
        except ValueError:
            send_message(
            f"Procesando...",
            data["chat"]["id"], tkn
        )
            pass
        else:
            break

def download_image(file_id, bot_token):
    # Returns the local path to the downloaded file
    response = requests.get(
        f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
    )

    file_path = response.json()["result"]["file_path"]
    response = requests.get(
       f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
    )

    local_filename = f"images/{file_id}.png"
    with open(local_filename, 'wb') as f:
        f.write(response.content)
    return local_filename
