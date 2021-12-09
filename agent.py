# -*- coding: utf-8 -*-
"""
@file: simulator
@author: Yong Xie
@time: 12/8/2021 11:25 AM
@Description:

Agent simulator.

"""
from orderbook.order import LimitOrder, CancelOrder
import numpy as np
import scipy.stats as ss


class Agent:

    def __init__(self, side, seed, consensus_price, tick, max_tick_num, max_num):
        self.side = side
        self.generator = np.random.default_rng(seed)
        self.seed = seed
        self.consensus_price = consensus_price
        self.tick = tick
        self.max_tick_num = max_tick_num
        self.max_num = max_num
        self.count = 0

    def _discretize_probability(self):
        """
        Discretize probability for each tick
        """

        if self.consensus_price - self.max_tick_num * self.tick < 0:
            raise Exception('Price can drop below 0, please check!')
        tick_grid = np.linspace(-self.max_tick_num, self.max_tick_num, 2 * self.max_tick_num + 1)

        lo = self.consensus_price + tick_grid * self.tick - self.tick * 0.5
        hi = self.consensus_price + tick_grid * self.tick + self.tick * 0.5

        hi_prob = ss.norm.cdf(hi, scale=self.consensus_price / 30, loc=self.consensus_price)
        lo_prob = ss.norm.cdf(lo, scale=self.consensus_price / 30, loc=self.consensus_price)
        prob = hi_prob - lo_prob
        prob = prob / prob.sum()

        return tick_grid, prob

    def hasnext(self):

        if self.max_num:
            if self.count < self.max_num:
                return True
            else:
                return False
        else:
            return True

    def __iter__(self):
        return self


class BuyAgent(Agent):

    def __init__(self, side, seed, consensus_price, market_order_intensity,
                 limit_order_intensity, cancel_order_intensity,
                 tick=0.01, max_tick_num=3000, max_num=None):

        Agent.__init__(self, side, seed, consensus_price, tick, max_tick_num, max_num)
        self.market_order_intensity = market_order_intensity
        self.limit_order_intensity = limit_order_intensity
        self.cancel_order_intensity = cancel_order_intensity
        self.tick_grid, self.prob = self._discretize_probability()

    def _simulate_price(self):
        """
        Simulate price for bid order of ask order
        """

        tick_num = np.random.choice(self.tick_grid, size=1, p=self.prob)[0]
        price = tick_num * self.tick + self.consensus_price
        return price

    def update_market_order_intensity(self, market_order_intensity):
        self.market_order_intensity = market_order_intensity

    def update_cancel_order_intensity(self, cancel_order_intensity):
        self.cancel_order_intensity = cancel_order_intensity

    def update_limit_order_intensity(self, limit_order_intensity):
        self.limit_order_intensity = limit_order_intensity

    def __next__(self):

        if not self.hasnext():
            raise Exception('Maximum number of orders is reached!')

        order_type_prob = np.array([self.market_order_intensity,
                                    self.limit_order_intensity,
                                    self.cancel_order_intensity])
        order_type_prob = order_type_prob / order_type_prob.sum()
        order_types = [0, 1, 2]

        order_type = np.random.choice(order_types, size=1, p=order_type_prob)[0]
        size = 1
        # generate orders, use fake id
        if order_type == 0:  # market order
            order = LimitOrder(self.side, 1, self.consensus_price + self.max_tick_num * self.tick, size)
            waiting_time = self.generator.exponential(1 / self.market_order_intensity, size=1)[0]
        elif order_type == 1:
            price = self._simulate_price()
            order = LimitOrder(self.side, 1, price, size)
            waiting_time = self.generator.exponential(1 / self.limit_order_intensity, size=1)[0]
        else:
            order = CancelOrder(1)
            waiting_time = self.generator.exponential(1 / self.cancel_order_intensity, size=1)[0]

        self.count += 1

        return waiting_time, order


class SellAgent(Agent):

    def __init__(self, side, seed, consensus_price, market_order_intensity,
                 limit_order_intensity, cancel_order_intensity,
                 tick=0.01, max_tick_num=3000, max_num=None):

        Agent.__init__(self, side, seed, consensus_price, tick, max_tick_num, max_num)
        self.market_order_intensity = market_order_intensity
        self.limit_order_intensity = limit_order_intensity
        self.cancel_order_intensity = cancel_order_intensity
        self.tick_grid, self.prob = self._discretize_probability()

    def _simulate_price(self):
        """
        Simulate price for bid order of ask order
        """

        tick_num = np.random.choice(self.tick_grid, size=1, p=self.prob)[0]
        price = tick_num * self.tick + self.consensus_price
        return price

    def update_market_order_intensity(self, market_order_intensity):
        self.market_order_intensity = market_order_intensity

    def update_cancel_order_intensity(self, cancel_order_intensity):
        self.cancel_order_intensity = cancel_order_intensity

    def update_limit_order_intensity(self, limit_order_intensity):
        self.limit_order_intensity = limit_order_intensity

    def __next__(self):

        if not self.hasnext():
            raise Exception('Maximum number of orders is reached!')

        order_type_prob = np.array([self.market_order_intensity,
                                    self.limit_order_intensity,
                                    self.cancel_order_intensity])
        order_type_prob = order_type_prob / order_type_prob.sum()
        order_types = [0, 1, 2]

        order_type = np.random.choice(order_types, size=1, p=order_type_prob)[0]
        size = 1

        # generate orders, use fake id
        if order_type == 0:  # market order
            order = LimitOrder(self.side, 1, self.consensus_price - self.max_tick_num * self.tick, size)
            waiting_time = self.generator.exponential(1/self.market_order_intensity, size=1)[0]
        elif order_type == 1:
            price = self._simulate_price()
            order = LimitOrder(self.side, 1, price, size)
            waiting_time = self.generator.exponential(1 / self.limit_order_intensity, size=1)[0]
        else:
            order = CancelOrder(1)
            waiting_time = self.generator.exponential(1 / self.cancel_order_intensity, size=1)[0]

        self.count += 1
        return waiting_time, order

