"""
3D Plotly visualization and animation for 3D Liquidity Vacuum & Flash Crash Simulator
"""
import plotly.graph_objs as go
import numpy as np

def plot_liquidity_surface(price_grid, time_grid, bid_depths, ask_depths):
    # bid_depths, ask_depths: shape (n_times, n_prices)
    surface_bid = go.Surface(z=bid_depths, x=price_grid, y=time_grid, colorscale='Blues', name='Bid Depth', showscale=False, opacity=0.7)
    surface_ask = go.Surface(z=ask_depths, x=price_grid, y=time_grid, colorscale='Reds', name='Ask Depth', showscale=False, opacity=0.7)
    layout = go.Layout(
        title='3D Liquidity Surface',
        scene=dict(
            xaxis_title='Price',
            yaxis_title='Time',
            zaxis_title='Liquidity Depth',
        ),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    fig = go.Figure(data=[surface_bid, surface_ask], layout=layout)
    return fig

def animate_liquidity(history, price_grid):
    # history: list of (price_grid, bid_depth, ask_depth)
    frames = []
    for t, (p, bid, ask) in enumerate(history):
        frame = go.Frame(data=[
            go.Surface(z=[bid], x=price_grid, y=[t], colorscale='Blues', showscale=False, opacity=0.7),
            go.Surface(z=[ask], x=price_grid, y=[t], colorscale='Reds', showscale=False, opacity=0.7)
        ], name=str(t))
        frames.append(frame)
    fig = go.Figure(frames=frames)
    return fig
