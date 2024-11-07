from dataclasses import dataclass, field

import numpy as np

SEED = 2330
RNG_PART_NAME = np.random.default_rng(SEED)
RNG_BIAS = np.random.default_rng(SEED)
RNG_VAR = np.random.default_rng(SEED)

@dataclass
class Schema:
    lst_layer: list[str]= field(default_factory=lambda: ["Reticle", "Prev1Reticle", "Prev2Reticle"])
    lst_layer_name: list[str]= field(default_factory=lambda: ["97A", "98A", "99A"])
    num_reticle: list[int]= field(default_factory=lambda: [10, 10, 10])
    chuck_type: int= 0
    dim: int= 10
    factor_bias: dict[str, float]= field(default_factory=lambda: {"Part": 1, "Reticle": 0.5, "Prev1Reticle": 0.1, "Prev2Reticle": 0})

schema = Schema()
LST_SCALE = [1, 1, 150, 150, 150, 150, 15, 15, 15, 15]


def gen_bias(feat, base=0):
    bias = RNG_BIAS.random(size=[schema.dim, 1]) - 0.5
    scale = 1 / np.array(LST_SCALE[:schema.dim]).reshape([schema.dim, -1])
    factor = schema.factor_bias[feat]
    return bias * scale * factor + base

def gen_ret_names(part_name, layer_name, num):
    return [f'{part_name[2:6]}{layer_name}-{i}' for i in range(1, num+1)]

def gen_part_name():
    prefix = "TM"
    get_chr = lambda: chr(RNG_PART_NAME.integers(65,91))
    suffix = f'{RNG_PART_NAME.integers(0, 100):02d}'
    return prefix + get_chr() + get_chr() + suffix

@dataclass
class Part:
    id: int
    name: str=field(init=False)
    
    ret_name: dict=field(init=False)
    ret_bias: dict=field(init=False)
    
    chuck_type: list=field(init=False)
    
    def __post_init__(self):
        self.name = gen_part_name()
        self.bias = gen_bias(feat="Part")
        
        self.ret_name = dict()
        self.ret_bias = dict()
        for layer, layer_name, num_reticle in zip(schema.lst_layer, schema.lst_layer_name, schema.num_reticle):
            ret_names = gen_ret_names(self.name, layer_name, num_reticle)
            self.ret_name[layer] = ret_names
            
            for ret_name in ret_names:
                self.ret_bias[ret_name] = gen_bias(feat=layer, base=self.bias)

        self.chuck_type = schema.chuck_type
    
if __name__ == "__main__":
    p = Part(1)
    print(p)