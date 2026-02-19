"""
Momentum Trader agent for 3D Liquidity Vacuum & Flash Crash Simulator
"""
import numpy as np

class MomentumTrader:
    def __init__(self, agent_id, price_grid, size, lookback=5, threshold=1.0):
        self.agent_id = agent_id
        self.price_grid = price_grid
        self.size = size
        self.lookback = lookback
        self.threshold = threshold
        self.last_prices = []

    def act(self, lob, time):
        # Track mid price
        best_bid = lob.best_bid() or self.price_grid[len(self.price_grid)//2]
        best_ask = lob.best_ask() or self.price_grid[len(self.price_grid)//2]
        mid = (best_bid + best_ask) / 2 if best_bid and best_ask else self.price_grid[len(self.price_grid)//2]
        self.last_prices.append(mid)
        if len(self.last_prices) > self.lookback:
            self.last_prices.pop(0)
        # If momentum detected, send marketable order
        if len(self.last_prices) == self.lookback:
            momentum = self.last_prices[-1] - self.last_prices[0]
            if momentum > self.threshold:
                # Buy aggressively
                price = lob.best_ask() or mid
                lob.add_order('bid', price, self.size, self.agent_id, time)
            elif momentum < -self.threshold:
                # Sell aggressively
                price = lob.best_bid() or mid
                lob.add_order('ask', price, self.size, self.agent_id, time)
