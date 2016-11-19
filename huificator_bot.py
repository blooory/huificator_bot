from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from telegram.ext.dispatcher import run_async
import telegram
import logging
import numpy as np
import string
import json

with open('params.json', 'r') as temp_file:
    TOKEN = json.load(temp_file)['TOKEN']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def n_slogov(s):
    return len(list(filter(lambda x: x in 'уеыаоэяию', list(s))))


def vowel_pos(s, num_vowel):
    cnt = 0
    vowel_cnt = 0
    for i in s:
        if (i in 'уеыаоэяию'):
            vowel_cnt += 1
            if vowel_cnt == num_vowel:
                return cnt
        cnt += 1

def replace_string(s, d):
    for key in d:
        s = s.replace(key, d[key])
    return s

def leave_only_russian_letters(s):
    s_upd = ''
    for letter in s:
        s_upd += letter*(letter in 'йцукенгшщзхъфывапролджэячсмитьбю ')
    return s_upd

def start(bot, update):
    update.message.reply_text('Хуй тебе {0}, рад видеть'.format(update.message.from_user.first_name))
    with open('chat_ids.txt', 'a') as f:
        f.write(str(update.message.chat_id) +';'+ update.message.from_user.first_name + ';'+ update.message.from_user.last_name + ';' + str(update.message.date) +'\n')

def hui(bot, update):
    if np.random.rand(1)[0] < 0.05:
        text = update.message.text
        exclude = set(string.punctuation)
        text = (''.join(ch for ch in text if ch not in exclude)).lower()
        text = leave_only_russian_letters(text)
        text = [x for x in (set(text.split(' ')) - {''}) if n_slogov(x)>=2]
        if len(text) != 0:
            hui_word = np.random.choice(text, 1)[0]
            prefix = 'ху'
            print(hui_word)
            if n_slogov(hui_word) <= 2:
                vowel = hui_word[vowel_pos(hui_word, 1)]
                postfix = hui_word[(vowel_pos(hui_word, 1)+1):]
                vowel = replace_string(vowel, {'а':'я', 'у':'ю', 'о':'е'})
            else:
                vowel = hui_word[vowel_pos(hui_word, 2)]
                postfix = hui_word[(vowel_pos(hui_word, 2)+1):]
                vowel = replace_string(vowel, {'а':'я', 'у':'ю', 'о':'е'})
            hui_word = prefix + vowel + postfix
            bot.sendMessage(chat_id = update.message.chat_id, text = hui_word)

updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler([Filters.text], hui))

updater.start_polling()
updater.idle()