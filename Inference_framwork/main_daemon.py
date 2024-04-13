import threading
import time
import random
import queue
import math
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

logger = logging.getLogger()

BUF_SIZE = 1

def data_chunker(data, batch_size):
    start, end = 0, batch_size
    while end < len(data):
        yield data[start:end]
        start, end = end, end+batch_size
    yield data[start:]
    


class PredictorThread(threading.Thread):
    def __init__(self, shared_queue: queue.Queue, data, pred_batch_size, *args, **kwargs) -> None:
        super(PredictorThread, self).__init__(*args, **kwargs)
        self.shared_queue = shared_queue
        self.data = data
        self.pred_batch_size = pred_batch_size

    def run(self):
        logger.info(f'Start to Pridict')
        try:
            for batch_id, _data in enumerate(data_chunker(self.data, self.pred_batch_size)):
                logger.info(f'Batch {batch_id}, Get: {_data}')
                self.shared_queue.put(_data)
                time.sleep(1)
        except Exception as e:
            logger.error(f'Get Error : {e}')
        logger.info(f'Predict Done')


class UploaderThread(threading.Thread):
    def __init__(self, shared_queue: queue.Queue, flag_finish_pred:threading.Event, *args, **kwargs) -> None:
        super(UploaderThread, self).__init__(*args, **kwargs)
        self.shared_queue = shared_queue
        self.flag_finish_pred = flag_finish_pred

    def run(self):
        logger.info(f'Waiting Result to Upload')
        while True:
            if self.shared_queue.empty():
                if self.flag_finish_pred.is_set():
                    logger.info(f'Predict Thread Finish!!!!!!!!!!!!')
                    break
                else:
                    time.sleep(2)
            else:
                try:
                    self.shared_queue.get(timeout=5)
                except Exception as e:
                    logger.error(f'Get Error : {e}')
        logger.info(f'Upload Done')

class InferenceMgr:
    def __init__(self, json_data, data) -> None:
        self.cfg = json_data
        self.data = data
        pred_batch_size = 5

        self.shared_queue = queue.Queue(BUF_SIZE)
        self.flag_finish_pred = threading.Event()

        self.predictor = PredictorThread(self.shared_queue, self.data, pred_batch_size, name="Predictor", daemon=True)
        self.uploader = UploaderThread(self.shared_queue, self.flag_finish_pred, name="Uploader", daemon=True)

    def start_pred(self):
        self.predictor.start()
        self.uploader.start()
        while self.predictor.is_alive(): 
            self.predictor.join(1)
        logger.info(f'Predict Thread Finish?')
        self.flag_finish_pred.set()
        self.uploader.join()


def main():
    data = list(range(1, 20))
    infMgr = InferenceMgr({}, data)
    infMgr.start_pred()


if __name__ == "__main__":
    main()
