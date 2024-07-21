import os
import random
import pathlib
import pandas as pd

NUM_PART = 20
NUM_TOOL = 20
NUM_PRE1 = 20

LST_FEAT = ["Part", "Tool", "Prev1Tool"]
LST_VALUE = ["value\n1", "value\n2", "value\n3"]
LST_RATIO = [[0.9, 0.5, 0.5], [0.1, 0.3, 0.2], [0.001, 0.0015, 0.002]]
_concat = lambda x: "_".join(x)

def create_data(num: int):
    dic_res, dic_value = dict(), dict()
    lst_part = [f"Part_{_num}" for _num in range(1, 1+NUM_PART)]
    lst_tool = [f"Tool_{_num}" for _num in range(1, 1+NUM_TOOL)]
    lst_pre1tool = [f"Pre1Tool_{_num}" for _num in range(1, 1+NUM_PRE1)]
    
    dic_res["Part"] = random.choices(lst_part, k=num)
    dic_res["Tool"] = random.choices(lst_tool, k=num)
    dic_res["Prev1Tool"] = random.choices(lst_pre1tool, k=num)
    
    for part in lst_part:
        dic_value[part] = random.randint(-10,10)
    for tool in lst_tool:
        dic_value[tool] = random.randint(-5,5)
    for pre1tool in lst_pre1tool:
        dic_value[pre1tool] = random.randint(-2,2)
    pd.DataFrame.from_dict(dic_value, orient='index').to_csv(f'./value_mapping_table_{num}.csv')
    
    return pd.DataFrame(dic_res), dic_value

def cal_value(df: pd.DataFrame, dic_value: dict) -> tuple[float, float]:
    value1: float = 0
    value2: float = 0
    value3: float = 0
    for idx, feat in enumerate(LST_FEAT):
        value1 += LST_RATIO[0][idx]*dic_value[df[feat]]
        value2 += LST_RATIO[1][idx]*dic_value[df[feat]]
        value3 += LST_RATIO[2][idx]*dic_value[df[feat]]
    return value1, value2, value3

def save_csv(df: pd.DataFrame, chuck_size: int, folder_name: str):
    os.makedirs(folder_name, exist_ok=True)
    idx = 0
    chuck_idx = 0
    while idx < df.shape[0]:
        df.iloc[idx: idx+chuck_size].to_csv(f'{pathlib.Path(folder_name)}/runtable_{chuck_idx}.csv', index=False)
        idx += chuck_size
        chuck_idx += 1

def gen_data(num: int= 100, chunk_size: int= 1000, folder_name: str= "."):
    df_data, dic_value = create_data(num)
    df_data[LST_VALUE[0]], df_data[LST_VALUE[1]], df_data[LST_VALUE[2]] = zip(*df_data.apply(cal_value, args=(dic_value,), axis=1))    
    # df_data["comb"] = df_data[LST_FEAT].apply(_concat, axis=1)
    save_csv(df_data, chunk_size, folder_name)