import heapq
import time
import random
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --------------------------
# 1. CORE GRAPH & ALGORITHMS
# --------------------------
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.pos = {}  # For visualization
    
    def add_edge(self, u, v, cost=1):
        if u not in self.edges:
            self.edges[u] = []
        self.edges[u].append((v, cost))
        self.nodes.update([u, v])
    
    def set_positions(self, pos_dict):
        self.pos = pos_dict

class SearchAlgorithm:
    def __init__(self, graph):
        self.graph = graph
        self.visited = set()
        self.path = []
        self.time_taken = 0
    
    def search(self, start, goal):
        raise NotImplementedError

class BFS(SearchAlgorithm):
    def search(self, start, goal):
        start_time = time.time()
        queue = deque([(start, [start])])
        
        while queue:
            node, path = queue.popleft()
            if node == goal:
                self.time_taken = time.time() - start_time
                self.path = path
                return path
            if node not in self.visited:
                self.visited.add(node)
                for neighbor, _ in self.graph.edges.get(node, []):
                    queue.append((neighbor, path + [neighbor]))
        return []

class DFS(SearchAlgorithm):
    def search(self, start, goal):
        start_time = time.time()
        stack = [(start, [start])]
        
        while stack:
            node, path = stack.pop()
            if node == goal:
                self.time_taken = time.time() - start_time
                self.path = path
                return path
            if node not in self.visited:
                self.visited.add(node)
                for neighbor, _ in reversed(self.graph.edges.get(node, [])):
                    stack.append((neighbor, path + [neighbor]))
        return []

class AStar(SearchAlgorithm):
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance
    
    def search(self, start, goal):
        start_time = time.time()
        open_set = []
        heapq.heappush(open_set, (0, start, [start]))
        
        while open_set:
            _, node, path = heapq.heappop(open_set)
            if node == goal:
                self.time_taken = time.time() - start_time
                self.path = path
                return path
            if node not in self.visited:
                self.visited.add(node)
                for neighbor, cost in self.graph.edges.get(node, []):
                    new_path = path + [neighbor]
                    heapq.heappush(open_set, (
                        len(new_path) + self.heuristic(neighbor, goal),
                        neighbor,
                        new_path
                    ))
        return []

# --------------------------
# 2. REAL-WORLD APPLICATIONS
# --------------------------
def generate_maze(rows, cols, obstacle_prob=0.3):
    maze = Graph()
    for r in range(rows):
        for c in range(cols):
            if random.random() > obstacle_prob:
                for dr, dc in [(0,1), (1,0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        maze.add_edge((r,c), (nr,nc))
    # Assign grid positions for visualization
    pos = {(r,c): (c, -r) for r in range(rows) for c in range(cols)}
    maze.set_positions(pos)
    return maze

# --------------------------
# 3. VISUALIZATION & ANALYSIS
# --------------------------
def visualize_graph(graph, path=None, title="Graph Visualization"):
    G = nx.Graph()
    for node in graph.nodes:
        G.add_node(node)
    for u in graph.edges:
        for v, cost in graph.edges[u]:
            G.add_edge(u, v, weight=cost)
    
    plt.figure(figsize=(10, 8))
    pos = graph.pos if graph.pos else nx.spring_layout(G)
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
    if path:
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red')
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    plt.title(title)
    plt.show()

def compare_algorithms(graph, start, goal):
    results = {}
    algorithms = {
        "BFS": BFS(graph),
        "DFS": DFS(graph),
        "A*": AStar(graph)
    }
    
    for name, algo in algorithms.items():
        algo.search(start, goal)
        results[name] = {
            "time": algo.time_taken,
            "path_length": len(algo.path),
            "path": algo.path
        }
    
    # Plot comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    names = list(results.keys())
    times = [results[name]["time"] for name in names]
    lengths = [results[name]["path_length"] for name in names]
    
    ax1.bar(names, times, color=['skyblue', 'lightgreen', 'salmon'])
    ax1.set_title("Time Taken (seconds)")
    
    ax2.bar(names, lengths, color=['skyblue', 'lightgreen', 'salmon'])
    ax2.set_title("Path Length (nodes)")
    
    plt.tight_layout()
    plt.show()
    
    return results

# --------------------------
# 4. INTERACTIVE GUI (Tkinter)
# --------------------------
class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pathfinding Visualizer")
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)
        
        self.btn_maze = tk.Button(self.frame, text="Generate Maze", command=self.generate_maze)
        self.btn_maze.pack(side=tk.LEFT, padx=5)
        
        self.btn_bfs = tk.Button(self.frame, text="Run BFS", command=lambda: self.run_algorithm("BFS"))
        self.btn_bfs.pack(side=tk.LEFT, padx=5)
        
        self.btn_dfs = tk.Button(self.frame, text="Run DFS", command=lambda: self.run_algorithm("DFS"))
        self.btn_dfs.pack(side=tk.LEFT, padx=5)
        
        self.btn_astar = tk.Button(self.frame, text="Run A*", command=lambda: self.run_algorithm("A*"))
        self.btn_astar.pack(side=tk.LEFT, padx=5)
        
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()
        
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack()
        
        self.graph = None
        self.start = (0, 0)
        self.goal = (9, 9)
    
    def generate_maze(self):
        self.graph = generate_maze(10, 10)
        self.visualize_graph("Generated Maze")
    
    def run_algorithm(self, algo_name):
        if not self.graph:
            self.generate_maze()
        
        if algo_name == "BFS":
            algo = BFS(self.graph)
        elif algo_name == "DFS":
            algo = DFS(self.graph)
        else:
            algo = AStar(self.graph)
        
        path = algo.search(self.start, self.goal)
        self.visualize_graph(f"{algo_name} Path", path)
    
    def visualize_graph(self, title, path=None):
        self.ax.clear()
        G = nx.Graph()
        for node in self.graph.nodes:
            G.add_node(node)
        for u in self.graph.edges:
            for v, _ in self.graph.edges[u]:
                G.add_edge(u, v)
        
        pos = self.graph.pos
        nx.draw(G, pos, ax=self.ax, with_labels=True, node_color='lightblue', node_size=300)
        if path:
            nx.draw_networkx_nodes(G, pos, nodelist=path, ax=self.ax, node_color='red')
            path_edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=self.ax, edge_color='red', width=2)
        
        self.ax.set_title(title)
        self.canvas.draw()

# --------------------------
# MAIN EXECUTION
# --------------------------
if __name__ == "__main__":
    # Option 1: Run GUI
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
    
    # Option 2: Run console-based analysis
    # maze = generate_maze(10, 10)
    # visualize_graph(maze)
    # compare_algorithms(maze, (0,0), (9,9))