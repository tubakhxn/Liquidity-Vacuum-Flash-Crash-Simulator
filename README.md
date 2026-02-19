
# 3D Liquidity Vacuum & Flash Crash Simulator
# Developer: tubakhxn
## What is this project about?
This project is a fully modular, agent-based simulation platform for studying market microstructure phenomena such as liquidity evaporation and flash crashes. It features a realistic limit order book, multiple agent types (market makers, momentum traders, forced liquidators), shock propagation, and 3D visualization of liquidity collapse over time. The app is interactive and built for research, education, and experimentation in financial market dynamics.



## How to fork this project
1. Click the **Fork** button at the top right of the repository page on GitHub.
2. Clone your forked repository to your local machine:
	```
	git clone https://github.com/YOUR-USERNAME/REPO-NAME.git
	```
3. Install requirements and run as described below.

## Structure
- `main.py`: Streamlit entry point
- `order_book.py`: Limit order book logic
- `agents/`: Agent classes (market makers, momentum traders, forced liquidators)
- `simulation.py`: Simulation engine
- `shocks.py`: Shock and liquidity evaporation logic
- `network.py`: NetworkX shock propagation
- `visualization.py`: Plotly 3D/animation
- `ui.py`: Streamlit UI and metrics
- `metrics.py`: Metrics calculations
- `utils.py`: Helpers

