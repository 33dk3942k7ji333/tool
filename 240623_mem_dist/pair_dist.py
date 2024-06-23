import os
import sys
import math
import time
import datetime
import logging
import itertools
from collections import defaultdict
from functools import wraps
from memory_profiler import profile
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics.pairwise import manhattan_distances, pairwise_distances_chunked

# region Logger
logFilename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-1s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
os.makedirs("./log", exist_ok=True)
fileHandler = logging.FileHandler(f'./log/{logFilename}.log')
fileHandler.setFormatter(logFormatter)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
# endregion Logger

TIME_RECORDER = defaultdict(list)

def func_timer(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        st = time.perf_counter()
        result = func(*args, **kwargs)
        et = time.perf_counter()
        total_time = et-st
        logger.info(f'FUNCTION TIMER - Function [{func.__name__}] Took {total_time:.4f} sec')
        TIME_RECORDER[func.__name__].append(total_time)
        return result
    return func_wrapper

# region Data
@func_timer
def gen_data(part_num: int, tool_num: int, pre1tool_num: int, pre2tool_num: int, save_data=False) -> pd.DataFrame:
    lst_part = [f'Part_{i}' for i in range(1, part_num+1)]
    lst_ret = [f'Ret_{i}' for i in range(1, part_num+1)]
    lst_pre1ret = [f'Pre1Ret_{i}' for i in range(1, part_num+1)]
    lst_tool = [f'Tool_{i}' for i in range(1, tool_num+1)]
    lst_pre1tool = [f'Pre1Tool_{i}' for i in range(1, pre1tool_num+1)]
    lst_pre2tool = [f'Pre2Tool_{i}' for i in range(1, pre2tool_num+1)]
    feat_lst = ["Part", "Reticle", "Prev1Reticle", "Tool", "Prev1Tool", "Prev2Tool"]
    
    df_data = pd.DataFrame(columns=feat_lst)
    for idx,_ in enumerate(lst_part):
        _slice = slice(idx,idx+1)
        _part_lst_comb = [lst_part[_slice], lst_ret[_slice], lst_pre1ret[_slice], lst_tool, lst_pre1tool, lst_pre2tool]
        _part_df_data = pd.DataFrame([i for i in itertools.product(*_part_lst_comb)], columns=feat_lst)
        df_data = pd.concat([df_data, _part_df_data])
    df_data = df_data.reset_index(drop=True)
    if save_data:
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
# endregion Data


# region Distance Matrix
def get_max_batch(num, batch_size):
    return math.ceil(num/batch_size)

@func_timer
def manhattan(X, Y):
    dist_mat = manhattan_distances(X, Y) / 2
    return dist_mat
    # return dist_mat.astype(np.uint8)
    
@func_timer
def hamming(X, Y):
    out = np.empty((X.shape[0], Y.shape[0]), dtype=np.uint8)
    col = 0
    for _m in pairwise_distances_chunked(X, Y, metric="hamming"):
        out[col:col+len(_m)] = (_m * X.shape[1])
        col += len(_m)
    return out

@profile
@func_timer
def manhattan_method(onehot_data, batch_size, once=True):
    known_comb = onehot_data[:2500, :]
    unknown_comb = onehot_data[2500:2500+batch_size*5, :] if once else onehot_data[2500:, :]
    
    for i in range(get_max_batch(unknown_comb.shape[0], batch_size)):
        st = i * batch_size
        et = (i+1) * batch_size if (i+1) * batch_size < unknown_comb.shape[0] else unknown_comb.shape[0]
        batch_unknown_comb = unknown_comb[st:et, :]
        logger.info(f'Batch {i}: {st}~{et}')
        dist_mat = manhattan(batch_unknown_comb, known_comb)
        # logger.info(dist_mat)

@profile
@func_timer
def hamming_method(df_data_le, batch_size, once=True):
    known_comb = df_data_le.iloc[:2500, :]
    unknown_comb = df_data_le.iloc[2500:2500+batch_size*5, :] if once else df_data_le.iloc[2500:, :]

    for i in range(get_max_batch(unknown_comb.shape[0], batch_size)):
        st = i * batch_size
        et = (i+1) * batch_size if (i+1) * batch_size < unknown_comb.shape[0] else unknown_comb.shape[0]
        batch_unknown_data = unknown_comb.iloc[st:et,:]
        logger.info(f'Batch {i}: {st}~{et}')
        dist_mat = hamming(batch_unknown_data, known_comb)
        # logger.info(dist_mat)
# endregion Distance Matrix


def main():
    df_data = gen_data(part_num=10, tool_num=20, pre1tool_num=20, pre2tool_num=30)
    BATCH_SIZE = 200_000
    while df_data.shape[0] < 6_000_000:
        df_data = pd.concat([df_data, df_data])
    df_data = df_data.iloc[:6000000,:]
    logger.info(f'Gen Data Shape: {df_data.shape}')
    logger.info(f'Feature: {list(df_data.columns)}')
    
    df_data_le,_ = label_encode_data(df_data, df_data.columns)
    onehot_data = onehot_encode_data(df_data_le)
    logger.info(f'df_data_le Shape: {df_data_le.shape}')
    logger.info(f'onehot_data Shape: {onehot_data.shape}')
    
    manhattan_method(onehot_data, BATCH_SIZE, once=True)
    
    time.sleep(7)
    
    hamming_method(df_data_le, BATCH_SIZE, once=True)

    logger.info(f'===== Cost Time =====')
    for _func, lst_time in TIME_RECORDER.items():
        for _id,_time in enumerate(lst_time):
            logger.info(f'Function [{_func}], Batch: {_id} cost {_time:.4f}')
        if _func == "manhattan":
            logger.info(f'Avg. [{sum(lst_time[1:4])/3:.4f}]')
        if _func == "hamming":
            logger.info(f'Avg. [{sum(lst_time[1:4])/3:.4f}]')

if __name__ == "__main__":
    main()