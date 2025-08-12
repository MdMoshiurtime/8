class VisualWrapper:
    def __init__(self, canvas, core_solver):
        self.canvas = canvas
        self.core_solver = core_solver

    def run_with_animation(self, algo, start, end):
        path = self.core_solver.solve(algo, start, end)
        for index, node in enumerate(path):
            self.canvas.after(index * 50, lambda n=node: self.animate_node(n))
        self.canvas.after(len(path) * 50, lambda: print("Path complete."))

    def animate_node(self, node):
        x, y = node
        self.canvas.itemconfig(self.canvas.grid[x][y], fill="yellow")
