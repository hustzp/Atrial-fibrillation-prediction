
import os
import numpy as np
import pandas as pd
from Demo.util.test import Test
import time


if __name__ == '__main__':
    data_path = './data'
    model_path = './model/model.h5'
    save_path = 'output'

    types = ['Normal', 'NAF', 'LAF', 'PAF']

    test_pro = Test(model_path)

    for each in types:
        result = test_pro.test(data_path + '/' + each, interval=90)
        result.to_csv(save_path + '/' + '{}.csv'.format(each))
