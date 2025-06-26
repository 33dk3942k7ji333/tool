import hashlib
import math
from pathlib import Path

DEFAULT_PART_SIZE = 5 * 1024 * 1024


def calculate_minio_etag_from_local(
    local_file_path: str,
    part_size: int = DEFAULT_PART_SIZE,
):
    file_size = Path(local_file_path).stat().st_size

    if file_size <= part_size:
        with open(local_file_path, "rb") as f:
            md5_hash = hashlib.md5(f.read())
        return md5_hash.hexdigest()
    else:
        part_md5s = []
        with open(local_file_path, "rb") as f:
            while True:
                chunk = f.read(part_size)
                if not chunk:
                    break
                part_md5s.append(hashlib.md5(chunk).digest())

        concatenated_md5s = b"".join(part_md5s)
        final_md5 = hashlib.md5(concatenated_md5s).hexdigest()
        return f"{final_md5}-{len(part_md5s)}"


def calculate_minio_etag(
    data_bytes: bytes,
    part_size: int = DEFAULT_PART_SIZE,
):
    file_size = len(data_bytes)

    if file_size <= part_size:
        return hashlib.md5(data_bytes).hexdigest()
    else:
        num_parts = math.ceil(file_size / part_size)
        part_md5s = []
        for i in range(num_parts):
            start = i * part_size
            end = min((i + 1) * part_size, file_size)
            part_data = data_bytes[start:end]
            part_md5s.append(hashlib.md5(part_data).digest())

        concatenated_md5s = b"".join(part_md5s)
        final_md5 = hashlib.md5(concatenated_md5s).hexdigest()
        return f"{final_md5}-{len(part_md5s)}"
