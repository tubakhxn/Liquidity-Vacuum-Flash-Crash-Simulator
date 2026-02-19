"""
Metrics calculations for 3D Liquidity Vacuum & Flash Crash Simulator
"""
import numpy as np

def compute_spread(lob):
    best_bid = lob.best_bid()
    best_ask = lob.best_ask()
    if best_bid is not None and best_ask is not None:
        return best_ask - best_bid
    return np.nan

def compute_slippage(trades, reference_price):
    if not trades:
        return 0.0
    prices = np.array([t[0] for t in trades])
    return np.mean(np.abs(prices - reference_price))

def liquidity_vacuum_index(lob):
    # Simple: fraction of empty price levels
    total = len(lob.price_grid)
    empty = sum((not lob.bids[p] and not lob.asks[p]) for p in lob.price_grid)
    return empty / total

def crash_probability(history, threshold=0.1):
    # Estimate: fraction of time steps with vacuum index > threshold
    vacs = [liquidity_vacuum_index(lob) for lob in history]
    return np.mean([v > threshold for v in vacs])
