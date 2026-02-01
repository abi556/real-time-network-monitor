# visualizer.py
import networkx as nx
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import config

class NetworkVisualizer:
    """Creates interactive network visualizations"""
    
    def __init__(self, network):
        self.G = network
