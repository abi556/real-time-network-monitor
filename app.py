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