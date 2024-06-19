import math
import time
import itertools
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics.pairwise import manhattan_distances, pairwise_distances_chunked
from memory_profiler import profile

# region data
def gen_data(part_num: int, ret_num: int, tool_num: int, pre1tool_num: int, pre2tool_num: int, chuck_num: int) -> pd.DataFrame:
    lst_part = [f'Part_{i}' for i in range(1, part_num)]
    lst_ret = [f'Ret_{i}' for i in range(1, ret_num)]
    lst_tool = [f'Tool_{i}' for i in range(1, tool_num)]
    lst_pre1 = [f'Pre1Tool_{i}' for i in range(1, pre1tool_num)]
    lst_pre2 = [f'Pre2Tool_{i}' for i in range(1, pre2tool_num)]
    lst_chuck = [f'Chuck_{i}' for i in range(1, chuck_num)]
    
    lst_comb = [lst_part, lst_ret, lst_tool, lst_pre1, lst_pre2, lst_chuck]
    feat_lst = ["Part", "Reticle", "Tool", "Prev1Tool", "Prev2Tool", "ChuckID"]
    df_data = pd.DataFrame([i for i in itertools.product(*lst_comb)], columns=feat_lst)
    df_data.to_csv("./df_data.csv", index=False)
    return df_data

def label_encode_data(df_data: pd.DataFrame, lst_feat: list):
    lst_label_encoder = []
    df_data_le = pd.DataFrame()
    
    for feat in lst_feat:
        label_encoder = LabelEncoder()
        df_data_le[feat] = label_encoder.fit_transform(df_data[feat])
        lst_label_encoder.append(label_encoder)
        
    return df_data_le, lst_label_encoder

def onehot_encode_data(df_data_le: pd.DataFrame) -> np.ndarray:
    ohe = OneHotEncoder()
    res = ohe.fit_transform(df_data_le).toarray()
    return res
# endregion data


# region distance matrix
def get_max_batch(num, batch_size):
    return math.ceil(num/batch_size)

def manhattan(X, Y):
    dist_mat = manhattan_distances(X, Y) / 2
    return dist_mat

@profile
def manhattan_method(onehot_data, batch_size, once=True):
    known_comb = onehot_data[:2500, :]
    unknown_comb = onehot_data[2500:2500+batch_size, :] if once else onehot_data[2500:, :]
    
    for i in range(get_max_batch(unknown_comb.shape[0], batch_size)):
        st = i * batch_size
        et = (i+1) * batch_size if (i+1) * batch_size < unknown_comb.shape[0] else unknown_comb.shape[0]
        batch_unknown_comb = unknown_comb[st:et, :]
        print(f'{st}~{et}')
        dist_mat = manhattan(batch_unknown_comb, known_comb)
        print(dist_mat)

def hamming(X, Y):
    out = np.empty((X.shape[0], Y.shape[0]), dtype=np.uint8)
    col = 0
    for _m in pairwise_distances_chunked(X, Y, metric="hamming"):
        out[col:col+len(_m)] = (_m * X.shape[1])
        col += len(_m)
    return out

@profile
def hamming_method(df_data_le, batch_size, once=True):
    known_comb = df_data_le.iloc[:2500, :]
    unknown_comb = df_data_le.iloc[2500:2500+batch_size, :] if once else df_data_le.iloc[2500:, :]

    for i in range(get_max_batch(unknown_comb.shape[0], batch_size)):
        st = i * batch_size
        et = (i+1) * batch_size if (i+1) * batch_size < unknown_comb.shape[0] else unknown_comb.shape[0]
        batch_unknown_data = unknown_comb.iloc[st:et,:]
        print(f'{st}~{et}')
        dist_mat = hamming(batch_unknown_data, known_comb)
        print(dist_mat)
# endregion distance matrix


def main():
    df_data = gen_data(part_num=40, ret_num=20, tool_num=20, pre1tool_num=20, pre2tool_num=20, chuck_num=2)
    lst_feat = df_data.columns
    print(f'Gen Data Shape: {df_data.shape}')
    print(f'Feature: {lst_feat}')
    
    BATCH_SIZE = 200000
    df_data_le,_ = label_encode_data(df_data, lst_feat)
    onehot_data = onehot_encode_data(df_data_le)
    
    print(f'df_data_le Shape: {df_data_le.shape}')
    print(f'onehot_data Shape: {onehot_data.shape}')
    
    manhattan_method(onehot_data, BATCH_SIZE, False)
    
    time.sleep(20)
    
    hamming_method(df_data_le, BATCH_SIZE, False)



if __name__ == "__main__":
    main()