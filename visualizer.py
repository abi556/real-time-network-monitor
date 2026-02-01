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
    
    def create_plotly_network(self, community_dict=None, 
                             centrality_dict=None,
                             layout='spring',
                             show_labels=True):
        """Create interactive Plotly network visualization"""
        
        if self.G.number_of_nodes() == 0:
            # Return empty figure
            fig = go.Figure()
            fig.add_annotation(
                text="Network is empty",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        # Calculate layout
        if layout == 'spring':
            pos = nx.spring_layout(self.G, k=1, iterations=config.LAYOUT_ITERATIONS, seed=42)
        elif layout == 'circular':
            pos = nx.circular_layout(self.G)
        elif layout == 'kamada_kawai':
            try:
                pos = nx.kamada_kawai_layout(self.G)
            except:
                pos = nx.spring_layout(self.G, seed=42)
        else:
            pos = nx.spring_layout(self.G, seed=42)
