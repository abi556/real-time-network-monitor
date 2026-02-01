# Network Monitoring Dashboard

Real-time network monitoring and visualization dashboard built with Streamlit.

## Features

- Interactive network visualization with Plotly
- Real-time metrics (Density, Centrality, Clustering, Modularity)
- Filter by Community
- Filter by Centrality (Top K nodes)
- Auto-refresh capability
- Network evolution tracking over time
- Multiple layout algorithms (Spring, Circular, Kamada-Kawai)
- Update history tracking
- Theme support: Choose System, Light, or Dark theme (Settings menu)

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
```bash
cd network_dashboard
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note:** If you have multiple Python environments, make sure you're in the correct one. You can also use:
```bash
python -m pip install -r requirements.txt
```

## Running the Dashboard

### Method 1: Using python -m (Recommended for Windows)
```bash
python -m streamlit run app.py
```

### Method 2: Direct streamlit command (if streamlit is in PATH)
```bash
streamlit run app.py
```

### Method 3: Using py launcher (Windows)
```bash
py -m streamlit run app.py
```

**The dashboard will open in your browser at `http://localhost:8501`**

**Troubleshooting:**
- If `streamlit` command is not recognized, use `python -m streamlit run app.py`
- Make sure you're in the `network_dashboard` directory
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## Configuration

Edit `config.py` to customize:
- **Network generation settings:**
  - `INITIAL_NODES`: Number of nodes in initial network (default: 100)
  - `NETWORK_TYPE`: Type of network to generate ("barabasi_albert", "erdos_renyi", "watts_strogatz")
  
- **Update simulation settings:**
  - `UPDATE_INTERVAL`: Auto-refresh interval in seconds (default: 5)
  - `EDGES_TO_ADD_PER_UPDATE`: Number of edges to add per update (default: 1)
  - `EDGES_TO_REMOVE_PER_UPDATE`: Number of edges to remove per update (default: 0)

- **Visualization settings:**
  - `NODE_SIZE_MULTIPLIER`: Multiplier for node sizes (default: 10)
  - `EDGE_WIDTH`: Width of edges in visualization (default: 0.5)
  - `LAYOUT_ITERATIONS`: Number of iterations for spring layout (default: 50)

- **Metrics calculation:**
  - `CALCULATE_BETWEENNESS`: Whether to calculate betweenness centrality (default: True)
  - `TOP_K_NODES`: Number of top nodes to display (default: 10)

## Usage

### Basic Usage

1. **Start the dashboard:** Run `python -m streamlit run app.py`
2. **View the network:** The main visualization shows the current network state
3. **Refresh manually:** Click "Refresh Now" to simulate network updates
4. **Auto-refresh:** Enable "Auto-refresh" checkbox and set interval

### Changing Theme

The dashboard supports theme switching:

1. **Click the 3-dot menu (☰)** in the top right corner
2. **Select "Settings"**
3. **Go to "Theme" section**
4. **Choose your preferred theme:**
   - **System:** Uses your device's theme (light/dark based on OS settings)
   - **Light:** Always light theme
   - **Dark:** Always dark theme

**Note:** The app defaults to System theme, which automatically matches your device's appearance.

### Features Guide

#### Network Visualization
- **Interactive graph:** Zoom, pan, and hover over nodes for details
- **Node colors:** Colored by community (modularity class)
- **Node sizes:** Sized by degree centrality
- **Layout options:** Choose from Spring, Circular, or Kamada-Kawai layouts

#### Live Metrics Panel
- **Density:** Network density (edges / max possible edges)
- **Average Degree:** Average number of connections per node
- **Clustering:** Average clustering coefficient
- **Modularity:** Community structure quality measure
- **Connectivity:** Shows if network is connected or number of components

#### Filtering
- **By Community:** Select specific communities to display
- **By Centrality:** View top K most central nodes by different centrality measures

#### Network Evolution
- **Time series charts:** Track nodes, edges, and density over time
- **Update history:** View recent network updates (add/remove edges)

## Project Structure

```
network_dashboard/
├── app.py                    # Main Streamlit dashboard
├── config.py                 # Configuration settings
├── data_simulator.py         # Simulated live data generator
├── network_builder.py        # Network construction and updates
├── metrics_calculator.py     # Real-time metrics calculation
├── visualizer.py            # Network visualization
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── .streamlit/
    └── config.toml          # Streamlit theme config
```

## Module Descriptions

### `data_simulator.py`
Simulates live network data updates. Generates initial networks and simulates edge additions/removals over time.

### `network_builder.py`
Manages network construction and state. Handles initialization, updates, and tracks update history.

### `metrics_calculator.py`
Calculates real-time network metrics including:
- Basic metrics (density, average degree, clustering)
- Centrality measures (degree, betweenness, closeness, eigenvector)
- Community detection
- Modularity calculation

### `visualizer.py`
Creates interactive Plotly network visualizations with customizable layouts and styling.

### `app.py`
Main Streamlit application that integrates all modules and provides the user interface.

## Testing

### Test Checklist

- [x] Dashboard loads successfully
- [x] Network visualization displays correctly
- [x] Metrics calculate accurately
- [x] Auto-refresh works
- [x] Manual refresh works
- [x] Community filtering works
- [x] Centrality filtering works
- [x] Network evolution charts update
- [x] Update history displays correctly
- [x] Different network types work
- [x] Different layout algorithms work
- [x] Edge cases handled (empty network, single node)

### Testing Different Scenarios

1. **Small network:** Set `INITIAL_NODES = 20` in config.py
2. **Large network:** Set `INITIAL_NODES = 500` in config.py
3. **Different network types:** Change `NETWORK_TYPE` in config.py
4. **Fast updates:** Set `UPDATE_INTERVAL = 1` and enable auto-refresh
5. **Edge removal:** Set `EDGES_TO_REMOVE_PER_UPDATE = 1` in config.py

## Future: Twitter/X API Integration

The code is structured to easily integrate Twitter/X API:

1. **Create `twitter_connector.py`:**
   - Similar interface to `data_simulator.py`
   - Methods: `get_initial_network()`, `get_updates()`
   - Connect to Twitter API v2

2. **Update `network_builder.py`:**
   - Replace `DataSimulator` with `TwitterConnector`
   - All other code remains the same!

3. **Benefits:**
   - Real-time social network data
   - Retweet/reply networks
   - Influence analysis
   - Community detection in social media

## Troubleshooting

### Dashboard won't start
- Check Python version (3.8+ required)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check for port conflicts (default: 8501)

### Network visualization is empty
- Check if network has nodes: Look at "Nodes" metric
- Try clicking "Reset Network"
- Check console for errors

### Metrics not calculating
- Large networks (>1000 nodes) may skip some centrality calculations
- Check `CALCULATE_BETWEENNESS` in config.py
- For very large networks, consider reducing `INITIAL_NODES`

### Auto-refresh not working
- Ensure checkbox is enabled
- Check refresh interval setting
- Browser may need to be active (some browsers pause inactive tabs)

## Performance Notes

- **Small networks (<100 nodes):** All features work perfectly
- **Medium networks (100-500 nodes):** All features work, may be slightly slower
- **Large networks (500-1000 nodes):** Some centrality measures may be disabled
- **Very large networks (>1000 nodes):** Betweenness and closeness centrality disabled for performance

## License

This project is created for educational purposes as part of SECT-4321: Social Network Analysis course.

## Contributors

- Group members working on Track 4: Tool Building project

## Acknowledgments

- NetworkX library for network analysis
- Streamlit for dashboard framework
- Plotly for interactive visualizations
