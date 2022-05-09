import time

from surprise import Reader, Dataset, dump
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import random
from collections import defaultdict
from redis import StrictRedis
import pandas as pd


class State:
    def __init__(self):
        self.statenum = 'general'
        self.res = []
        self.animeID = 0
        self.sendContext = ""


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to demo bot.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /hello - To reply you a hello
    /Anime_recommendation - Recommend Top 10 anime for you 
    """)


def hello(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to demo bot.")


def handler_rating(update: Update, context: CallbackContext):
    if s.statenum == "start_predict":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Please rate the following movie(from 1 to 10) \n" + animeList[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Your response should be integer from 1 to 10")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question2"
            s.animeID = rand_num

        return
    if s.statenum == "question2":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Please rate the following movie(from 1 to 10) \n" + animeList[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Your resonse should be integer from 1 to 10")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question3"
            s.animeID = rand_num

        return

    if s.statenum == "question3":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Please rate the following movie(from 1 to 10) \n" + animeList[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Your resonse should be integer from 1 to 10")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question4"
            s.animeID = rand_num

        return
    if s.statenum == "question4":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Please rate the following movie(from 1 to 10) \n" + animeList[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Your resonse should be integer from 1 to 10")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question5"
            s.animeID = rand_num

        return

    if s.statenum == "question5":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Please rate the following movie(from 1 to 10) \n" + animeList[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Your resonse should be integer from 1 to 10")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question6"
            s.animeID = rand_num

        return

    if s.statenum == "question6":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Please rate the following movie(from 1 to 10) \n" + animeList[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Your resonse should be integer from 1 to 10")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question7"
            s.animeID = rand_num

        return

    if s.statenum == "question7":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Please rate the following movie(from 1 to 10) \n" + animeList[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Your resonse should be integer from 1 to 10")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question8"
            s.animeID = rand_num

        return
    if s.statenum == "question8":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Please rate the following movie(from 1 to 10) \n" + animeList[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Your resonse should be integer from 1 to 10")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question9"
            s.animeID = rand_num

        return

    if s.statenum == "question9":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Please rate the following movie(from 1 to 10) \n" + animeList[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Your resonse should be integer from 1 to 10")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "predict"
            s.animeID = rand_num

        return

    if s.statenum == "predict":
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Your response should be integer from 1 to 10")
        else:
            s.res.append([s.animeID, response])
            # Get a connection to Redis
            queue = StrictRedis(host='localhost', port=6379)
            # Publish a message to a channel called testing
            message_send = ""
            for i in range(9):
                for j in range(2):
                    message_send += str(s.res[i][j])
                    message_send += ","
            message_send += str(s.res[9][0])
            message_send += ","
            message_send += str(s.res[9][1])

            queue.publish("anime_request", message_send.encode("utf-8"))

            flag = True
            pubsub = StrictRedis(host='localhost', port=6379).pubsub()
            pubsub.subscribe('anime_response')
            # The first message you receive will be a confirmation of subscription
            message = pubsub.get_message()
            while flag:
                # update.message.reply_text('Done')
                # {'pattern': None, 'type': 'subscribe', 'channel': 'testing', 'data': 1L}
                # The subsequent messages are those from the publisher(s)
                message = pubsub.get_message()
                print(message)
                if message and message['data'] != 1:
                    msg = message['data'].decode("utf-8")
                    update.message.reply_text(msg)
                    flag = False

                else:
                    time.sleep(1)


            s.statenum = "handler_rating"
        return


def anime_recommendation(update: Update, context: CallbackContext):
    rand_num = random.randint(1, 7390)
    update.message.reply_text(
        "Please send your rating about the following movie(from 1 to 10) \n" + animeList[rand_num])
    s.statenum = "start_predict"
    s.animeID = rand_num




if __name__ == "__main__":
    # Provide your bot's token
    REQUEST_KWARGS = {
        'proxy_url': 'http://127.0.0.1:7890',
    }
    updater = Updater("5252978559:AAFY4yiCU0aWcICh7gDzBgHCiWevdfYZnc0", use_context=True, request_kwargs=REQUEST_KWARGS)

    s = State()

    animeList = {}
    with open('anime/anime_info.dat', 'r', encoding='utf-8') as file:
        for info in file.readlines():
            line = info.strip()
            context = line.split('	')
            # pass first line
            if context[0] != 'anime_ids':
                anime_id = int(context[0])
                anime_name = context[1]
                animeList[anime_id] = anime_name



updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('Anime_recommendation', anime_recommendation))
updater.dispatcher.add_handler(MessageHandler(Filters.text, handler_rating))
updater.start_polling()
