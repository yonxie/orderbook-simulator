import unittest

from orderbook.order import LimitOrder, CancelOrder
from orderbook.orderBook import OrderBook


class TestOrderBook(unittest.TestCase):

    # def test_AddOrder(self):
    #     book = OrderBook()
    #     # Simple Limit order example (as defined in spec)
    #
    #     # B,100322,5103,7500
    #     book.process_order(LimitOrder('B', 100322, 5103, 7500))
    #     self.assertTrue(len(book.bids.order_map) == 1)
    #     self.assertTrue(100322 in book.bids.order_map)
    #     self.assertTrue(5103 is book.bids.max)
    #     self.assertTrue(5103 in book.bids.price_map)
    #
    #     # S,100345,5103,100000,10000
    #     book.process_order(LimitOrder('S', 100345, 5103, 100000))
    #     self.assertTrue(len(book.asks.order_map) == 1)
    #     self.assertTrue(100345 in book.asks.order_map)
    #     # Trade should have matched the bid
    #     self.assertTrue(5103 is book.asks.min)
    #     self.assertTrue(5103 not in book.bids.price_map)
    #
    # def test_Bids(self):
    #     book = OrderBook()
    #     book.process_order(LimitOrder('B', 100322, 5103, 7500))
    #     book.process_order(LimitOrder('B', 100345, 5103, 10000))
    #     book.process_order(LimitOrder('B', 1, 5100, 10))
    #     self.assertTrue(len(book.bids.price_map.keys()) == 2)
    #     self.assertTrue(len(book.bids.order_map.keys()) == 3)
    #     self.assertTrue(book.bids.min == 5100)
    #
    # def test_ComplexLimitOrders(self):
    #     book = OrderBook()
    #     book.process_order(LimitOrder('B', 1138, 31502, 7500))
    #     book.process_order(LimitOrder('B', 1139, 31502, 7500))
    #     trades = book.process_order(LimitOrder('S', 1, 31501, 20000))
    #     self.assertTrue(len(trades) == 2)
    #     self.assertTrue(trades[0].id == 1138)
    #     self.assertTrue(trades[1].id == 1139)
    #     self.assertTrue(1138 not in book.bids.order_map)
    #     self.assertTrue(1139 not in book.bids.order_map)
    #     book.process_order(LimitOrder('S', 2, 30501, 1000))
    #     book.process_order(LimitOrder('S', 3, 30501, 200))
    #     trades = book.process_order(LimitOrder('B', 1003, 30501, 1000))
    #     self.assertTrue(3 not in book.bids.order_map)
    #     self.assertTrue(3 in book.asks.order_map)
    #
    #     self.assertTrue(len(trades) == 1)
    #     self.assertTrue(trades[0].id == 2)
    #
    #
    # def test_CancelOrder(self):
    #
    #     book = OrderBook()
    #     book.process_order(LimitOrder('B', 1, 101, 10))
    #     book.process_order(LimitOrder('B', 2, 102, 10))
    #     book.process_order(LimitOrder('B', 3, 103, 10))
    #     book.process_order(LimitOrder('B', 4, 104, 10))
    #     book.process_order(LimitOrder('B', 5, 102, 10))
    #
    #     book.process_order(CancelOrder(1))
    #     self.assertTrue(1 not in book.bids.order_map)
    #     self.assertTrue(101 not in book.bids.price_map)
    #     self.assertEqual(len(book.bids.price_map), 3)
    #
    #     book.process_order(CancelOrder(2))
    #     self.assertTrue(2 not in book.bids.order_map)
    #     self.assertTrue(102 in book.bids.price_map)
    #     self.assertEqual(len(book.bids.price_map), 3)
    #
    #     trades = book.process_order(LimitOrder('S', 5, 102, 15))
    #     self.assertEqual(trades[0].id, 4)
    #     self.assertEqual(trades[1].id, 3)
    #     self.assertEqual(len(trades), 2)

    def test_MarketOrder(self):
        book = OrderBook()
        book.process_order(LimitOrder('B', 1, 101, 10))
        book.process_order(LimitOrder('B', 2, 102, 10))
        book.process_order(LimitOrder('S', 3, 0, 30))
        trades = book.process_order(LimitOrder('B', 4, 103, 5))

    if __name__ == '__main__':
        unittest.main()
