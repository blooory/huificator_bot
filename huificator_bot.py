from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from telegram.ext.dispatcher import run_async
import telegram
import logging
import numpy as np
import json
import pickle
from special_function import special_function
from word_functions import n_slogov, vowel_pos, replace_string, leave_only_russian_letters, huificate_word, \
                           preprocess_text, find_verbs
import pymorphy2 as pm2
import csv

with open('params.json', 'r') as temp_file:
    TOKEN = json.load(temp_file)['TOKEN']

# Add word dictionary
word_dict = {}
with open('dict.txt') as f:
    word_dict = {key: value for (key, value) in csv.reader(f)}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    update.message.reply_text('Хуй тебе {0}, рад видеть'.format(update.message.from_user.first_name))
    with open('chat_ids.txt', 'a') as f:
        f.write(str(update.message.chat_id) + ';' +
                update.message.from_user.first_name + ';' +
                update.message.from_user.last_name + ';' +
                str(update.message.date) + '\n')


def hui(bot, update):
    rv = np.random.rand(1)[0]

    # запоминаем имя автора сообщения
    name_user = update.message.from_user.first_name

    # say smth to net

    if ('почему' in str.lower(update.message.text)) & (' почему' not in str.lower(update.message.text)):
        bot.sendMessage(chat_id=update.message.chat_id, text='Потому что ты осёл, ' + name_user)
    elif '?' in update.message.text:
        if rv < 0.05:
            bot.sendMessage(chat_id=update.message.chat_id, text='Отвечают только пидарасы')
    elif leave_only_russian_letters(str.lower(update.message.text)) in word_dict:
        if rv < 0.35:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=word_dict[leave_only_russian_letters(str.lower(update.message.text))])
    else:
        # huificate word
        if rv < 0.2:
            text = preprocess_text(update.message.text)
            if len(text) != 0:  
                flag, hui_word = special_function(text, update)
                if flag:
                    bot.sendMessage(chat_id=update.message.chat_id, text=hui_word)
                elif (rv < 0.07):
                    hui_word = huificate_word(np.random.choice(text, 1)[0])
                    bot.sendMessage(chat_id=update.message.chat_id, text=hui_word)
        # say smth about mom
        if rv > 0.925:
            print('for mamka', update.message.text, update.message.chat_id)
            text = preprocess_text(update.message.text)
            if len(text) != 0:
                verbs = find_verbs(text, parser)
                if len(verbs) != 0:
                    your_mom_message = 'Мамка твоя '+np.random.choice(verbs, 1)[0]+', '+name_user+'!'
                    print(your_mom_message)
                    bot.sendMessage(chat_id=update.message.chat_id, text=your_mom_message)

updater = Updater(TOKEN)

parser = pm2.MorphAnalyzer()
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler([Filters.text], hui))

updater.start_polling()
updater.idle()