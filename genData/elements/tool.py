from dataclasses import dataclass, field

import numpy as np

SEED = 2330
RNG_TOOL_NAME = np.random.default_rng(SEED)
RNG_BIAS = np.random.default_rng(SEED)
RNG_VAR = np.random.default_rng(SEED)

@dataclass
class Schema:
    dim: int= 10
    factor_bias: dict[str, float]= field(default_factory=lambda: {"Tool": 8, "Prev1Tool": 4, "Prev2Tool": 2, "ChuckID": 1})

schema = Schema()
LST_SCALE = [1, 1, 150, 150, 150, 150, 15, 15, 15, 15]

def gen_bias(feat, base=0):
    bias = RNG_BIAS.random(size=[schema.dim, 1]) - 0.5
    scale = 1 / np.array(LST_SCALE[:schema.dim]).reshape([schema.dim, -1])
    factor = schema.factor_bias[feat]
    return bias * scale * factor + base

@dataclass
class Tool:
    id: int
    
    name: str=field(init=False)
    bias0: list=field(init=False)
    bias1: list=field(init=False)
    bias2: list=field(init=False)
    
    chuck0: list=field(init=False)
    chuck1: list=field(init=False)
    chuck2: list=field(init=False)
    
    def __post_init__(self):
        self.name = f'Tool-{self.id}'
        self.bias0 = gen_bias(feat="Tool")
        self.bias1 = gen_bias(feat="Prev1Tool")
        self.bias2 = gen_bias(feat="Prev2Tool")
        
        self.chuck0 = gen_bias(feat="Tool")
        self.chuck1 = gen_bias(feat="Prev1Tool")
        self.chuck2 = gen_bias(feat="Prev2Tool")
    
if __name__ == "__main__":
    t = Tool(1)
    print(t)