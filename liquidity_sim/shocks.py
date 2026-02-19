"""
Shock event and liquidity evaporation logic for 3D Liquidity Vacuum & Flash Crash Simulator
"""
import numpy as np

class ShockEvent:
    def __init__(self, size, time, target_price=None):
        self.size = size
        self.time = time
        self.target_price = target_price

    def apply(self, lob, current_time):
        # Remove liquidity from both sides around target price
        if current_time == self.time:
            center = self.target_price or (lob.best_bid() + lob.best_ask()) / 2
            for price in lob.price_grid:
                if abs(price - center) < self.size:
                    # Remove all orders at this price (liquidity evaporation)
                    lob.bids[price].clear()
                    lob.asks[price].clear()

class LiquidityEvaporation:
    def __init__(self, evaporation_rate):
        self.evaporation_rate = evaporation_rate

    def apply(self, lob):
        # Randomly remove orders to simulate liquidity withdrawal
        for price in lob.price_grid:
            for book in [lob.bids, lob.asks]:
                orders = list(book[price])
                for order in orders:
                    if np.random.rand() < self.evaporation_rate:
                        book[price].remove(order)
                        if order.order_id in lob.order_map:
                            del lob.order_map[order.order_id]
