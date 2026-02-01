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
    
    def initialize_network(self):
        """Initialize network with simulated data"""
        if not self.initialized:
            self.G = self.simulator.generate_initial_network()
            self.initialized = True
            self.update_history.append({
                'type': 'initialize',
                'timestamp': datetime.now(),
                'nodes': self.G.number_of_nodes(),
                'edges': self.G.number_of_edges()
            })
    
    def update_network(self, add_edges=None, remove_edges=None):
        """Update network with new edges"""
        if add_edges is None:
            add_edges = config.EDGES_TO_ADD_PER_UPDATE
        if remove_edges is None:
            remove_edges = config.EDGES_TO_REMOVE_PER_UPDATE
        updates = self.simulator.simulate_update(
         self.G, 
         add_edges=add_edges,
         remove_edges=remove_edges
         )
        self.update_history.extend(updates)
        return updates
    def get_network(self):
        """Return current network copy"""
        return self.G.copy()




