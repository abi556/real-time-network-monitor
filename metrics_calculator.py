# metrics_calculator.py
import networkx as nx
import numpy as np
from collections import Counter
import config

class MetricsCalculator:
    """Calculates real-time network metrics"""
    
    def __init__(self, network):
        self.G = network
        self._centrality_cache = {}
        self._community_cache = None
    
    def calculate_density(self):
        """Calculate network density"""
        n = self.G.number_of_nodes()
        if n < 2:
            return 0.0
        m = self.G.number_of_edges()
        max_edges = n * (n - 1) / 2
        return m / max_edges if max_edges > 0 else 0.0
    
    def calculate_average_degree(self):
        """Calculate average degree"""
        if self.G.number_of_nodes() == 0:
            return 0.0
        degrees = dict(self.G.degree())
        return sum(degrees.values()) / len(degrees)
    
    def calculate_clustering_coefficient(self):
        """Calculate average clustering coefficient"""
        if self.G.number_of_nodes() == 0:
            return 0.0
        return nx.average_clustering(self.G)