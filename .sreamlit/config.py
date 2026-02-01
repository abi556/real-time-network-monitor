# config.py
# Configuration settings for the dashboard

# Network generation settings
INITIAL_NODES = 100
INITIAL_EDGES_PER_NODE = 3
NETWORK_TYPE = "barabasi_albert"  # Options: "barabasi_albert", "erdos_renyi", "watts_strogatz"

# Update simulation settings
UPDATE_INTERVAL = 5  # seconds
EDGES_TO_ADD_PER_UPDATE = 1
EDGES_TO_REMOVE_PER_UPDATE = 0  # Set to 0 to only add edges

# Visualization settings
NODE_SIZE_MULTIPLIER = 10
EDGE_WIDTH = 0.5
LAYOUT_ITERATIONS = 50

# Metrics calculation
CALCULATE_BETWEENNESS = True  # Set False for large networks (>1000 nodes)
TOP_K_NODES = 10
