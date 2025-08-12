import tkinter as tk
from tkinter import simpledialog, messagebox
from visualizer import PathfindingVisualizer
import time

# Dummy user database
USERS = {
    "player1": "pass123",
    "player2": "abc456"
}

# Log history function
def log_history(username, action):
    with open("user_history.txt", "a") as file:
        file.write(f"{time.ctime()} | {username} | {action}\n")

# Login screen
def login_screen():
    login = tk.Tk()
    login.title("Login")

    tk.Label(login, text="Username:").grid(row=0, column=0)
    tk.Label(login, text="Password:").grid(row=1, column=0)

    username_entry = tk.Entry(login)
    password_entry = tk.Entry(login, show='*')
    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def authenticate():
        username = username_entry.get()
        password = password_entry.get()
        if USERS.get(username) == password:
            login.destroy()
            log_history(username, "Logged in")
            launch_visualizer(username)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Button(login, text="Login", command=authenticate).grid(row=2, columnspan=2, pady=5)
    login.mainloop()

# Launch visualizer after login
def launch_visualizer(username):
    root = tk.Tk()
    root.title(f"AI Maze Solver - Logged in as {username}")
    
    app = PathfindingVisualizer(root)

    def run_bfs_wrapper():
        log_history(username, "Ran BFS")
        app.run_bfs()
    
    def run_dfs_wrapper():
        log_history(username, "Ran DFS")
        app.run_dfs()

    # Overwrite button functions to log actions
    app.btn_bfs.config(command=run_bfs_wrapper)
    app.btn_dfs.config(command=run_dfs_wrapper)

    root.mainloop()

if __name__ == "__main__":
    login_screen()
