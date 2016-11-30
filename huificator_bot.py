from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from telegram.ext.dispatcher import run_async
import telegram
import logging
import numpy as np
import json
import pickle
import string
from special_function import special_function
from word_functions import we_find_latin_letters,n_slogov, vowel_pos, \
        replace_string, leave_only_russian_letters, huificate_word, \
        preprocess_text,find_verbs
from other_functions import check_time
import pymorphy2 as pm2
import csv
from datetime import datetime, timedelta

with open('params.json', 'r') as temp_file:
    TOKEN = json.load(temp_file)['TOKEN']
old_message_flag = True
now = datetime.now()
# Add word dictionary
word_dict={}
with open('dict.txt') as f:
    word_dict={key:value for (key,value) in csv.reader(f)}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    update.message.reply_text('Хуй тебе {0}, рад видеть'.format(update.message.from_user.first_name))
    with open('chat_ids.txt', 'a') as f:
        f.write(str(update.message.chat_id) +';'+ update.message.from_user.first_name + ';'+ update.message.from_user.last_name + ';' + str(update.message.date) +'\n')

import re
regexp_question = re.compile('\?$')

new_re_dict = {}
for phrase in word_dict:
    my_str = '\s{1,1}'+phrase+'['+string.punctuation+']{0,6}$'+'|^'+phrase+'['+string.punctuation+']{0,6}$'
    reg_exp = re.compile(my_str)
    new_re_dict[reg_exp] = word_dict[phrase]
    
def hui(bot, update):
    global old_message_flag
    if old_message_flag:
        if update.message.date > now - timedelta(hours = 1):
            old_message_flag = False
    else:

        rv = np.random.rand(1)[0]

        text_raw = update.message.text
        text = preprocess_text(text_raw)
        text, fake_flag = we_find_latin_letters(text)
        
        if fake_flag:
            name_user = update.message.from_user.first_name
            msg_about_fake = 'Наебать нас хотел, ' + name_user + '!'
            bot.sendMessage(chat_id = update.message.chat_id, text = msg_about_fake)
            
        if len(regexp_question.findall(text_raw)) > 0:
            if rv<0.15:
                bot.sendMessage(chat_id = update.message.chat_id, text = 'Отвечают только пидарасы')
        else:
            # check on regexp compl
            text_raw = text_raw.lower()
            for regexp in new_re_dict:
                if len(regexp.findall(text_raw)) > 0:
                    if rv > 0.5:
                        bot.sendMessage(chat_id = update.message.chat_id, text = new_re_dict[regexp])
            # huificate word
            if rv < 0.2:
                if len(text) != 0:  
                    flag, hui_word = special_function(text, update)
                    if flag:
                        bot.sendMessage(chat_id = update.message.chat_id, text = hui_word)
                    elif (rv<0.07):        
                        hui_word = huificate_word(np.random.choice(text, 1)[0])
                        bot.sendMessage(chat_id = update.message.chat_id, text = hui_word)
            # say smth about mom with verb
            if (rv > 0.925):
                print('for mamka', update.message.text, update.message.chat_id)
                if (len(text) != 0) :
                    verbs = find_verbs(text, parser)
                    if len(verbs) != 0:
                        rv_for_appeal = np.random.rand(1)[0]
                        if rv_for_appeal > 0.5:
                            name_user = update.message.from_user.first_name
                            your_mom_message = 'Мамка твоя '+np.random.choice(verbs,1)[0]+', '+name_user+'!'
                            print(your_mom_message)
                            bot.sendMessage(chat_id = update.message.chat_id, text = your_mom_message)
                        else:
                            your_mom_message = 'Мамка твоя '+np.random.choice(verbs,1)[0]+'!'
                            print(your_mom_message)
                            bot.sendMessage(chat_id = update.message.chat_id, text = your_mom_message)
    


updater = Updater(TOKEN)

parser = pm2.MorphAnalyzer()
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler([Filters.text], hui))


updater.start_polling()
updater.idle()