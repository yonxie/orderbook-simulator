# -*- coding: utf-8 -*-
"""
@file: utils.py
@author: Yong Xie
@time: 12/8/2021 9:47 PM
@Description: 
"""


class UniqueIDGenerator:

    def __init__(self, start):

        self.start = start
        self.cursor = start

    def __iter__(self):
        return self

    def __next__(self):
        self.cursor += 1
        return self.cursor - 1

