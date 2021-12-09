import sys
import time


class CancelOrder(object):

    def __init__(self, order_id):
        self.id = order_id


class LimitOrder(object):

    def __init__(self, order_type, order_id, order_price, order_size):
        self.type = order_type
        self.id = order_id
        self.price = order_price    # market order is represented as extreme high price
        self.size = order_size
        # DList: each Order has a next and previous (see OrderList)
        self.next_order = None
        self.prev_order = None
        self.time = time.time()

        self.trade_size = 0  # Variable to track traded size (of matched orders)

    @property
    def is_bid(self):
        """
        Returns if the Order is a bid or not
        :return boolean:
        """
        return self.type == 'B'

    def match(self, other_order):
        """
        Returns true ONLY when other_order matches ALL current size
        :param other_order:
        :return boolean:
        """
        # Error checking
        # if other_order.type == self.type:
        #     return False
        # if other_order.is_bid and other_order.price < self.price:
        #     return False
        # if not other_order.is_bid and self.price < other_order.price:
        #     return False

        # full size trade (order size < other_order's order size)
        if self.size <= other_order.size:
            trade_size = self.size
            # update both parties
            self.make_trade(trade_size)
            other_order.make_trade(trade_size)
            return True
        # partial trade (order size > other_order's order size)
        else:
            trade_size = other_order.size
            self.make_trade(trade_size)
            other_order.make_trade(trade_size)
            return False

    def update_id(self, order_id):
        self.id = order_id

    def make_trade(self, trade_size):
        """
        Close a deal of a specific size and update remaining order sizes accordingly
        :param trade_size:
        """
        self.trade_size += trade_size
        self.size -= trade_size

    def print_trade_result(self, other_order_id):
        if self.trade_size > 0:
            if self.is_bid:
                print("{},{},{},{}".format(self.id, other_order_id, self.price, self.trade_size))
            else:
                print("{},{},{},{}".format(other_order_id, self.id, self.price, self.trade_size))
            self.trade_size = 0

    def to_print(self):
        if self.is_bid:
            sys.stdout.write("{:>10}|{:>13}|{:>7}".format(     # custom line spacing
                    self.id,
                    "{:,}".format(self.size),  # thousands separator
                    "{:,}".format(self.price)))
        else:
            sys.stdout.write("{:>7}|{:>13}|{:>10}".format(
                "{:,}".format(self.price),
                "{:,}".format(self.size),
                self.id))

    def __str__(self):
        return "Order: type: {} id: {} price: {} size {}".format(self.type, self.id, self.price, self.size)
