"""
Forced Liquidator agent for 3D Liquidity Vacuum & Flash Crash Simulator
"""
import numpy as np

class ForcedLiquidator:
    def __init__(self, agent_id, price_grid, size, trigger_prob=0.01):
        self.agent_id = agent_id
        self.price_grid = price_grid
        self.size = size
        self.trigger_prob = trigger_prob
        self.triggered = False

    def act(self, lob, time):
        # With some probability, trigger forced liquidation
        if not self.triggered and np.random.rand() < self.trigger_prob:
            self.triggered = True
            # Sell all at market
            price = lob.best_bid() or self.price_grid[0]
            lob.add_order('ask', price, self.size, self.agent_id, time)
