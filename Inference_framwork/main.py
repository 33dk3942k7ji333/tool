import threading
import time
import random
import queue
import math

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

logger = logging.getLogger()

class PredictorThread(threading.Thread):
    def __init__(self, shared_queue, data, pred_batch_size, *args, **kwargs) -> None:
        super(PredictorThread, self).__init__(*args, **kwargs)
        self.shared_queue = shared_queue
        self.data = data
        self.pred_batch_size = pred_batch_size
        self.flag = True
        
        self.total_batch = self.get_batches()
        
    def get_batches(self):
        return math.ceil(len(self.data)/self.pred_batch_size)
        

    def run(self):
        logger.info(f'Start to Pridict')
        for batch_id in range(self.total_batch):
            logger.info(f'[{batch_id+1:2d}/{self.total_batch:2d}] Start')
            batch_data_start = batch_id * self.pred_batch_size
            batch_data_end = ((batch_id+1)*self.pred_batch_size) if ((batch_id+1)*self.pred_batch_size) <= len(self.data) else len(self.data)
            _sum = sum(self.data[batch_data_start:batch_data_end])
            self.shared_queue.put(_sum)
            logger.debug(f'[{batch_id+1:2d}/{self.total_batch:2d}] Get Result {_sum}, queue size: {self.shared_queue.qsize()}')
            time.sleep(random.random())
        logger.info(f'Predict Done')


class UploaderThread(threading.Thread):
    def __init__(self, shared_queue, flag, *args, **kwargs) -> None:
        super(UploaderThread, self).__init__(*args, **kwargs)
        self.shared_queue = shared_queue
        self.flag = flag

    def run(self):
        logger.info(f'Waiting Result to Upload')
        while True:
            if self.flag.is_set():
                break
            item = self.shared_queue.get()
            logger.debug('Getting ' + str(item)
                          + ' : ' + str(self.shared_queue.qsize()) + ' items in queue')
            time.sleep(random.random())
        logger.info(f'Upload Done')


class InferenceMgr:
    def __init__(self, json_data, data) -> None:
        self.cfg = json_data
        self.data = data
        pred_batch_size = 50
        
        BUF_SIZE = 30
        self.shared_queue = queue.Queue(BUF_SIZE)
        
        self.flag = threading.Event()
        
        self.predictor = PredictorThread(self.shared_queue, self.data, pred_batch_size, name="Predictor")
        self.uploader = UploaderThread(self.shared_queue, self.flag, name="Uploader")
        self.uploader.start()

    def start_pred(self):
        self.predictor.start()
        self.predictor.join()
        logger.info(f'Predict Thread Finish')
        self.flag.set()

        


def main():
    data = list(range(1,100))
    infMgr = InferenceMgr({}, data)
    infMgr.start_pred()


if __name__ == "__main__":
    main()
