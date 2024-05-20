import numpy as np
from utils import *


def generate_user_vector(
    users_predict,
    movies_vector,
    item_biases,
    lamb=5,
    tau=0.4,
    gamma=2e-1,
    iteration=1500,
    k=10,
):
    user_new = np.random.normal(0, 1 / np.sqrt(k), (k))
    user_bias_new = 0
    for _ in range(iteration):
        biais = 0
        item_counter = 0
        for n, r in users_predict:
            biais += r - np.dot(user_new, movies_vector.T[n]) - item_biases[n]
            item_counter += 1
        biais *= lamb
        biais = biais / (lamb * item_counter + gamma)
        user_bias_new = biais
        left_val = 0
        right_val = 0
        for n, r in users_predict:
            left_val += movies_vector.T[n] * movies_vector.T[n].reshape(-1, 1)
            right_val += movies_vector.T[n] * (r - user_bias_new - item_biases[n])
        left_val *= lamb
        user_new = np.linalg.solve(left_val + tau * np.eye(k), lamb * right_val)
    return user_new, user_bias_new


def prediction(
    user_new, user_bias_new, movies_vector, item_biases, dico, occurrences, fact=1
):
    def movie_ids_less_than_k_occurrences(occurences, rate=50):
        less_than_30_occurrences = occurrences[occurrences["occurrences"] < rate][
            "movieId"
        ].tolist()
        return less_than_30_occurrences

    n = movies_vector.shape[1]
    predict = []
    for i in range(n):
        predict.append(
            np.dot(user_new, movies_vector.T[i]) + fact * item_biases[i] + user_bias_new
        )
    recommender = np.argsort(predict)[::-1]
    recommender = recommender[:700]
    rec = []
    less_than_k_occurrences_ids = movie_ids_less_than_k_occurrences(
        occurrences, rate=130
    )
    for i in recommender:
        key = find_key_by_values(dico, i)
        if key not in less_than_k_occurrences_ids:
            rec.append(key)
    return rec
