import time

import pandas as pd

from etag import calculate_minio_etag_from_local
from gen_test_file import generate_bin_file, generate_csv_file, generate_txt_file


def test_func_time(func, parameters, file_name):
    lst_size = []
    lst_time = []

    for param_n in parameters:
        print(f"Testing :{param_n}")
        func(file_name, str(param_n) + "MB")
        start_time = time.perf_counter()
        calculate_minio_etag_from_local(file_name)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        lst_size.append(param_n)
        lst_time.append(elapsed_time)

    result = {
        "": lst_size,
        "Used_Time": lst_time,
    }

    return pd.DataFrame(result)


if __name__ == "__main__":
    test_parameters = [2 ** (i) for i in range(13)]

    function_to_test = generate_bin_file
    output_csv_file = "./test_data/sample.bin"
    df_result = test_func_time(function_to_test, test_parameters, output_csv_file)
    df_result.to_csv("bin.csv", index=False)

    function_to_test = generate_txt_file
    output_csv_file = "./test_data/sample.txt"
    df_result = test_func_time(function_to_test, test_parameters, output_csv_file)
    df_result.to_csv("txt.csv", index=False)

    function_to_test = generate_csv_file
    output_csv_file = "./test_data/sample.csv"
    df_result = test_func_time(function_to_test, test_parameters, output_csv_file)
    df_result.to_csv("csv.csv", index=False)
