# IEMS5780_1155161089_bot
# 1155161089 XUZijun
# Deploying the Model as a Telegram Bot

import time
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import random
from joblib import load

class State:
    def __init__(self):
        self.statenum = "general"
        self.model = 0
        self.content = ""

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to demo bot.")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /hello - To reply you a hello
    Otherwise - To pick a random number between 0 and 1""")

def hello(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to demo bot.")
    
def asmt2model1(update: Update, context: CallbackContext):
    update.message.reply_text(
        "What is the title of your message?")
    s.statenum = "title"
    s.model = 1

def asmt2model1(update: Update, context: CallbackContext):
    update.message.reply_text(
        "What is the title of your message?")
    s.statenum = "title"
    s.model = 1
    
def asmt2model2(update: Update, context: CallbackContext):
    update.message.reply_text(
        "What is the title of your message?")
    s.statenum = "title"
    s.model = 2
    
def general(update: Update, context: CallbackContext):
    if s.statenum == "title":
        s.title = update.message.text
        s.statenum = "content"
        update.message.reply_text(
            "What is the content of your message?")
        return
    
    if s.statenum == "content":
        s.content = update.message.text
        s.statenum = "general"
        # use the loaded model to get the predicted values
        # output the result in the reply variable
        if s.model == 1:
            pre = model1.predict_proba([update.message.text])
        if s.model == 2:
            pre = model2.predict_proba([update.message.text])
        if pre[0][1] < 0.4:
            reply = "Your message is FAKE" + "(p = %.2f)" % pre[0][0]
        elif pre[0][1] > 0.6:
            reply = "The input message is REAL" + "(p = %.2f)" % pre[0][1]
        else:
            reply = "Cannot determine if the message is FAKE or REAL" + "(p = %.2f)" % pre[0][1]
        update.message.reply_text(reply)
        return
    

if __name__ == "__main__":
    # REQUEST_KWARGS = {
    #    'proxy_url': 'http://127.0.0.1:7890',
    # }
    # Provide your bot's token
    # updater = Updater("5252978559:AAFY4yiCU0aWcICh7gDzBgHCiWevdfYZnc0", use_context=True,  request_kwargs = REQUEST_KWARGS)
    updater = Updater("5252978559:AAFY4yiCU0aWcICh7gDzBgHCiWevdfYZnc0", use_context=True)

    # In assignment, if you need to load the model, load it here
    model1 = load("Count_1155161089.pkl")
    model2 = load("Tfid_1155161089.pkl")
    
    s = State()

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('asmt2model1', asmt2model1))
    updater.dispatcher.add_handler(CommandHandler('asmt2model2', asmt2model2))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, general))
    updater.start_polling()
