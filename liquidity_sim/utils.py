"""
Helper utilities for 3D Liquidity Vacuum & Flash Crash Simulator
"""
import numpy as np

def make_price_grid(center=100.0, n=50, tick=0.1):
    return np.round(np.linspace(center - n//2*tick, center + n//2*tick, n), 2)
