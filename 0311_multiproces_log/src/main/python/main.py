import concurrent.futures
import logging
import os
import multiprocessing
import time
import kernel

from proj_logger import setup_logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("main.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger.addHandler(file_handler)
file_handler.setFormatter(formatter)


def process_task(element):
    """
    A task function that creates a process-specific logger.
    """
    setup_logger(element)
    process_name = element  # Use the element as the process name
    # log_file = f"process_{process_name}.log"

    # logger = logging.getLogger(process_name)  # Logger name is process name
    # logger.setLevel(logging.INFO)

    # file_handler = logging.FileHandler(log_file)
    # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    logger.info(f"Process {process_name} started.")

    # Simulate some work
    kernel.foo(process_name)

    logger.info(f"Process {process_name} completed.")

    return f"Process {process_name} completed."


if __name__ == "__main__":
    task_list = ["a", "b", "c"]
    logger.info(f"Task list: {task_list}")

    with concurrent.futures.ProcessPoolExecutor(max_workers=len(task_list)) as executor:
        futures = {executor.submit(process_task, element): element for element in task_list}

        results = []
        for future in concurrent.futures.as_completed(futures):
            element = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(result)
            except Exception as exc:
                print(f"Process {element} generated an exception: {exc}")

    print("Log files created:")
    for filename in os.listdir("."):
        if filename.startswith("process_") and filename.endswith(".log"):
            print(filename)
