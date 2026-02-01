# app.py
import streamlit as st
import networkx as nx
import pandas as pd
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

from network_builder import NetworkBuilder
from metrics_calculator import MetricsCalculator
from visualizer import NetworkVisualizer
import config
# Page configuration
st.set_page_config(
    page_title="Network Monitoring Dashboard",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS with Font Awesome
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .icon {
        margin-right: 8px;
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)
# Initialize session state
if 'network_builder' not in st.session_state:
    st.session_state.network_builder = NetworkBuilder()
    st.session_state.network_builder.initialize_network()

if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

if 'update_history_data' not in st.session_state:
    st.session_state.update_history_data = []

if 'metrics_history' not in st.session_state:
    st.session_state.metrics_history = []
# Title
st.markdown('<h1 class="main-header"><i class="fas fa-project-diagram"></i> Real-Time Network Monitoring Dashboard</h1>', 
            unsafe_allow_html=True)
st.markdown("---")
# Sidebar
st.sidebar.markdown('<h2><i class="fas fa-cog"></i> Dashboard Controls</h2>', unsafe_allow_html=True)

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh", value=False)
refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 1, 60, 5)

# Manual refresh button
if st.sidebar.button("Refresh Now", use_container_width=True):
    updates = st.session_state.network_builder.update_network()
    st.session_state.last_update = datetime.now()
    if updates:
        st.session_state.update_history_data.extend(updates)
    st.rerun()
st.sidebar.markdown("---")

# Network settings
st.sidebar.markdown('<h3><i class="fas fa-network-wired"></i> Network Settings</h3>', unsafe_allow_html=True)
network_type = st.sidebar.selectbox(
    "Network Type",
    ["barabasi_albert", "erdos_renyi", "watts_strogatz"],
    index=0
)

if st.sidebar.button("Reset Network", use_container_width=True):
    st.session_state.network_builder = NetworkBuilder()
    st.session_state.network_builder.initialize_network()
    st.session_state.update_history_data = []
    st.session_state.metrics_history = []
    st.rerun()
st.sidebar.markdown("---")

# Visualization settings
st.sidebar.markdown('<h3><i class="fas fa-palette"></i> Visualization Settings</h3>', unsafe_allow_html=True)
layout_type = st.sidebar.selectbox(
    "Layout Algorithm",
    ["spring", "circular", "kamada_kawai"],
    index=0
)

show_labels = st.sidebar.checkbox("Show Node Labels", value=True)

st.sidebar.markdown("---")
# Get current network
G = st.session_state.network_builder.get_network()

# Calculate metrics
metrics_calc = MetricsCalculator(G)
all_metrics = metrics_calc.get_all_metrics()

# Store metrics history
current_time = datetime.now()
st.session_state.metrics_history.append({
    'timestamp': current_time,
    'nodes': all_metrics['nodes'],
    'edges': all_metrics['edges'],
    'density': all_metrics['density']
})

# Keep only last 100 entries
if len(st.session_state.metrics_history) > 100:
    st.session_state.metrics_history = st.session_state.metrics_history[-100:]
# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h2><i class="fas fa-sitemap"></i> Network Visualization</h2>', unsafe_allow_html=True)
    
    # Detect communities
    community_dict = metrics_calc.detect_communities()
    
    # Calculate centrality
    centrality_metrics = metrics_calc.calculate_centrality_metrics()
    degree_cent = centrality_metrics.get('degree', {})
    
    # Create visualization
    visualizer = NetworkVisualizer(G)
    fig = visualizer.create_plotly_network(
        community_dict=community_dict,
        centrality_dict=degree_cent,
        layout=layout_type,
        show_labels=show_labels
    )
    
    st.plotly_chart(fig, use_container_width=True, height=600)
    
    # Network info
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Nodes", all_metrics['nodes'])
    with col_info2:
        st.metric("Edges", all_metrics['edges'])
    with col_info3:
        st.metric("Communities", len(set(community_dict.values())) if community_dict else 0)

with col2:
    st.markdown('<h2><i class="fas fa-chart-line"></i> Live Metrics</h2>', unsafe_allow_html=True)
    
    # Key metrics
    st.metric("Density", f"{all_metrics['density']:.4f}")
    st.metric("Avg Degree", f"{all_metrics['average_degree']:.2f}")
    st.metric("Clustering", f"{all_metrics['clustering']:.4f}")
    
    if all_metrics['modularity']:
        st.metric("Modularity", f"{all_metrics['modularity']:.4f}")
    
    st.markdown("---")
    
    # Connectivity status
    if all_metrics['is_connected']:
        st.markdown('<div style="color: green;"><i class="fas fa-check-circle"></i> Network is Connected</div>', unsafe_allow_html=True)
        if all_metrics['diameter']:
            st.metric("Diameter", all_metrics['diameter'])
    else:
        st.markdown(f'<div style="color: orange;"><i class="fas fa-exclamation-triangle"></i> {all_metrics["num_components"]} Components</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Last update time
    time_diff = (datetime.now() - st.session_state.last_update).total_seconds()
    st.caption(f"Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}")
    st.caption(f"({int(time_diff)}s ago)")
    
    # Update statistics
    stats = st.session_state.network_builder.get_network_stats()
    st.markdown("---")
    st.caption(f"Total updates: {stats['update_count']}")