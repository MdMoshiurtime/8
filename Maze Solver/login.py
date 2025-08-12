import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import os
from visualizer import PathfindingVisualizer

# Simulated user database
users = {
    "admin": "221",
    "guest": "cse"
}

# Save user actions for history
def log_action(username, action):
    with open("user_history.txt", "a") as f:
        f.write(f"[{datetime.datetime.now()}] {username}: {action}\n")

# Login window
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - AI Maze Solver")
        self.root.geometry("350x200")

        tk.Label(root, text="Username").pack(pady=5)
        self.username_entry = ttk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack(pady=5)
        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.pack()

        self.show_pass = tk.BooleanVar()
        tk.Checkbutton(root, text="Show Password", variable=self.show_pass, command=self.toggle_password).pack()

        ttk.Button(root, text="Login", command=self.login).pack(pady=10)

    def toggle_password(self):
        if self.show_pass.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()

        if user in users and users[user] == pwd:
            log_action(user, "Logged in")
            self.root.destroy()
            launch_visualizer(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# Launch the main visualizer after login
def launch_visualizer(username):
    root = tk.Tk()
    app = PathfindingVisualizer(root)

    # Wrap original methods to log user actions
    original_bfs = app.run_bfs
    original_dfs = app.run_dfs

    def wrapped_bfs():
        original_bfs()
        log_action(username, "Ran BFS")

    def wrapped_dfs():
        original_dfs()
        log_action(username, "Ran DFS")

    app.run_bfs = wrapped_bfs
    app.run_dfs = wrapped_dfs

    root.mainloop()

# Start login window
if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()
