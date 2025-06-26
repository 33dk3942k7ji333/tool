import logging
import os
import random
import re
import string
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UNITS = {
    "B": 1,
    "KB": 1024,
    "MB": 1024**2,
    "GB": 1024**3,
}

FAILED = "FAILED"
CHUCK_SIZE = 5 * 1024 * 1024

CHARS_TO_USE = string.ascii_letters + string.digits


def parse_size(str_size: str):
    """
    Parses a size string with units (KB, MB, GB) into an integer number of bytes.\\
    Example: "10MB" -> 10485760
    """
    _str_size = str_size.upper().strip()
    match = re.match(r"^(\d+(\.\d+)?)\s*(B|KB|MB|GB)?$", _str_size)

    if not match:
        raise ValueError(f"Cannot parse size format: '{str_size}'")

    num_size, _, unit = match.groups()
    result = int(float(num_size) * UNITS.get(unit, 1))
    logger.debug(f"Parse [{str_size}] to [{result}]")

    return result


def generate_bin_file(filepath: str, str_size: str):
    """
    Generates a random bin file of a specified size.

    :param filepath: The output file path.
    :param str_size: The file size, e.g., "2KB", "3MB", "30GB".
    """

    _filepath = Path(filepath)
    try:
        target_bytes = parse_size(str_size)
    except ValueError as e:
        logger.error(f"Error: {e}", exc_info=True)
        return FAILED

    logger.info(f"Generate File : {_filepath}")
    logger.info(f"Target Size   : {target_bytes / 1024**2:.2f} MB ({target_bytes} bytes)")

    try:
        with _filepath.open("wb") as f:
            written_bytes = 0
            while written_bytes < target_bytes:
                bytes_to_write = min(CHUCK_SIZE, target_bytes - written_bytes)
                f.write(os.urandom(bytes_to_write))
                written_bytes += bytes_to_write
        logger.info(f"File Generated: {_filepath} (Actual size: {_filepath.stat().st_size} bytes)")
    except IOError as e:
        logger.error(f"An I/O error occurred: {e}", exc_info=True)


def generate_txt_file(filepath: str, str_size: str):
    """
    Generates a random txt file of a specified size.\\
    Note: The final size may vary due to encoding.

    :param filepath: The output file path.
    :param str_size: The file size, e.g., "2KB", "3MB", "30GB".
    """

    _filepath = Path(filepath)
    try:
        target_bytes = parse_size(str_size)
    except ValueError as e:
        logger.error(f"Error: {e}", exc_info=True)
        return FAILED

    logger.info(f"Generate File : {_filepath}")
    logger.info(f"Target Size   : {target_bytes / 1024**2:.2f} MB ({target_bytes} characters)")

    try:
        with _filepath.open("w", encoding="utf-8") as f:
            written_chars = 0
            max_chunk_size = min(int(target_bytes ** (1 / 2)), 4096)
            while written_chars < target_bytes:
                chunk_size = random.randint(0, max_chunk_size)
                chars_to_write = min(chunk_size, target_bytes - written_chars)
                chunk = "".join(random.choices(list(CHARS_TO_USE), k=chars_to_write))

                if target_bytes - (written_chars + chars_to_write) > 2:
                    chunk += "\n"
                    chars_to_write += 2

                f.write(chunk)
                written_chars += chars_to_write

        logger.info(f"File Generated: {_filepath} (Actual size: {_filepath.stat().st_size} bytes)")
    except IOError as e:
        logger.error(f"An I/O error occurred: {e}", exc_info=True)


def generate_csv_file(filepath: str, str_size: str, max_col: int = 40):
    """
    Generates a random csv file of a specified size.\\
    Note: The final size may vary due to encoding.

    :param filepath: The output file path.
    :param str_size: The file size, e.g., "2KB", "3MB", "30GB".
    :param max_col: Maximum number of columns.
    """

    def _gen_cell_str(length: int):
        chars = string.ascii_lowercase + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    _filepath = Path(filepath)
    try:
        target_bytes = parse_size(str_size)
    except ValueError as e:
        logger.error(f"Error: {e}", exc_info=True)
        return FAILED

    logger.info(f"Generate File : {_filepath}")
    logger.info(f"Target Size   : {target_bytes / 1024**2:.2f} MB ({target_bytes} characters)")

    try:
        with _filepath.open("w", encoding="utf-8") as f:
            num_columns = min(int(target_bytes ** (1 / 2)), max_col)
            headers = [f"col_{i}" for i in range(1, num_columns + 1)]
            header = ",".join(headers) + "\n"
            f.write(header)
            written_chars = len(header)
            while written_chars < target_bytes:
                row_data = ",".join([_gen_cell_str(1) * 8 for _ in headers]) + "\n"
                f.write(row_data)
                written_chars += len(row_data)

        logger.info(f"File Generated: {_filepath} (Actual size: {_filepath.stat().st_size} bytes)")
    except IOError as e:
        logger.error(f"An I/O error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    output_dir = "./test_data"
    Path(output_dir).mkdir(exist_ok=True)

    generate_bin_file(f"{output_dir}/sample.bin", "2MB")
    generate_txt_file(f"{output_dir}/sample.txt", "3MB")
    generate_csv_file(f"{output_dir}/sample.csv", "30MB")
