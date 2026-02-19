# 3D Liquidity Vacuum & Flash Crash Simulator

## Overview
This application simulates a limit order book (LOB) with agent-based modeling to study liquidity evaporation and flash crash dynamics. It features:
- Market makers, momentum traders, and forced liquidators
- Order flow, cancellations, and liquidity withdrawal
- Shock events and stress propagation (NetworkX)
- 3D Plotly visualization (Price × Time × Liquidity)
- Streamlit UI with interactive controls and metrics

## Core Modules
- `order_book.py`: Implements a price-level LOB with order matching, depth, and cancellation
- `agents/`: Contains agent classes with distinct behaviors
- `simulation.py`: Runs the simulation loop, collects history
- `shocks.py`: Models exogenous shocks and endogenous liquidity evaporation
- `network.py`: Propagates stress between agents using a random network
- `visualization.py`: 3D/animated liquidity surface with Plotly
- `ui.py`: Streamlit UI, controls, and metrics panel
- `metrics.py`: Computes spread, slippage, vacuum index, crash probability
- `utils.py`: Helper functions (e.g., price grid)

## How to Run
1. Install requirements: `pip install -r requirements.txt`
2. Launch: `streamlit run liquidity_sim/main.py`

## Simulation Logic
- Each agent acts at each time step (places/cancels orders)
- Orders are matched in the LOB
- Shocks and liquidity evaporation can remove orders
- NetworkX propagates stress to simulate correlated agent behavior
- Metrics are computed and visualized in real time

## Metrics
- **Spread**: Best ask - best bid
- **Slippage**: Avg. trade price deviation from mid
- **Liquidity Vacuum Index**: Fraction of empty price levels
- **Crash Probability**: Fraction of time with high vacuum index

## Customization
- UI controls for shock size, cancel rate, risk aversion, coupling, etc.
- Easily extendable agent logic and event types

---
For further details, see code comments in each module.