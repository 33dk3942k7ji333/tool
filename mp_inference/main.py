import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import numpy as np
import model_trainer
from concurrent.futures import ProcessPoolExecutor

from tensorflow.keras.models import load_model

from  multiprocessing import Manager


def call_model(model_dir, data):
    loaded_model = load_model(model_dir)
    res = loaded_model.predict(data)
    print(res)
    print("Done")
    return res


def main():
    
    model_dir = "./saved_model/model.h5"
    model, x_train, y_train, x_test, y_test = model_trainer.main()
    model.save(model_dir)
    # manager = Manager()
    # namespace = manager.Namespace()
    # namespace.model = model
    # mp_mgr = ProcessPoolExecutor(max_workers=1, initializer=init_pool, initargs=(namespace,))
    
    mp_mgr = ProcessPoolExecutor(max_workers=20)

    

    for i in range(20):
        mp_mgr.submit(call_model, model_dir, x_train)
    print("End")

if __name__ == "__main__":
    main()