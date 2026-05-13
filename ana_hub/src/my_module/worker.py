import json
import sys

from my_toolkit.core import Processor


def main():
    # 接收來自 runner.py 的參數（例如 JSON 字串）
    if len(sys.argv) > 1:
        input_data = sys.argv[1]
    else:
        input_data = "Default Task"

    # 初始化 Processor
    proc = Processor()

    # 執行需求：印出版本並處理資料
    proc.print_version()
    result = proc.process(input_data)

    # 將結果輸出到 stdout，讓 runner 可以接收
    print(f"RESULT_START:{result}:RESULT_END")


if __name__ == "__main__":
    main()
