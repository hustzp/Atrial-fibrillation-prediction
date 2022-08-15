
import numpy as np
import os
import pandas as pd
from Demo.util.load_data import FileExtract
from tensorflow.keras.models import load_model
from sklearn.metrics import auc


# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class Test:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.file_extract = FileExtract()

    def test(self, path, interval=90):
        '''
            :param path: test path
            :param interval: sample length
            :return: test result
        '''

        files = os.listdir(path)

        save_aurc = []
        for file in files:
            cur_aurc = self._get_aurc(path, file, interval)
            print(file, cur_aurc)
            save_aurc.append(cur_aurc)

        re = pd.DataFrame({'filename': files, 'AURC': save_aurc})

        return re

    def _get_aurc(self, path, file, interval, num=1000):
        cur_x = self.file_extract.extract(path, file, interval)
        time = np.sum(cur_x, axis=-1)
        pred = self.model.predict(np.expand_dims(cur_x, 2) / 1000)[:, 1]

        thresh = np.arange(0, num) / num
        point = []
        for th in thresh:
            cur_pred = np.zeros(shape=(pred.shape[0],))
            cur_pred[pred >= th] = 1
            rate = np.sum(time[cur_pred == 1]) / np.sum(time)
            point.append(rate)
        point.append(0)
        thresh = np.hstack((thresh, 1))
        area = auc(thresh, point)

        return area


if __name__ == '__main__':
    model_path = '../model/model.h5'
    data_path = '../data/PAF'

    test = Test(model_path)

    result = test.test(data_path).values[:, 1]

    print(result[result > 0.48].shape, result.shape)
