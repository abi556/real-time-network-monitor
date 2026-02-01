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