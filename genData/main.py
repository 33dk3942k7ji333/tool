
from itertools import product

import numpy as np
import pandas as pd

from elements.part import Part
from elements.tool import Tool

LST_FEAT = ["Part", "Reticle", "Prev1Reticle", "Tool", "Prev1Tool", "Prev2Tool", "ChuckID"]
rng = np.random.default_rng()
rng_part = np.random.default_rng()
n_protect = 4
thr_ret0 = 20
thr_ret1 = 40

CHUCK_TYPE = {
    0: ["S1", "S2"],
    1: ["BASE"]
}

def gen_data(n_part, n_tool):
    _part_map = [Part(i) for i in range(n_part)]
    _tool_map = [Tool(i) for i in range(n_tool)]
    
    part_map = {part.name: part for part in _part_map}
    tool_map = {tool.name: tool for tool in _tool_map}
    return part_map, tool_map

def _gen_part_data_nums(n_data, n_part, n_protect):
    lst_num = list()
    is_lt_protect = False
    while sum(lst_num) <= n_data or is_lt_protect:
        lst_num = rng.normal(loc=n_data/n_part, scale=n_data/n_part/2, size=n_part)
        lst_num = [int(x)>>1<<1 for x in lst_num]
        is_lt_protect = any([x<n_protect for x in lst_num])
    return lst_num

def gen_part_data_nums(n_data, n_part, n_protect=4):
    idx = 0
    lst_num = _gen_part_data_nums(n_data, n_part, n_protect)

    while sum(lst_num) >= n_data+2:
        if lst_num[idx%n_part] > n_protect:
            lst_num[idx%n_part] -= 2
        idx += 1

    return lst_num


def main(n_data, n_part, n_tool):
    
    part_data_nums = gen_part_data_nums(n_data, n_part, n_protect)
    part_map, tool_map = gen_data(n_part, n_tool)
    
    LST_FEAT = ["Part", "Reticle", "Prev1Reticle", "Tool", "Prev1Tool", "Prev2Tool"]

    lst_comb = []
    for part, data_num in zip(part_map.values(), part_data_nums):
        part_data_num = int(data_num / len(CHUCK_TYPE[part.chuck_type]))
        part_ret0_num = int(np.ceil(part_data_num / thr_ret0))
        part_ret1_num = int(np.ceil(part_data_num / thr_ret1))
        res0 = rng_part.choice(part.ret_name["Reticle"], part_ret0_num)
        res1 = rng_part.choice(part.ret_name["Prev1Reticle"], part_ret1_num)
        print(part.name, part_data_num)
        print(res0)
        print(res1)
        
        
        # lst_tool = list(tool_map.keys())
        # lst_feats = [[part_name], part.ret_name["Reticle"], part.ret_name["Prev1Reticle"], lst_tool[:len], lst_tool[5:], lst_tool[5:], part.chuck_type]
        # lst_comb.extend(list(product(*lst_feats)))

    # df_data = pd.DataFrame(lst_comb, columns=LST_FEAT)

if __name__ == "__main__":
    n_data = 501
    n_part = 4
    n_tool = 12
    
    main(n_data, n_part, n_tool)