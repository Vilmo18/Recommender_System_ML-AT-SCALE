import numpy as np


def loss_cost(
    users_map, users_vector, movies_vector, item_biases, user_biases, lamb, tau, gamma
):
    loss = 0
    M = len(users_map)
    for m in range(M):
        for n, r in users_map[m]:
            loss += (
                r
                - np.dot(users_vector[m], movies_vector.T[n])
                - item_biases[n]
                - user_biases[m]
            ) ** 2
    loss *= lamb
    loss += (
        gamma * (np.sum(item_biases) ** 2)
        + gamma * np.sum((user_biases) ** 2)
        + tau * (np.linalg.norm(users_vector, "fro") ** 2)
        + tau * (np.linalg.norm(movies_vector, "fro") ** 2)
    )
    loss = loss / 2
    return loss


def rmse(users_map, users_vector, movies_vector):
    rms = 0
    count = 0
    M = len(users_map)
    for m in range(M):
        for n, r in users_map[m]:
            rms += (r - np.dot(users_vector[m], movies_vector.T[n])) ** 2
            count += 1
    result = np.sqrt(rms / count)
    return result
