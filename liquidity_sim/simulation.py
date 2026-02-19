"""
Simulation engine for 3D Liquidity Vacuum & Flash Crash Simulator
"""
from liquidity_sim.order_book import LimitOrderBook
import numpy as np

class Simulation:
    def __init__(self, price_grid, agents, params):
        self.lob = LimitOrderBook(price_grid)
        self.agents = agents  # List of agent instances
        self.params = params
        self.time = 0
        self.history = []  # For visualization/metrics

    def step(self):
        # Agents act
        for agent in self.agents:
            agent.act(self.lob, self.time)
        # Match orders
        trades = self.lob.match_orders()
        # Record state
        self.history.append(self.lob.get_depth())
        self.time += 1
        return trades

    def run(self, n_steps):
        for _ in range(n_steps):
            self.step()
