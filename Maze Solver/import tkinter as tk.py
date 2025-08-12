import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import random
from collections import deque

# Login window
class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Login")
        
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        tk.Label(self.frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_btn = ttk.Button(self.frame, text="Login", command=self.check_login)
        self.login_btn.grid(row=2, columnspan=2, pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "123":
            self.frame.destroy()
            self.on_success()
        else:
            messagebox.showerror("Login Failed", "Please try again")


# Pathfinding visua
class PathfindingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pathfinding Visualizer (BFS/DFS)")
        self.rows = 10
        self.cols = 10
        self.maze = []
        self.start = (0, 0)
        self.goal = (9, 9)
        self.setup_controls()
        self.setup_canvas()
        self.generate_maze()

    def setup_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        self.btn_maze = ttk.Button(control_frame, text="Generate Maze", command=self.generate_maze)
        self.btn_maze.pack(side=tk.LEFT, padx=5)

        self.btn_bfs = ttk.Button(control_frame, text="Run BFS", command=self.run_bfs)
        self.btn_bfs.pack(side=tk.LEFT, padx=5)

        self.btn_dfs = ttk.Button(control_frame, text="Run DFS", command=self.run_dfs)
        self.btn_dfs.pack(side=tk.LEFT, padx=5)

        self.btn_compare = ttk.Button(control_frame, text="Run Both (BFS vs DFS)", command=self.run_both)
        self.btn_compare.pack(side=tk.LEFT, padx=5)

        self.lbl_status = ttk.Label(control_frame, text="Ready")
        self.lbl_status.pack(side=tk.LEFT, padx=10)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg='white')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.set_start)
        self.canvas.bind("<Button-3>", self.set_goal)

    def generate_maze(self):
        self.maze = []
        for _ in range(self.rows):
            row = [0 if random.random() > 0.3 else 1 for _ in range(self.cols)]
            self.maze.append(row)
        self.maze[self.start[0]][self.start[1]] = 0
        self.maze[self.goal[0]][self.goal[1]] = 0
        self.draw_maze()
        self.lbl_status.config(text="New maze generated")

    def draw_maze(self):
        self.canvas.delete("all")
        cell_size = 500 // max(self.rows, self.cols)
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * cell_size, r * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                color = 'black' if self.maze[r][c] == 1 else 'white'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                if (r, c) == self.start:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill='green')
                elif (r, c) == self.goal:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill='red')

    def set_start(self, event):
        cell_size = 500 // max(self.rows, self.cols)
        c = event.x // cell_size
        r = event.y // cell_size
        if 0 <= r < self.rows and 0 <= c < self.cols and self.maze[r][c] == 0:
            self.start = (r, c)
            self.draw_maze()
            self.lbl_status.config(text=f"Start set to ({r}, {c})")

    def set_goal(self, event):
        cell_size = 500 // max(self.rows, self.cols)
        c = event.x // cell_size
        r = event.y // cell_size
        if 0 <= r < self.rows and 0 <= c < self.cols and self.maze[r][c] == 0:
            self.goal = (r, c)
            self.draw_maze()
            self.lbl_status.config(text=f"Goal set to ({r}, {c})")

    def run_bfs(self):
        path = self.bfs()
        self.visualize_path(path, "blue")
        self.lbl_status.config(text=f"BFS found path with {len(path)-1} steps" if path else "BFS: No path found")

    def run_dfs(self):
        path = self.dfs()
        self.visualize_path(path, "purple")
        self.lbl_status.config(text=f"DFS found path with {len(path)-1} steps" if path else "DFS: No path found")

    def run_both(self):
        bfs_path = self.bfs()
        dfs_path = self.dfs()

        self.visualize_path(bfs_path, "blue")
        self.visualize_path(dfs_path, "purple")

        if not bfs_path and not dfs_path:
            self.lbl_status.config(text="Both BFS and DFS failed to find a path")
        elif not dfs_path:
            self.lbl_status.config(text="DFS failed; BFS found path with {} steps".format(len(bfs_path)-1))
        elif not bfs_path:
            self.lbl_status.config(text="BFS failed; DFS found path with {} steps".format(len(dfs_path)-1))
        else:
            accuracy = ((len(bfs_path)-1) / (len(dfs_path)-1)) * 100 if len(dfs_path) != 0 else 0
            self.lbl_status.config(
                text=f"BFS: {len(bfs_path)-1} steps, DFS: {len(dfs_path)-1} steps, Accuracy: {accuracy:.2f}%"
            )

    def bfs(self):
        queue = deque([(self.start, [self.start])])
        visited = set()
        while queue:
            (r, c), path = queue.popleft()
            if (r, c) == self.goal:
                return path
            if (r, c) not in visited:
                visited.add((r, c))
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < self.rows and 0 <= nc < self.cols and 
                        self.maze[nr][nc] == 0 and (nr, nc) not in visited):
                        queue.append(((nr, nc), path + [(nr, nc)]))
        return None

    def dfs(self):
        stack = [(self.start, [self.start])]
        visited = set()
        while stack:
            (r, c), path = stack.pop()
            if (r, c) == self.goal:
                return path
            if (r, c) not in visited:
                visited.add((r, c))
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < self.rows and 0 <= nc < self.cols and 
                        self.maze[nr][nc] == 0 and (nr, nc) not in visited):
                        stack.append(((nr, nc), path + [(nr, nc)]))
        return None

    def visualize_path(self, path, color):
        if not path:
            return
        cell_size = 500 // max(self.rows, self.cols)
        offset = 0
        if color == "blue":  # BFS
            offset = -3
        elif color == "purple":  # DFS
            offset = 3

        for i in range(1, len(path)):
            r1, c1 = path[i - 1]
            r2, c2 = path[i]
            x1 = c1 * cell_size + cell_size // 2
            y1 = r1 * cell_size + cell_size // 2
            x2 = c2 * cell_size + cell_size // 2
            y2 = r2 * cell_size + cell_size // 2
            self.canvas.create_line(x1 + offset, y1 + offset, x2 + offset, y2 + offset, fill=color, width=3)

        # Redraw start and goal
        r, c = self.start
        x1, y1 = c * cell_size, r * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill='green')

        r, c = self.goal
        x1, y1 = c * cell_size, r * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill='red')


if __name__ == "__main__":
    root = tk.Tk()

    def start_main_app():
        PathfindingVisualizer(root)

    LoginWindow(root, start_main_app)
    root.mainloop()
