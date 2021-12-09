# Wrapper method to satisfy setup.py entry_point
import sys

from orderbook.order import LimitOrder, CancelOrder
from orderbook.orderBook import OrderBook
from timeit import default_timer as timer
from utils import UniqueIDGenerator
from agent import BuyAgent, SellAgent
import numpy as np
import time


def main():
    book = OrderBook()
    buyer = BuyAgent('B', 42, 98, 1, 10, 5)
    seller = SellAgent('S', 43, 102, 1, 10, 5)
    order_id_generator = UniqueIDGenerator(1000000)
    start = timer()
    order_count = 0
    trade_count = 0
    target_level = 10

    while order_count < 100000:
        bid_wait_time, bid_order = next(buyer)
        ask_wait_time, ask_order = next(seller)

        if bid_wait_time < ask_wait_time:
            new_order = bid_order
        else:
            new_order = ask_order

        if isinstance(new_order, LimitOrder):
            new_order.id = next(order_id_generator)
        elif isinstance(new_order, CancelOrder):
            if bid_wait_time < ask_wait_time:
                if len(book.bids.order_map) > 0:
                    new_order.id = np.random.choice(list(book.bids.order_map.keys()), size=1)[0]
            else:
                if len(book.asks.order_map) > 0:
                    new_order.id = np.random.choice(list(book.asks.order_map.keys()), size=1)[0]

        trade = book.process_order(new_order)
        trade_count += len(trade)

        buyer.update_cancel_order_intensity(1)
        seller.update_cancel_order_intensity(1)
        order_count += 1

        if order_count % 500 == 0:

            outstanding_bid = len(book.bids.order_map)
            outstanding_ask = len(book.asks.order_map)
            bid_levels = len(book.bids.price_map)
            ask_levels = len(book.asks.price_map)

            shallow_bid_prices = sorted(book.bids.price_map.keys(), reverse=True)[:target_level]
            shallow_ask_prices = sorted(book.asks.price_map.keys(), reverse=False)[:target_level]

            outstanding_bid_shallow = sum([book.bids.price_map[p].size for p in shallow_bid_prices])
            outstanding_ask_shallow = sum([book.asks.price_map[p].size for p in shallow_ask_prices])

            print('---------------------------------------------------------------------------')
            print('|++ count: {} | trade count: {} |'.format(order_count, trade_count))
            print('|++++ bid level: {} | outstanding bid: {} | outstanding shallow bid: {} |'.format(bid_levels,
                                        outstanding_bid, outstanding_bid_shallow))
            print('|++++ ask level: {} | outstanding ask: {} | outstanding shallow ask: {} |'.format(ask_levels,
                                        outstanding_ask, outstanding_ask_shallow))

    total = timer() - start


if __name__ == '__main__':
    main()