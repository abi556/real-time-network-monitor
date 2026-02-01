import networkx as nx
from datetime import datetime
from data_simulator import DataSimulator
import config

class NetworkBuilder:
    """Manages network construction and updates"""
    def __init__(self):
        self.G = nx.Graph()
        self.simulator = DataSimulator(
            num_nodes=config.INITIAL_NODES,
            network_type=config.NETWORK_TYPE
        )
        self.update_history = []
        self.initialized = False

