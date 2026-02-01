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
        
        # Extract node positions
        node_x = [pos[node][0] for node in self.G.nodes()]
        node_y = [pos[node][1] for node in self.G.nodes()]
        
        # Create edge traces
        edge_x = []
        edge_y = []
        for edge in self.G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=config.EDGE_WIDTH, color='#888'),
            hoverinfo='none',
            mode='lines',
            name='Edges'
        )
        
        # Prepare node information
        node_info = []
        node_sizes = []
        node_colors = []
        
        # Get node colors from communities
        if community_dict:
            num_communities = len(set(community_dict.values())) if community_dict else 1
            colors = plt.cm.Set3(np.linspace(0, 1, max(num_communities, 1)))
            for node in self.G.nodes():
                comm_id = community_dict.get(node, 0)
                node_colors.append(f'rgb({int(colors[comm_id][0]*255)}, '
                                  f'{int(colors[comm_id][1]*255)}, '
                                  f'{int(colors[comm_id][2]*255)})')
        else:
            node_colors = ['lightblue'] * self.G.number_of_nodes()42)
