import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics.pairwise import manhattan_distances, pairwise_distances, pairwise_distances_chunked



df_data = pd.read_csv("./df_data.csv")
feat_list = df_data.columns
BATCH_SIZE = 10000000
feat_list


le_list = []
df_data_le = pd.DataFrame()
for _feat in feat_list:
    le = LabelEncoder()
    df_data_le[_feat] = le.fit_transform(df_data[_feat])
    le_list.append(le)
    
ohe = OneHotEncoder()
res = ohe.fit_transform(df_data_le).toarray()
res.shape


res = res.astype("uint8")
res


known_comb = res[:2500,:]
unknown_comb = res[2500:BATCH_SIZE*2,:]


known_data = df_data_le.iloc[:2500, :]
unknown_data = df_data_le.iloc[2500:BATCH_SIZE*2, :]

def get_max_batch(num, batch_size):
    return math.ceil(num/batch_size)

def m1(res1, res2):
    out1 = manhattan_distances(res1, res2) / 2
    return out1.astype("uint8")


# for i in range(get_max_batch(unknown_comb.shape[0], BATCH_SIZE)):
#     st = i * BATCH_SIZE
#     et = (i+1) * BATCH_SIZE if (i+1) * BATCH_SIZE < res.shape[0] else res.shape[0]
#     batch_unknown_comb = unknown_comb[st:et,:]
#     print(f'{st}~{et}')
#     out1 = m1(batch_unknown_comb, known_comb)
#     print(out1)
    
    
def m2c(res1, res2):
    out = np.empty((res1.shape[0], res2.shape[0]), dtype="uint8")
    col = 0
    for _m in pairwise_distances_chunked(res1, res2, metric="hamming"):
        out[col:col+len(_m)] = (_m * res1.shape[1])
        col += len(_m)
    return out.astype("uint8")



known_data = df_data_le.iloc[:2500, :]
unknown_data = df_data_le.iloc[2500:, :]


for i in range(get_max_batch(unknown_data.shape[0], BATCH_SIZE)):
    st = i * BATCH_SIZE
    et = (i+1) * BATCH_SIZE if (i+1) * BATCH_SIZE < unknown_data.shape[0] else unknown_data.shape[0]
    batch_unknown_data = unknown_data.iloc[st:et,:]
    print(f'{st}~{et}')
    out2c = m2c(batch_unknown_data, known_data)
    print(out2c)