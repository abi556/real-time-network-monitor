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