#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telepot
import sys
import time
import os
import emoji
import dbhelper
from telepot.loop import MessageLoop
from googletrans import Translator


texte01 = '🚫 Problema con la traduzione. Digitare correttamente'
texte02 = "⚠️⚠️ Non hai inserito un testo. Riprova e passami il link. 😊"

texti02 = "Ciao <strong>&0, </strong>digita qualcosa per iniziare subito a tradurre!😎\n"\
          "Lingua di partenza <strong>Italiano 🇮🇹</strong>.\n" \
          "Lingua di destinazione <strong>Inglese 🇬🇧</strong>.\n"\
          "Lista comandi ⚙️ <strong>Comandi:</strong>\n" \
          "/en - Traduzione in Inglese 🇬🇧\n" \
          "/fr - Traduzione in Francese 🇫🇷 \n" \
          "/es - Traduzione in Spagnolo 🇪🇸 \n" \
          "/de - Traduzione in Tedesco 🇧🇪 \n" \
          "/switch - Scambia la lingua 🔄\n"\
          "/help - Lista dei comandi 📖\n"\
          "Per tutte le traduzione verrà utilizzato Google Translate\n" \
          "Buon divertimento✌️"


texti03 = "⚙️ <strong>Comandi:</strong>\n" \
          "\n" \
          "/en - Traduzione in Inglese 🇬🇧\n"\
          "/fr - Traduzione in Francese 🇫🇷 \n" \
          "/es - Traduzione in Spagnolo 🇪🇸 \n" \
          "/de - Traduzione in Tedesco 🇧🇪 \n" \
          "/switch - Scambia la lingua 🔄\n"\
          "/help - Lista dei comandi 📖\n"

def traduci_testo(parola_from, chat_id, lingua_dest, lingua_src):
    trans = Translator(service_urls=['translate.google.com'])

    # Effettuo la traduzione
    translation = trans.translate(parola_from, src=lingua_src, dest=lingua_dest)
    return translation.text


def mostra_start(chat_id,name):
    testo = texti02.replace('&0', name)
    bot.sendMessage(chat_id, testo, parse_mode='HTML')


def mostra_info(chat_id):
    bot.sendMessage(chat_id, texti03, parse_mode='HTML')


def switch_lingua(chat_id, lingua_dest, lingua_src):

    lingua_temp = lingua_src
    lingua_src = lingua_dest
    lingua_dest = lingua_temp

    text_src = '/' + lingua_src
    text_dest = '/' + lingua_dest
    bot.sendMessage(chat_id, 'Da %s a %s' % (dict_comandi_lingua.get(text_src), dict_comandi_lingua.get(text_dest)),
                        parse_mode='HTML')

    return lingua_src, lingua_dest

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    input_text = ''
    # Prelevo il messaggio inserito dall'utente e controllo che sia un testo
    try:
        input_text = msg['text']
    except:
        bot.sendMessage(chat_id, texte02)

    if input_text:
        db = dbhelper.DBHelper()
        db.create_table()
        name = msg['from']['first_name']
        print(content_type, chat_type, chat_id, name)

        items = db.get_items(chat_id)
        if not items:
            lingua_src = 'it'
            lingua_dest = 'en'
            db.add_item(chat_id, lingua_src, lingua_dest)
        else:
            lingua_src = items[0][1]
            lingua_dest = items[0][2]

        if input_text == '/start' or input_text =='/start@iltradutorebot':
            mostra_start(chat_id, name)
        elif input_text == '/help' or input_text == '/help@iltraduttorebot':
            mostra_info(chat_id)
        elif input_text == '/switch' or input_text == '/switch@iltraduttorebot':
            lingua_src, lingua_dest = switch_lingua(chat_id, lingua_dest, lingua_src)
            db.update_items(chat_id, lingua_src, lingua_dest)
        else:
            try:
                if input_text in dict_comandi_lingua:
                    bot.sendMessage(chat_id, 'Ho settato la lingua in: %s' % (dict_comandi_lingua.get(input_text)))
                    input_text = input_text.replace('/','')
                    lingua_dest = input_text[:2]
                    lingua_src = 'it'
                    db.update_items(chat_id, lingua_src, lingua_dest)
                else:
                    # Chiamo la funzione che esegue la traduzione
                    parolatrad = traduci_testo(input_text, chat_id, lingua_dest, lingua_src)
                    # Invio la traduzione all'utente
                    bot.sendMessage(chat_id, parolatrad)
            except:
                bot.sendMessage(chat_id, texte01)

dict_comandi_lingua = {'/en': 'Inglese🇬🇧', '/en@iltraduttorebot': 'Inglese🇬🇧',
                       '/fr': 'Francese🇫🇷', '/fr@iltraduttorebot': 'Francese🇫🇷',
                       '/es': 'Spagnolo🇪🇸', '/es@iltraduttorebot': 'Spagnolo🇪🇸',
                       '/de': 'Tedesco🇧🇪','/de@iltraduttorebot': 'Tedesco🇧🇪',
                       '/it': 'Italiano🇮🇹', '/it@iltraduttorebot': 'Italiano🇮🇹'
                       }
TOKEN = os.environ.get('API_TOKEN', None)

if __name__ == "__main__":
    # Recuper il TOKEN
    bot = telepot.Bot(TOKEN)
    # Avvio il loop dei messaggi
    MessageLoop(bot, {'chat': on_chat_message, }).run_as_thread()
    print('Listening ...')
    while 1:
        time.sleep(10)
