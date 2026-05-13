# 從模組名稱匯入 Processor 與相關工具
from my_toolkit.core import Processor
from my_toolkit.utils import get_system_report


def run_app():
    # 建立實例
    proc = Processor()

    # 呼叫印出版本的功能
    proc.print_version()

    # 執行其他邏輯
    print(get_system_report())
    print(proc.process("Test Task"))


if __name__ == "__main__":
    run_app()
