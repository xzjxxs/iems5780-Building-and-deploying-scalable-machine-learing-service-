# IEMS5780_1155161089_bot
# 1155161089 XUZijun
# Deploying the Model as a Telegram Bot

import socket
import requests
import validators
from queue import Queue
from threading import Thread
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters


user = None
q1 = Queue()
q2 = Queue()


# Process message from user
def thread1():
    def start(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Hello sir, Welcome to demo bot."
        )

    def help(update: Update, context: CallbackContext):
        update.message.reply_text("""Available Commands :=
        /hello - To reply you a hello.
        Otherwise - Send an image or the url of the image to predict what bird""")

    def hello(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Hello sir, Welcome to demo bot."
        )

    def image_handler(update: Update, context: CallbackContext):
        global user
        user = update
        file = update.message.photo[-1].file_id
        obj = context.bot.get_file(file)
        b = obj.download_as_bytearray()

        q1.put(b)
        update.message.reply_text("Received image, predicting!")

    def text_handler(update: Update, context: CallbackContext):
        global user
        v = validators.url(update.message.text)
        if v:
            user = update
            update.message.reply_text("Downloading your image from: {}, please wait!".format(update.message.text))
            r = requests.get(update.message.text, timeout=20)
            update.message.reply_text("Predicting!")
            q1.put(r.content)
        else:
            update.message.reply_text("{} is not a valid URL to download the image!".format(update.message.text))

    REQUEST_KWARGS = {
        'proxy_url': 'http://127.0.0.1:7890',
    }
    updater = Updater("5252978559:AAFY4yiCU0aWcICh7gDzBgHCiWevdfYZnc0", use_context=True, request_kwargs=REQUEST_KWARGS)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
    updater.start_polling()


# Communicate with the server that is running the image classification
def thread2():
    while True:
        message = q1.get()
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(("127.0.0.1", 8080))
        soc.send(message)
        data = soc.recv(1024).decode("UTF-8")
        q2.put(data)
        soc.close()


# Send response to user
def thread3():
    while True:
        message = q2.get()
        user.message.reply_text(message)


threads = list()

messageThread = Thread(target=thread1)
messageThread.start()
threads.append(messageThread)

tcpThread = Thread(target=thread2)
tcpThread.start()
threads.append(tcpThread)

replyThread = Thread(target=thread3)
replyThread.start()
threads.append(replyThread)
