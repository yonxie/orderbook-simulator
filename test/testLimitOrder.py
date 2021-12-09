import unittest

from orderbook.order import LimitOrder, CancelOrder
from orderbook.orderBook import OrderBook


class TestLimitOrder(unittest.TestCase):

    def test_LimitOrderSimple(self):

        print('-------------Test Simple Limit Orders-------------')

        book = OrderBook()
        book.process_order(LimitOrder('B', 1, 101, 10))
        book.process_order(LimitOrder('B', 2, 101, 10))
        trades = book.process_order(LimitOrder('S', 3, 103, 10))
        self.assertTrue(len(trades) == 0)

        # Marching first B order
        trades = book.process_order(LimitOrder('S', 4, 101, 10))
        self.assertTrue(len(trades) == 1)
        self.assertTrue(len(book.bids.price_map) == 1)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 1)

    def test_LimitOrdersAdvanced(self):

        print('-------------Test Advanced Limit Orders-------------')

        book = OrderBook()
        book.process_order(LimitOrder('B', 1, 101, 10))
        book.process_order(LimitOrder('B', 2, 101, 10))
        trades = book.process_order(LimitOrder('S', 3, 103, 10))
        self.assertTrue(len(trades) == 0)
        # Fill both B orders
        trades = book.process_order(LimitOrder('S', 5, 101, 20))
        self.assertTrue(len(trades) == 2)
        self.assertTrue(len(book.bids.price_map) == 0)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 1)
        self.assertTrue(trades[1].id == 2)

    def test_LimitOrderPartial(self):

        print('-------------Test Partial Limit Orders-------------')

        book = OrderBook()
        book.process_order(LimitOrder('B', 1, 101, 10))
        book.process_order(LimitOrder('B', 2, 101, 10))
        trades = book.process_order(LimitOrder('S', 5, 101, 15))
        self.assertTrue(len(trades) == 2)
        self.assertTrue(len(book.bids.price_map) == 1)
        self.assertTrue(len(book.asks.price_map) == 0)
        self.assertTrue(trades[0].id == 1)
        self.assertTrue(trades[1].id == 2)
        self.assertTrue(trades[1].size == 5)

    def test_LimitNewOrderPartial(self):

        print('-------------Test New Partial Limit Orders-------------')

        book = OrderBook()
        book.process_order(LimitOrder('B', 1, 101, 10))
        book.process_order(LimitOrder('B', 2, 101, 10))
        trades = book.process_order(LimitOrder('S', 5, 101, 25))
        self.assertTrue(len(trades) == 2)
        self.assertTrue(len(book.bids.price_map) == 0)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 1)
        self.assertTrue(trades[1].id == 2)
        self.assertTrue(book.asks.order_map[5].size == 5)

    if __name__ == '__main__':
        unittest.main()
