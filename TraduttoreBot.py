#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telepot, sys, time, os
from telepot.loop import MessageLoop
from googletrans import Translator
import emoji

texte01 = '🚫 Problema con la traduzione. Digitare correttamente'
texti02 = "Ciao <strong>&0, </strong>digita qualcosa per iniziare subito a tradurre!😎\n"\
          "La lingua di partenza è in <strong>Italiano 🇮🇹</strong>.\n" \
          "La lingua di destinazione è in <strong>Inglese 🇬🇧</strong>.\n" \
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
          "/en - Traduzione in Inglese 🇬🇧\n" \
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
#     testo = texti02.replace('&0', str(name.encode('utf-8')))
    testo = texti02.replace('&0', name)
    bot.sendMessage(chat_id, testo, parse_mode='HTML')


def mostra_info(chat_id):
    testo = texti03.replace('&0', str(emoji.emojize(':gear:', use_aliases=True).encode('utf-8')))
    bot.sendMessage(chat_id, testo, parse_mode='HTML')


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
    global lingua_dest, lingua_src
    content_type, chat_type, chat_id = telepot.glance(msg)
    input_text = msg['text']
    name = msg['chat']['first_name']
    print(content_type, chat_type, chat_id, name)

    if input_text == '/start':
        mostra_start(chat_id, name)
    elif input_text == '/help':
        mostra_info(chat_id)
    elif input_text == '/switch':
        lingua_src, lingua_dest = switch_lingua(chat_id, lingua_dest, lingua_src)
    else:
        try:
            if input_text in dict_comandi_lingua:
                bot.sendMessage(chat_id, 'Ho settato la lingua in: %s' % (dict_comandi_lingua.get(input_text)))
                input_text = input_text.replace('/','')
                lingua_dest = input_text
                lingua_src = 'it'
            else:
                # Chiamo la funzione che esegue la traduzione
                parolatrad = traduci_testo(input_text, chat_id, lingua_dest, lingua_src)
                # Invio la traduzione all'utente
                bot.sendMessage(chat_id, parolatrad)
        except:
            bot.sendMessage(chat_id, texte01)

dict_comandi_lingua = {'/en': 'Inglese🇬🇧', '/fr': 'Francese🇫🇷', '/es': 'Spagnolo🇪🇸', '/de': 'Tedesco🇧🇪', '/it': 'Italiano🇮🇹'}
lingua_src = 'it'
lingua_dest = 'en'
# TOKEN = os.environ.get('API_TOKEN', None)
TOKEN = '834994363:AAEOcDtlg9j1nSd-9vgoec-siUdD10oV2VE'

if __name__ == "__main__":
    # Recuper il TOKEN
    bot = telepot.Bot(TOKEN)
    # Avvio il loop dei messaggi
    MessageLoop(bot, {'chat': on_chat_message, }).run_as_thread()
    print('Listening ...')
    while 1:
        time.sleep(10)

