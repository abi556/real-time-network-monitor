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
    
    def calculate_centrality_metrics(self, force_recalculate=False):
        """Calculate various centrality measures"""
        if not force_recalculate and self._centrality_cache:
            return self._centrality_cache
        
        metrics = {}
        
        # Degree Centrality (always fast)
        metrics['degree'] = nx.degree_centrality(self.G)
        
        # Betweenness Centrality (slow for large networks)
        if config.CALCULATE_BETWEENNESS and self.G.number_of_nodes() < 1000:
            try:
                metrics['betweenness'] = nx.betweenness_centrality(self.G)
            except:
                metrics['betweenness'] = {}
        else:
            metrics['betweenness'] = {}
        
        # Closeness Centrality (only for connected graphs)
        if nx.is_connected(self.G) and self.G.number_of_nodes() < 500:
            try:
                metrics['closeness'] = nx.closeness_centrality(self.G)
            except:
                metrics['closeness'] = {}
        else:
            metrics['closeness'] = {}
        
        # Eigenvector Centrality
        if self.G.number_of_nodes() < 500:
            try:
                metrics['eigenvector'] = nx.eigenvector_centrality(self.G, max_iter=100)
            except:
                metrics['eigenvector'] = {}
        else:
            metrics['eigenvector'] = {}
        
        self._centrality_cache = metrics
        return metrics
    
    def get_top_central_nodes(self, centrality_type='degree', top_k=None):
        """Get top K most central nodes"""
        if top_k is None:
            top_k = config.TOP_K_NODES
        
        metrics = self.calculate_centrality_metrics()
        
        if centrality_type not in metrics or not metrics[centrality_type]:
            return []
        
        sorted_nodes = sorted(
            metrics[centrality_type].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_nodes[:top_k]
    
    def detect_communities(self, force_recalculate=False):
        """Detect communities using modularity optimization"""
        if not force_recalculate and self._community_cache is not None:
            return self._community_cache
        
        try:
            if self.G.number_of_nodes() < 2:
                return {}
            
            communities = nx.community.greedy_modularity_communities(self.G)
            
            # Create community dictionary
            community_dict = {}
            for i, community in enumerate(communities):
                for node in community:
                    community_dict[node] = i
            
            self._community_cache = community_dict
            return community_dict
        except Exception as e:
            print(f"Community detection error: {e}")
            return {}