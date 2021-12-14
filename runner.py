# Wrapper method to satisfy setup.py entry_point
import sys

from orderbook.order import LimitOrder, CancelOrder
from orderbook.orderBook import OrderBook
from timeit import default_timer as timer
from utils import UniqueIDGenerator, NumpyEncoder
from agent import BuyAgent, SellAgent
import numpy as np


def main(attack_side, attack_level, attack=True, time_to_cancel=None,
         order_to_cancel=None, trading_hours=6.5, price_vol=0.01):

    book = OrderBook(log=True)
    buyer = BuyAgent('B', 42, 99.5, 4, 40, 6, price_vol=price_vol)
    seller = SellAgent('S', 43, 100.5, 4, 40, 6, price_vol=price_vol)
    order_id_generator = UniqueIDGenerator(1000000)
    start = timer()
    target_level = attack_level
    attack_orders = {'0': {'side': 'B', 'submit_time': 0, 'terminate_time': 0, 'terminate_type': 1}}
    attack_succ, attack_count = 0, 0.01
    last_attack, outstanding_attack_id = 0, None

    while book.order_count < 10000000 and book.sys_time < trading_hours * 3600:
        bid_wait_time, bid_order = next(buyer)
        ask_wait_time, ask_order = next(seller)

        if bid_wait_time < ask_wait_time:
            new_order = bid_order
        else:
            new_order = ask_order

        book.sys_time += min(bid_wait_time, ask_wait_time)

        if isinstance(new_order, LimitOrder):
            new_order.id = next(order_id_generator)
        elif isinstance(new_order, CancelOrder):
            if bid_wait_time < ask_wait_time:
                if len(book.bids.order_map) > 0:
                    new_order.id = np.random.choice(list(book.bids.order_map.keys()), size=1)[0]
            else:
                if len(book.asks.order_map) > 0:
                    new_order.id = np.random.choice(list(book.asks.order_map.keys()), size=1)[0]

        trades = book.process_order(new_order)

        if trades and outstanding_attack_id:
            for trade in trades:
                if trade.id == outstanding_attack_id:
                    attack_orders[outstanding_attack_id]['terminate_type'] = 0
                    attack_orders[outstanding_attack_id]['terminate_time'] = book.sys_time
                    if outstanding_attack_id in book.bids.order_map or outstanding_attack_id in book.asks.order_map:
                        book.process_order(CancelOrder(outstanding_attack_id))
                    outstanding_attack_id = None

        # buyer.update_cancel_order_intensity(1)
        # seller.update_cancel_order_intensity(1)

        # implement attack
        if attack:
            if outstanding_attack_id:
                if time_to_cancel and book.sys_time - last_attack > time_to_cancel:
                    book.process_order(CancelOrder(outstanding_attack_id))
                    attack_orders[outstanding_attack_id]['terminate_time'] = book.sys_time
                    attack_orders[outstanding_attack_id]['terminate_type'] = 1
                    outstanding_attack_id = None
                    attack_succ += 1
                elif order_to_cancel and book.order_count - last_attack > order_to_cancel:
                    book.process_order(CancelOrder(outstanding_attack_id))
                    attack_orders[outstanding_attack_id]['terminate_time'] = book.sys_time
                    attack_orders[outstanding_attack_id]['terminate_type'] = 1
                    outstanding_attack_id = None
                    attack_succ += 1
            else: # enforce attack
                attack_price = None
                if attack_side == 'B':
                    if len(book.bids.price_map.keys()) >= attack_level:
                        attack_price = sorted(book.bids.price_map.keys(), reverse=True)[attack_level-1]
                else:
                    if len(book.asks.price_map.keys()) >= attack_level:
                        attack_price = sorted(book.asks.price_map.keys(), reverse=False)[attack_level-1]
                if attack_price:
                    size = 1
                    outstanding_attack_id = next(order_id_generator)
                    book.process_order(LimitOrder(attack_side, outstanding_attack_id, attack_price, size))
                    if time_to_cancel:
                        last_attack = book.sys_time
                    elif order_to_cancel:
                        last_attack = book.order_count
                    attack_orders[outstanding_attack_id] = {'side': 'B', 'submit_time': book.sys_time, 'size': size,
                                                            'terminate_time': None, 'terminate_type': 1}
                    attack_count += 1

        if book.order_count % 50000 == 0:

            outstanding_bid = book.book_log[book.order_count]['outstanding_bid']
            outstanding_ask = book.book_log[book.order_count]['outstanding_ask']
            bid_levels = book.book_log[book.order_count]['bid_depth']
            ask_levels = book.book_log[book.order_count]['ask_depth']

            shallow_bid_prices = sorted(book.bids.price_map.keys(), reverse=True)[:target_level]
            shallow_ask_prices = sorted(book.asks.price_map.keys(), reverse=False)[:target_level]

            outstanding_bid_shallow = sum([book.bids.price_map[p].size for p in shallow_bid_prices])
            outstanding_ask_shallow = sum([book.asks.price_map[p].size for p in shallow_ask_prices])
            hour = int(book.sys_time // 3600)
            minute = int((book.sys_time - hour * 3600) // 60)

            print('---------------------------------------------------------------------------')
            print('|++ count: {} | trade count: {} | time: {}:{}'.format(book.order_count, book.trade_count, hour, minute))
            print('|++++ bid level: {} | outstanding bid: {} | outstanding shallow bid: {} |'.format(
                bid_levels, outstanding_bid, outstanding_bid_shallow))
            print('|++++ ask level: {} | outstanding ask: {} | outstanding shallow ask: {} |'.format(
                ask_levels, outstanding_ask, outstanding_ask_shallow))
            print('|++++ attack count: {} | finished attack: {} |attack succ: {:.3f} |'.format(
                int(attack_count), len(attack_orders), attack_succ/len(attack_orders)))

    total = timer() - start

    del attack_orders['0']

    results = {
        'orders_amount': book.order_count,
        'attack_orders': attack_orders,
        "attack_count": attack_count,
        'attack_succ': attack_succ,
        'trade_count': book.trade_count,
        # 'lob_log': book.book_log
        'lob_log': None
    }

    return results


if __name__ == '__main__':

    experiment = {
        '1': {
            'time_to_cancel': 0.1,
            'price_vol': 0.01,
        },
        '2': {
            'time_to_cancel': 0.5,
            'price_vol': 0.01,
        },
        '3': {
            'time_to_cancel': 1,
            'price_vol': 0.01,
        },
        '4': {
            'time_to_cancel': 0.1,
            'price_vol': 0.05,
        },
        '5': {
            'time_to_cancel': 0.5,
            'price_vol': 0.05,
        },
        '6': {
            'time_to_cancel': 1,
            'price_vol': 0.05,
        },
        '7': {
            'order_to_cancel': 5,
            'price_vol': 0.05,
        },
        '8': {
            'order_to_cancel': 25,
            'price_vol': 0.05
        },
        '9': {
            'order_to_cancel': 50,
            'price_vol': 0.05
        }
    }

    import json

    with open(r'G:\orderbook-simulator\output\experiment_configuration.json', 'w') as f:
        f.write(json.dumps(experiment))

    levels = np.linspace(1, 15, 15)

    for k in ['1','2','3','4','5','6']:
        for level in levels:
            result = main('B', int(level), time_to_cancel=experiment[k]['time_to_cancel'],
                          price_vol=experiment[k]['price_vol'])
            with open(r'G:\orderbook-simulator\output\experiment-{},time_to_cancel-{},price_vol-{},level-{},.json'.format(
                    k, experiment[k]['time_to_cancel'], experiment[k]['price_vol'], int(level)), 'w') as f:
                f.write(json.dumps(result))

    # order to cancel

    for k in ['8']:
        for level in levels:
            result = main('B', int(level), order_to_cancel=experiment[k]['order_to_cancel'],
                          price_vol=experiment[k]['price_vol'])
            with open(r'G:\orderbook-simulator\output\experiment-{},order_to_cancel-{},price_vol-{},level-{},.json'.format(
                    k, experiment[k]['order_to_cancel'], experiment[k]['price_vol'], int(level)), 'w') as f:
                f.write(json.dumps(result))