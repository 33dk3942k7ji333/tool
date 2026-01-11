import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

import polars as pl
from tenacity import AsyncRetrying, RetryCallState, stop_after_attempt, wait_fixed

import mylogger
from my_dao import DataDAO

logger = logging.getLogger(__name__)

DAO_MAX_CONCURRENCY = 5
DAO_MAX_THREAD = 10
DAO_MAX_RETRIES = 3
DAO_TIMEOUT = 300
DAO_DEBUG = False

DAO_SUCCESS = "SUCCESS"
DAO_FAILED = "FAILED"

executor = ThreadPoolExecutor(max_workers=DAO_MAX_THREAD)
sem = asyncio.Semaphore(DAO_MAX_CONCURRENCY)


@dataclass
class TaskResponse:
    status: str
    dao_name: str
    total_time: str
    attempts: int
    resp: str | dict


def error_log(retry_state: RetryCallState):
    exc = retry_state.outcome.exception()  # type: ignore
    task_name = retry_state.args[1]["dao_name"]
    attempt_num = retry_state.attempt_number
    if DAO_DEBUG:
        logger.info(f"[{attempt_num}/{DAO_MAX_RETRIES}] {task_name} Failed: {type(exc).__name__}")


def _retry_error_callback(retry_state: RetryCallState):
    exc = retry_state.outcome.exception()  # type: ignore
    if isinstance(exc, asyncio.TimeoutError):
        error_msg = f"Request Timeout after {retry_state.attempt_number} Attempts"
    else:
        error_msg = str(exc) or "Unknown Error"

    return TaskResponse(
        status=DAO_FAILED,
        dao_name=retry_state.args[1]["dao_name"],
        total_time=f"{retry_state.seconds_since_start:.2f}s",
        attempts=retry_state.attempt_number,
        resp=error_msg,
    )


async def _task_with_retry(
    dao: DataDAO,
    params: dict,
    dao_timeout: float,
    loop: asyncio.AbstractEventLoop,
    start_time: float,
    retrier: AsyncRetrying,
):
    async with sem:
        resp = await asyncio.wait_for(
            loop.run_in_executor(executor, dao.fetch_post_data, params),
            timeout=dao_timeout,
        )

        return TaskResponse(
            status=DAO_SUCCESS,
            dao_name=params["dao_name"],
            total_time=f"{time.monotonic() - start_time:.2f}s",
            attempts=retrier.statistics["attempt_number"],
            resp=resp,
        )


async def task_with_retry(
    dao: DataDAO,
    param: dict,
    dao_timeout: float = DAO_TIMEOUT,
):
    loop = asyncio.get_running_loop()
    start_time = asyncio.get_event_loop().time()
    retrier = AsyncRetrying(
        stop=stop_after_attempt(DAO_MAX_RETRIES),
        wait=wait_fixed(5),
        before_sleep=error_log,
        retry_error_callback=_retry_error_callback,
    )
    return await retrier(_task_with_retry, dao, param, dao_timeout, loop, start_time, retrier)


async def dao_caller_with_async(target_url: str) -> list[TaskResponse]:
    logger.info(f"Start DAO Task with {DAO_MAX_CONCURRENCY} Concurrency and {DAO_MAX_THREAD} Thread")

    dao = DataDAO(target_url)
    task_configs = [
        {"dao_name": 1, "timeout": 3.0},
        {"dao_name": 2, "timeout": 0.1},
        {"dao_name": 3, "timeout": 5.0},
        {"dao_name": 4, "timeout": 5.0},
        {"dao_name": 5, "timeout": 5.0},
        {"dao_name": 6, "timeout": 5.0},
        {"dao_name": 7, "timeout": 5.0},
        {"dao_name": 8, "timeout": 5.0},
        {"dao_name": 9, "timeout": 5.0},
    ]

    tasks = [task_with_retry(dao, cfg) for cfg in task_configs]
    result = await asyncio.gather(*tasks)

    return result


def parse_resp(resp_cont: str):
    return pl.read_csv(
        resp_cont.replace("~|", "\x1f").encode(),
        separator="\x1f",
        skip_rows=0,
    )


if __name__ == "__main__":
    URL = "http://127.0.0.1:8000"
    result = asyncio.run(dao_caller_with_async(URL))

    for res in result:
        print(f"{res.status} - {res.dao_name} - {res.total_time} - {res.attempts}")

    cnt_success = sum([1 for res in result if res.status == DAO_SUCCESS])
    logger.info(f"Success Get {cnt_success} Data")
    lst_df = [parse_resp(res.resp["data"]) for res in result if isinstance(res.resp, dict)]
    df_res = pl.concat(lst_df)
    print(df_res.shape)
