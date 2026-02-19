"""
Streamlit UI and metrics panel for 3D Liquidity Vacuum & Flash Crash Simulator
"""
import streamlit as st
import numpy as np
from liquidity_sim.simulation import Simulation
from liquidity_sim.agents.market_maker import MarketMaker
from liquidity_sim.agents.momentum_trader import MomentumTrader
from liquidity_sim.agents.forced_liquidator import ForcedLiquidator
from liquidity_sim.shocks import ShockEvent, LiquidityEvaporation
from liquidity_sim.network import MarketNetwork
from liquidity_sim.visualization import plot_liquidity_surface
from liquidity_sim.metrics import compute_spread, compute_slippage, liquidity_vacuum_index, crash_probability
from liquidity_sim.utils import make_price_grid


def run_app():
    st.title("3D Liquidity Vacuum & Flash Crash Simulator")
    st.sidebar.header("Simulation Controls")
    # UI controls
    shock_size = st.sidebar.slider("Shock Size", 1, 10, 3)
    cancel_rate = st.sidebar.slider("Cancel Rate", 0.0, 0.5, 0.1, 0.01)
    mm_risk = st.sidebar.slider("Market Maker Risk Aversion", 0.1, 5.0, 1.0, 0.1)
    coupling = st.sidebar.slider("Correlation Coupling", 0.0, 1.0, 0.1, 0.01)
    n_steps = st.sidebar.slider("Simulation Steps", 10, 200, 50)
    n_agents = st.sidebar.slider("Number of Agents", 5, 50, 10)
    n_mms = st.sidebar.slider("Market Makers", 1, n_agents, 3)
    n_moms = st.sidebar.slider("Momentum Traders", 1, n_agents, 3)
    n_liqs = st.sidebar.slider("Forced Liquidators", 1, n_agents, 1)
    evaporation_rate = st.sidebar.slider("Liquidity Evaporation Rate", 0.0, 0.2, 0.05, 0.01)

    price_grid = make_price_grid()
    agents = []
    for i in range(n_mms):
        agents.append(MarketMaker(i, mm_risk, price_grid, size=5, cancel_rate=cancel_rate))
    for i in range(n_moms):
        agents.append(MomentumTrader(n_mms+i, price_grid, size=2))
    for i in range(n_liqs):
        agents.append(ForcedLiquidator(n_mms+n_moms+i, price_grid, size=10))

    sim = Simulation(price_grid, agents, params={})
    network = MarketNetwork(n_agents, coupling)
    shock = ShockEvent(size=shock_size, time=n_steps//2)
    evaporation = LiquidityEvaporation(evaporation_rate)

    bid_depths = []
    ask_depths = []
    for t in range(n_steps):
        if t == shock.time:
            shock.apply(sim.lob, t)
            network.propagate_shock([0], shock_size)  # Shock agent 0
        evaporation.apply(sim.lob)
        trades = sim.step()
        _, bid, ask = sim.lob.get_depth()
        bid_depths.append(bid)
        ask_depths.append(ask)

    time_grid = np.arange(n_steps)
    bid_depths = np.array(bid_depths)
    ask_depths = np.array(ask_depths)
    fig = plot_liquidity_surface(price_grid, time_grid, bid_depths, ask_depths)
    st.plotly_chart(fig, use_container_width=True)

    st.header("Metrics Panel")
    spread = compute_spread(sim.lob)
    slippage = compute_slippage(trades, price_grid[len(price_grid)//2])
    vacuum = liquidity_vacuum_index(sim.lob)
    crash_prob = crash_probability([sim.lob])
    st.metric("Spread", f"{spread:.2f}")
    st.metric("Slippage", f"{slippage:.2f}")
    st.metric("Liquidity Vacuum Index", f"{vacuum:.2f}")
    st.metric("Crash Probability", f"{crash_prob:.2f}")
