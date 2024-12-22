import pandas as pd
from itertools import product
from memory_profiler import profile
import time

NUM_F1 = 50
NUM_F2 = 20
NUM_F3 = 20
NUM_F4 = 50
NUM_F5 = 50

lst_f1 = list(range(0, NUM_F1))
lst_f2 = list(range(0, NUM_F2))
lst_f3 = list(range(0, NUM_F3))
lst_f4 = list(range(0, NUM_F4))
lst_f5 = list(range(0, NUM_F5))

@profile
def method1_all():
    st = time.time()
    lst_comb = list()
    for _f1 in lst_f1:
        lst_feat = [[_f1], lst_f2, lst_f3, lst_f4, lst_f5]
        lst_comb.extend(list(product(*lst_feat)))
    df_data = pd.DataFrame(lst_comb)
    print(f"method 1 use {time.time() - st:5.2f}")

@profile
def method2_split():
    st = time.time()
    lst_df = list()
    for _f1 in lst_f1:
        lst_feat = [[_f1], lst_f2, lst_f3, lst_f4, lst_f5]
        lst_df.append(pd.DataFrame(list(product(*lst_feat))))
    df_data = pd.concat(lst_df)
    print(f"method 2 use {time.time() - st:5.2f}")
    
def main():
    method1_all()
    time.sleep(2)
    
    method2_split()
    time.sleep(2)

if __name__ == "__main__":
    main()
    # mprof run .\test_pandas_iter.py
    # mprof plot