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
            node_colors = ['lightblue'] * self.G.number_of_nodes()
        
        # Get node sizes from centrality
        if centrality_dict:
            max_cent = max(centrality_dict.values()) if centrality_dict.values() else 1
            min_cent = min(centrality_dict.values()) if centrality_dict.values() else 0
            for node in self.G.nodes():
                cent = centrality_dict.get(node, 0)
                if max_cent > min_cent:
                    normalized_cent = (cent - min_cent) / (max_cent - min_cent)
                    size = 5 + normalized_cent * 15
                else:
                    size = 10
                node_sizes.append(size)
        else:
            node_sizes = [10] * self.G.number_of_nodes()
        
        # Create hover text
        for node in self.G.nodes():
            info = f"Node: {node}<br>"
            info += f"Degree: {self.G.degree(node)}<br>"
            if community_dict and node in community_dict:
                info += f"Community: {community_dict[node]}<br>"
            if centrality_dict and node in centrality_dict:
                info += f"Centrality: {centrality_dict[node]:.4f}"
            node_info.append(info)
        
        # Set text based on show_labels parameter
        if show_labels:
            node_text = [str(node) for node in self.G.nodes()]
            node_mode = 'markers+text'
        else:
            node_text = ['' for node in self.G.nodes()]
            node_mode = 'markers'
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode=node_mode,
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            textfont=dict(size=8),
            hovertext=node_info,
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=1, color='black'),
                opacity=0.8
            ),
            name='Nodes'
        )
        
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title=dict(
                    text='Interactive Network Graph',
                    x=0.5,
                    font=dict(size=20)
                ),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white',
                height=600
            )
        )
        
        return fig
