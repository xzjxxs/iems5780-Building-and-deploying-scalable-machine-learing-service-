# Assignment4_1155161089_XUZijun
# Training a recommender system using Surprise
import os
from collections import defaultdict

import pandas as pd
from surprise import Dataset, dump
from surprise import Reader
from surprise import SVD
from surprise.model_selection import cross_validate

# Read the data
ratings_data = pd.read_csv('anime/anime_ratings.dat', delimiter="\t")
info_data = pd.read_csv('anime/anime_info.dat', delimiter="\t")
history_data = pd.read_csv('anime/anime_history.dat', delimiter="\t")

# Use the first 4000 users as 5-fold cross validation, and leave the last 1000 users as a testing set.
train_set, test_set = ratings_data[ratings_data["User_ID"] <= 4000], ratings_data[ratings_data["User_ID"] > 4000]

reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(ratings_data[['User_ID', 'Anime_ID', 'Feedback']], reader)
train_data = Dataset.load_from_df(train_set[['User_ID', 'Anime_ID', 'Feedback']], reader)
test_data = Dataset.load_from_df(test_set[['User_ID', 'Anime_ID', 'Feedback']], reader)

# Use the famous SVD algorithm.
algo = SVD()

# Run 5-fold cross-validation and print results.
cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# Generate a SVD model using all training data, and save the model as anime_model.pickle using dump.
algo.fit(train_data.build_full_trainset())
dump.dump(os.path.expanduser("anime_model.pickle"), algo=algo, verbose=1)


def get_top_n_accuracy(predictions, n=10):
    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, true_r, float("%.1f" % round(est))))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[2], reverse=True)
        top_n[uid] = user_ratings[:n]

    # Compute accuracy based on the testing set using top-10 predictions.
    count = 0
    for uid, user_ratings in top_n.items():
        for i in user_ratings:
            if i[1] != i[2]:
                count += 1

    accuracy = 1 - count / 10000

    return accuracy


# Compute accuracy based on the testing set using top-10 predictions.
model_predictions = algo.test(test_data.build_full_trainset().build_testset())
print("Accuracy is ")
print(get_top_n_accuracy(model_predictions, n=10))
