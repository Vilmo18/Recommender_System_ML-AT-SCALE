import numpy as np
from tqdm import tqdm


def transform_df_numpy(data):
    first_two_int = data.iloc[:, :2].select_dtypes(include=np.int64).to_numpy()
    last_two_float = data.iloc[:, -4:].select_dtypes(include=np.float64).to_numpy()
    return np.hstack((first_two_int, last_two_float))


def transform_numpy_dico(data_transform):
    data = transform_df_numpy(data_transform)

    index_twice2 = {}
    index_twice1 = {}

    for entry in data:
        user_id, item_id, rating = entry
        if user_id not in index_twice1:
            index_twice1[user_id] = {}
        index_twice1[user_id][item_id] = rating
        if item_id not in index_twice2:
            index_twice2[item_id] = {}
        index_twice2[item_id][user_id] = rating
    return index_twice1, index_twice2



def mapper_new(index_mapping_user,index_mapping_movie,data_train,data_test):
    u_train,m_train=transform_df_numpy(data_train)
    u_test,m_test=transform_df_numpy(data_test)
    user_train = {}
    for new_index, old_index_dict in enumerate(u_train.values()):
        updated_old_index_dict = {}
        for old_index, value in old_index_dict.items():
            updated_old_index_dict[index_mapping_movie[old_index]] = value
        user_train[new_index] = updated_old_index_dict

    movie_train = {}
    for new_index, old_index_dict in enumerate(m_train.values()):
        updated_old_index_dict = {}
        for old_index, value in old_index_dict.items():
            updated_old_index_dict[index_mapping_user[old_index]] = value
        movie_train[new_index] = updated_old_index_dict
    
    #- -- ----- ------- ---------

    user_test = {}
    for new_index, old_index_dict in enumerate(u_test.values()):
        updated_old_index_dict = {}
        for old_index, value in old_index_dict.items():
            updated_old_index_dict[index_mapping_movie[old_index]] = value
        user_test[new_index] = updated_old_index_dict

    movie_test = {}
    for new_index, old_index_dict in enumerate(m_test.values()):
        updated_old_index_dict = {}
        for old_index, value in old_index_dict.items():
            updated_old_index_dict[index_mapping_user[old_index]] = value
        movie_test[new_index] = updated_old_index_dict

    return  user_train,user_test,movie_train,movie_test



def mapper(data):
    d1, d2 = transform_numpy_dico(data)
    index_mapping_user = {}
    index_mapping_movie = {}

    for i, key in enumerate(d1.keys()):
        index_mapping_user[int(key)] = i
    # print(index_mapping_user)
    for i, key in enumerate(d2.keys()):
        index_mapping_movie[int(key)] = i
    # print(index_mapping_movie)
   
    return index_mapping_user, index_mapping_movie


def transform_dict_tuple(input_dict):
    transformed_dict = {}
    for key, inner_dict in input_dict.items():
        transformed_inner_dict = {(k, v) for k, v in inner_dict.items()}
        transformed_dict[key] = transformed_inner_dict
    return transformed_dict


def dict_to_list(input_dict):
    input_dict = transform_dict_tuple(input_dict)
    max_key = max(input_dict.keys())
    result_list = [None] * (max_key + 1)
    for key, value in tqdm(input_dict.items()):
        result_list[key] = list(value)
    return result_list


def find_true_movie_id(dictionnary, fake_id):
    for key, val in dictionnary.items():
        if val == fake_id:
            return key
    return None
