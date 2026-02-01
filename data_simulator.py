# data_simulator.py
import networkx as nx
import random
from datetime import datetime, timedelta
import numpy as np

class DataSimulator:
    """Simulates live network data updates"""
    
    def __init__(self, num_nodes=100, network_type="barabasi_albert"):
        self.num_nodes = num_nodes
        self.network_type = network_type
        self.update_count = 0
        
    def generate_initial_network(self):
        """Generate initial network based on type"""
        if self.network_type == "barabasi_albert":
            G = nx.barabasi_albert_graph(self.num_nodes, 3, seed=42)
        elif self.network_type == "erdos_renyi":
            G = nx.erdos_renyi_graph(self.num_nodes, 0.1, seed=42)
        elif self.network_type == "watts_strogatz":
            G = nx.watts_strogatz_graph(self.num_nodes, 6, 0.3, seed=42)
        else:
            G = nx.barabasi_albert_graph(self.num_nodes, 3, seed=42)
        
        # Add timestamps to edges
        for edge in G.edges():
            G.edges[edge]['timestamp'] = datetime.now() - timedelta(
                days=random.randint(1, 30)
            )
        
        return G
    
    def simulate_update(self, G, add_edges=1, remove_edges=0):
        """Simulate a network update by adding/removing edges"""
        updates = []
        nodes = list(G.nodes())
        
        if len(nodes) < 2:
            return updates
        
        # Add edges
        for _ in range(add_edges):
            # Select two random nodes
            node1, node2 = random.sample(nodes, 2)
            
            # Add edge if it doesn't exist
            if not G.has_edge(node1, node2):
                G.add_edge(node1, node2, timestamp=datetime.now())
                updates.append({
                    'type': 'add',
                    'node1': node1,
                    'node2': node2,
                    'timestamp': datetime.now()
                })
        
        # Remove edges (optional)
        edges = list(G.edges())
        if len(edges) > 0 and remove_edges > 0:
            for _ in range(min(remove_edges, len(edges))):
                edge = random.choice(edges)
                G.remove_edge(edge[0], edge[1])
                updates.append({
                    'type': 'remove',
                    'node1': edge[0],
                    'node2': edge[1],
                    'timestamp': datetime.now()
                })
                edges.remove(edge)
        
        self.update_count += 1
        return updates
    
    def get_update_statistics(self):
        """Get statistics about updates"""
        return {
            'total_updates': self.update_count,
            'last_update': datetime.now()
        }
