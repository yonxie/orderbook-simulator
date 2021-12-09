import sys
from orderbook.priceTree import PriceTree
from orderbook.ptreeIterator import ComplexIterator
from orderbook.order import CancelOrder, LimitOrder


class OrderBook(object):
    def __init__(self):
        self.bids = PriceTree('Bids')
        self.asks = PriceTree('Asks')

    def process_order(self, order):
        """
        # General method to process different type of orders
        """
        if isinstance(order, CancelOrder):
            trade = self._process_cancel_order(order)
        elif isinstance(order, LimitOrder):
            trade = self._process_limit_order(order)

        return trade

    def _process_cancel_order(self, order):
        """Method to process cancel order"""
        if order.id in self.bids.order_map:
            self.bids.remove_order(order.id)
        elif order.id in self.asks.order_map:
            self.asks.remove_order(order.id)

        return []

    def _process_limit_order(self, curr_order):
        """
        Generic method to process a Bid or Ask limit order
        :param curr_order:
        """
        opposite_tree = self.bids if not curr_order.is_bid else self.asks
        # we are assuming thar order can not be modified or canceled
        # Try first to match this order with the opposite tree
        trades = opposite_tree.match_price_order(curr_order)

        # If there is remaining order size add it to the matching tree
        if curr_order.size > 0:
            matching_tree = self.bids if curr_order.is_bid else self.asks
            matching_tree.insert_price_order(curr_order)

        # First print all trades
        # for order in trades:
        #     order.print_trade_result(curr_order.id)
        # curr_order.trade_size = 0
        # # And then the LOB state

        return trades

    def print_book(self):
        print("+-----------------------------------------------------------------+")
        print("| BUY                            | SELL                           |")
        print("| Id       | Volume      | Price | Price | Volume      | Id       |")
        print("+----------+-------------+-------+-------+-------------+----------+")
        bids_it = ComplexIterator(self.bids.tree.values(reverse=True))
        asks_it = ComplexIterator(self.asks.tree.values())
        while bids_it.hasnext() and asks_it.hasnext():
            sys.stdout.write("|")
            next(bids_it).to_print()
            sys.stdout.write("|")
            next(asks_it).to_print()
            sys.stdout.write("|\n")

        while asks_it.hasnext():
            sys.stdout.write("|                                |")
            next(asks_it).to_print()
            sys.stdout.write("|\n")

        while bids_it.hasnext():
            sys.stdout.write("|")
            next(bids_it).to_print()
            sys.stdout.write("|                                |\n")

        print("+-----------------------------------------------------------------+")