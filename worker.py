# Assignment4_1155161089_XUZijun
# Deploying the Model as some worker programs

import heapq
import time
from collections import defaultdict
from operator import itemgetter

import pandas as pd
from redis import StrictRedis
from celery import Celery

# Create a Celery app, providing a name and the URL to the message broker
from surprise import Reader, Dataset, dump

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')


# Create a task using the app.task decorator
@app.task
def subscribe():
    def get_name(anime_id):
        if int(anime_id) in animeList:
            return animeList[int(anime_id)]
        else:
            return ""

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

    _, model = dump.load('anime_model.pickle')
    reader = Reader(rating_scale=(1, 10))
    anime_ratings = pd.read_table('anime/anime_ratings.dat')
    dataset = Dataset.load_from_df(anime_ratings[['User_ID', 'Anime_ID', 'Feedback']], reader)
    trainset = dataset.build_full_trainset()
    similarity_matrix = model.fit(trainset).compute_similarities()

    # Receive the user input rating
    pubsub = StrictRedis(host='localhost', port=6379).pubsub()
    pubsub.subscribe('anime_request')
    while True:
        message = pubsub.get_message()
        if message and message['data'] != 1:
            print(message)
            # predict
            arr_str = message['data'].decode("utf-8")
            arr = arr_str.split(",")
            index = 0
            output = []
            for i in range(10):
                sub_res = []
                sub_res.append(int(arr[index]))
                sub_res.append(int(arr[index + 1]))
                output.append(sub_res)
                index = index + 2
            print(output)
            k_neighbors = heapq.nlargest(10, output, key=lambda t: t[1])
            candidates = defaultdict(float)

            for itemID, rating in k_neighbors:
                try:
                    similaritities = similarity_matrix[itemID]
                    for innerID, score in enumerate(similaritities):
                        candidates[innerID] += score * (rating / 5.0)
                except:
                    continue
            recommendations = []

            position = 0
            reply = "Top 10 recommended anime for you:"
            reply += '\n'
            for itemID, rating_sum in sorted(candidates.items(), key=itemgetter(1), reverse=True):

                recommendations.append(get_name(trainset.to_raw_iid(itemID)))
                position += 1
                if position > 9:
                    break
            id = 1
            for rec in recommendations:
                reply += str(id)
                reply += "."
                reply += rec
                reply += '\n'
                id = id + 1

            # Publish the recommendation result
            queue = StrictRedis(host='localhost', port=6379)
            # Publish a message to a channel called testing
            print(reply)
            queue.publish("anime_response", reply.encode("utf-8"))
        else:
            time.sleep(1)


subscribe.delay()
