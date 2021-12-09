# -*- coding: utf-8 -*-
"""
@file: TestCancelOrder.py
@author: Yong Xie
@time: 12/8/2021 3:00 PM
@Description: 
"""


import unittest

from orderbook.order import LimitOrder, CancelOrder
from orderbook.orderBook import OrderBook


class TestCancelOrder(unittest.TestCase):

    def test_simple_order(self):

        print('-------------Test Simple Cancel Orders-------------')

        book = OrderBook()
        book.process_order(LimitOrder('B', 1, 101, 10))
        book.process_order(LimitOrder('B', 2, 101, 10))
        book.process_order(CancelOrder(1))
        trades = book.process_order(LimitOrder('S', 3, 103, 10))
        self.assertTrue(len(trades) == 0)

        # Marching first B order
        trades = book.process_order(LimitOrder('S', 4, 101, 10))
        self.assertTrue(len(trades) == 1)
        self.assertTrue(len(book.bids.price_map) == 0)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 2)

    def test2(self):

        print('-------------Test Partial Orders-------------')

        book = OrderBook()
        book.process_order(LimitOrder('B', 1, 101, 10))
        book.process_order(LimitOrder('B', 2, 101, 10))
        book.process_order(CancelOrder(1))
        trades = book.process_order(LimitOrder('S', 3, 103, 10))
        self.assertTrue(len(trades) == 0)

        # Marching first B order
        trades = book.process_order(LimitOrder('S', 4, 101, 20))
        self.assertTrue(len(trades) == 1)
        self.assertTrue(len(book.bids.price_map) == 0)
        self.assertTrue(len(book.asks.price_map) == 2)
        self.assertTrue(trades[0].id == 2)

    def test3(self):

        print('-------------Test Complex Cancel Orders-------------')

        book = OrderBook()
        book.process_order(LimitOrder('B', 1, 101, 10))
        book.process_order(LimitOrder('B', 2, 102, 10))
        book.process_order(LimitOrder('B', 3, 103, 10))
        book.process_order(LimitOrder('B', 4, 104, 10))
        book.process_order(LimitOrder('B', 5, 102, 10))

        book.process_order(CancelOrder(1))
        self.assertEqual(len(book.bids.price_map), 3)

        book.process_order(CancelOrder(2))
        self.assertEqual(len(book.bids.price_map), 3)

        trades = book.process_order(LimitOrder('S', 5, 102, 15))
        self.assertEqual(len(trades), 2)

    if __name__ == '__main__':
        unittest.main()
