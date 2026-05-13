import os
import subprocess
import sys


def execute_version(version_tag, task_name):
    """
    透過 Popen 啟動 worker.py，並注入指定版本的 libs 路徑
    """
    # 定義路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))

    # 指向 worker.py 的路徑
    worker_script = os.path.join(current_dir, "worker.py")

    # 指向對應版本的庫目錄 (例如: /libs/v1)
    lib_path = os.path.join(project_root, "libs", version_tag, "my_toolkit", "src")

    # 關鍵：設定環境變數
    env = os.environ.copy()
    # 將特定版本的庫路徑放在 PYTHONPATH 的最前面
    env["PYTHONPATH"] = lib_path + os.pathsep + env.get("PYTHONPATH", "")

    print(f"\n>>> [Runner] 正在啟動版本 {version_tag} 處理任務: {task_name}")

    # 使用 Popen 執行
    process = subprocess.Popen(
        [sys.executable, worker_script, task_name],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout, stderr = process.communicate()

    if process.returncode == 0:
        # 從 stdout 解析出 worker 的處理結果
        print(f"[Runner] 執行成功。子程序輸出：\n{stdout.strip()}")
    else:
        print(f"[Runner] 執行失敗。錯誤訊息：\n{stderr}")


if __name__ == "__main__":
    # 同時測試呼叫兩個不同版本的模組
    execute_version("v1", "Legacy_Data_Stream")
    execute_version("v2", "High_Speed_Data_Stream")
