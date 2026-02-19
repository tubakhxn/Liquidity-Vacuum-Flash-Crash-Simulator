"""
Market Maker agent for 3D Liquidity Vacuum & Flash Crash Simulator
"""
import numpy as np

class MarketMaker:
    def __init__(self, agent_id, risk_aversion, price_grid, size, cancel_rate):
        self.agent_id = agent_id
        self.risk_aversion = risk_aversion
        self.price_grid = price_grid
        self.size = size
        self.cancel_rate = cancel_rate
        self.active_orders = []

    def act(self, lob, time):
        # Cancel some orders probabilistically
        for oid in list(self.active_orders):
            if np.random.rand() < self.cancel_rate:
                lob.cancel_order(oid)
                self.active_orders.remove(oid)
        # Place new bid/ask orders around mid
        best_bid = lob.best_bid() or self.price_grid[len(self.price_grid)//2]
        best_ask = lob.best_ask() or self.price_grid[len(self.price_grid)//2]
        mid = (best_bid + best_ask) / 2 if best_bid and best_ask else self.price_grid[len(self.price_grid)//2]
        spread = 1 + self.risk_aversion
        bid_price = max(self.price_grid[0], mid - spread)
        ask_price = min(self.price_grid[-1], mid + spread)
        bid_oid = lob.add_order('bid', bid_price, self.size, self.agent_id, time)
        ask_oid = lob.add_order('ask', ask_price, self.size, self.agent_id, time)
        self.active_orders.extend([bid_oid, ask_oid])
