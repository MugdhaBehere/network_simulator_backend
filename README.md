# Network Routing Simulator Backend

Install & run:

pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000


This is a Network Simulator

        A web-based interactive network simulator that lets you design, visualize, and analyze graphs in real-time. Built with React (Vite) on the frontend and a lightweight backend for graph algorithms, the app provides a clean UI with Material UI controls and dynamic metrics visualization.

Features

1. Graph Construction

        Add, delete, and connect nodes/edges interactively.

        Choose between directed and undirected graphs.

        Assign custom edge weights.

        Generate random dense graphs with configurable parameters.

2. Graph Algorithms

        Supports shortest-path algorithms: Dijkstra, Bellman-Ford, BFS, A*, Floyd–Warshall.

        Visualizes packet routing with animated traversal.

3. Visualization

        Smooth interactive graph rendering (pan, zoom, clustering).

        Playback panel with Play/Pause/Step controls and adjustable speed.

        Highlighted paths for better understanding of algorithm output.

4. Metrics & History

        Tracks performance metrics (execution time, hops).

        Displays results as both a history log and an interactive line chart.

5. Topology Management

        Save and load custom topologies.

        View and select from saved topologies with a neat UI list.

Tech Stack

        Frontend: React (Vite), Material UI, Recharts, ECharts

        Backend: Python/FastAPI for algorithms & persistence
