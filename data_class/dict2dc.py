from dataclasses import dataclass, make_dataclass

MyDict = {
    "str1": "v1",
    "list2": [1,2,3],
    "dict3": {"d1":1,"d2":2},
    "dict4": [{"d3":3}, {"d4":4}]
}


@dataclass
class MyCFG:
    str1: str
    dict4: list[dict]

def covert_dataclass(dic: dict, dataclassName: str="Config"):
    _type = make_dataclass(dataclassName, [(k,type(v)) for k,v in dic.items()])
    return _type(**{k:v for k,v in dic.items()})

def main():
    
    mdc = covert_dataclass(MyDict)
    print(mdc)
    
    mcfg = MyCFG(**{k:v for k,v in MyDict.items() if k in MyCFG.__dataclass_fields__.keys()})
    print(mcfg)
    

if __name__ == "__main__":
    main()