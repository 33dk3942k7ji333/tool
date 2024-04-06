import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics.pairwise import manhattan_distances, pairwise_distances
import tracemalloc

# %%
df_data = pd.read_csv("./df_data.csv")
feat_list = df_data.columns
feat_list

# %%
le_list = []
df_data_le = pd.DataFrame()
for _feat in feat_list:
    le = LabelEncoder()
    df_data_le[_feat] = le.fit_transform(df_data[_feat])
    le_list.append(le)
    
ohe = OneHotEncoder()
res = ohe.fit_transform(df_data_le).toarray()
res

# %%
def m1(res):
    m1 = manhattan_distances(res, res)
    print(m1/2)

mem_usage = memory_usage(m1(res))

# %%
def m2(df_data):
    res_b = df_data.values
    m2 = pairwise_distances(res_b, res_b, metric="hamming") * res_b.shape[1]
    print(m2)

mem_usage = memory_usage(m2(df_data_le))


