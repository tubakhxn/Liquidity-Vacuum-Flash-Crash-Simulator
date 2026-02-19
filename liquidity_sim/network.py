"""
NetworkX-based shock propagation for 3D Liquidity Vacuum & Flash Crash Simulator
"""
import networkx as nx
import numpy as np

class MarketNetwork:
    def __init__(self, n_agents, coupling=0.1):
        self.n_agents = n_agents
        self.coupling = coupling
        self.G = nx.erdos_renyi_graph(n_agents, coupling)
        for node in self.G.nodes:
            self.G.nodes[node]['stress'] = 0.0

    def propagate_shock(self, shocked_agents, shock_size):
        # Set initial shock
        for agent in shocked_agents:
            self.G.nodes[agent]['stress'] += shock_size
        # Propagate via neighbors
        for agent in shocked_agents:
            for neighbor in self.G.neighbors(agent):
                self.G.nodes[neighbor]['stress'] += shock_size * self.coupling

    def get_stress(self):
        return np.array([self.G.nodes[n]['stress'] for n in range(self.n_agents)])
