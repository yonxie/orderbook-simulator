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

    def __init__(self, side, seed, consensus_price, max_size, tick, max_tick_num, max_num, price_vol=0.01):
        self.side = side
        self.generator = np.random.default_rng(seed)
        self.seed = seed
        self.consensus_price = consensus_price
        self.tick = tick
        self.max_tick_num = max_tick_num
        self.max_num = max_num
        self.max_size = max_size
        self.count = 0
        self.price_vol = price_vol
        self.tick_grid, self.tick_prob = self._discretize_price_probability()
        self.size_grid, self.size_prob = self._discretize_size_probability()

    def _simulate_price(self):
        """
        Simulate price for bid order of ask order
        """

        tick_num = np.random.choice(self.tick_grid, size=1, p=self.tick_prob)[0]
        price = tick_num * self.tick + self.consensus_price
        return price

    def _simulate_size(self):
        size = np.random.choice(self.size_grid, size=1, p=self.size_prob)
        return size

    def _discretize_size_probability(self):
        """
        Discretize probability for each size
        """
        size_grid = np.linspace(1, self.max_size, self.max_size)
        lo = size_grid - 0.5
        hi = size_grid + 0.5

        prob = ss.gamma.cdf(hi, a=3, loc=1, scale=10) - ss.gamma.cdf(lo, a=3, loc=1, scale=10)
        prob = prob / prob.sum()

        return size_grid, prob

    def _discretize_price_probability(self):
        """
        Discretize probability for each tick
        """

        if self.consensus_price - self.max_tick_num * self.tick < 0:
            raise Exception('Price can drop below 0, please check!')
        tick_grid = np.linspace(-self.max_tick_num, self.max_tick_num, 2 * self.max_tick_num + 1)

        lo = self.consensus_price + tick_grid * self.tick - self.tick * 0.5
        hi = self.consensus_price + tick_grid * self.tick + self.tick * 0.5

        hi_prob = ss.norm.cdf(hi, scale=self.consensus_price * self.price_vol, loc=self.consensus_price)
        lo_prob = ss.norm.cdf(lo, scale=self.consensus_price * self.price_vol, loc=self.consensus_price)
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
                 tick=0.01, max_size=100, max_tick_num=3000, max_num=None, price_vol=0.01):

        Agent.__init__(self, side, seed, consensus_price, max_size, tick, max_tick_num, max_num, price_vol)
        self.market_order_intensity = market_order_intensity
        self.limit_order_intensity = limit_order_intensity
        self.cancel_order_intensity = cancel_order_intensity

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
        size = self._simulate_size()
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
                 tick=0.01, max_size=100, max_tick_num=3000, max_num=None, price_vol=0.01):

        Agent.__init__(self, side, seed, consensus_price, max_size, tick, max_tick_num, max_num, price_vol)
        self.market_order_intensity = market_order_intensity
        self.limit_order_intensity = limit_order_intensity
        self.cancel_order_intensity = cancel_order_intensity

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
        size = self._simulate_size()

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
