# -*- coding: utf-8 -*-
"""
@file: utils.py
@author: Yong Xie
@time: 12/8/2021 9:47 PM
@Description: 
"""
import json
import numpy as np


class UniqueIDGenerator:

    def __init__(self, start):

        self.start = start
        self.cursor = start

    def __iter__(self):
        return self

    def __next__(self):
        self.cursor += 1
        return self.cursor - 1


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)