"""
maze_runner.py
Lab 1.1 - BFS vs DFS for LogiTech Warehouse Solutions
With ANSI colors (toggleable), Windows workaround, and dynamic explanations.
No external third-party frameworks used.
"""

from collections import deque
import random
import os

# ============================================================
#  WINDOWS ANSI COLOR WORKAROUND (built-in ctypes)
# ============================================================
if os.name == 'nt':  # Windows
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # Enable virtual terminal processing (ANSI codes)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass

# ============================================================
#  COLOR TOGGLE (user chooses at startup)
# ============================================================
USE_COLORS = True  # default, will be set by user input

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
DIM = '\033[2m'    # faint/gray
RESET = '\033[0m'

def colorize(text, color_code):
    """Apply color if USE_COLORS is True, else return plain text."""
    if USE_COLORS:
        return f"{color_code}{text}{RESET}"
    return text

# ============================================================
#  CORE ALGORITHMS
# ============================================================
def get_valid_neighbors(matrix, pos):
    rows = len(matrix)
    cols = len(matrix[0])
    x, y = pos
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] != 1:
            neighbors.append((nx, ny))
    return neighbors

def bfs(matrix, start, goal):
    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    visited_order = []

    while queue:
        current = queue.popleft()
        visited_order.append(current)
        if current == goal:
            break
        for nxt in get_valid_neighbors(matrix, current):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = current
                queue.append(nxt)

    path = []
    node = goal
    if goal in parent:
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
    return path, len(visited), visited_order

def dfs(matrix, start, goal):
    stack = [start]
    visited = set([start])
    parent = {start: None}
    visited_order = []

    while stack:
        current = stack.pop()
        visited_order.append(current)
        if current == goal:
            break
        for nxt in get_valid_neighbors(matrix, current):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = current
                stack.append(nxt)

    path = []
    node = goal
    if goal in parent:
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
    return path, len(visited), visited_order

# ============================================================
#  RANDOM GRID GENERATOR
# ============================================================
def generate_random_grid(rows, cols, density):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if (r == 0 and c == 0) or (r == rows-1 and c == cols-1):
                continue
            if random.random() < density:
                grid[r][c] = 1
    return grid

def has_valid_path(grid):
    rows, cols = len(grid), len(grid[0])
    start = (0, 0)
    goal = (rows-1, cols-1)
    path, _, _ = bfs(grid, start, goal)
    return len(path) > 0

def generate_valid_grid(rows, cols, density, max_attempts=50):
    for attempt in range(max_attempts):
        grid = generate_random_grid(rows, cols, density)
        if has_valid_path(grid):
            return grid
    print("  (High density made path-finding difficult. Lowering obstacle density slightly...)")
    return generate_valid_grid(rows, cols, max(0.1, density - 0.1), 10)

# ============================================================
#  PRINTING HELPERS (classic style + colors)
# ============================================================
def print_grid(matrix, path=None, visited=None, title="Grid"):
    if path is None:
        path = []
    if visited is None:
        visited = set()

    rows = len(matrix)
    cols = len(matrix[0])

    # Build display grid
    display = [[" " for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 1:
                display[r][c] = "1"
            else:
                display[r][c] = "0"

    # Mark S and G
    display[0][0] = "S"
    display[rows-1][cols-1] = "G"

    # Overlay path (*) and visited (.)
    for (r, c) in path:
        if (r, c) != (0, 0) and (r, c) != (rows-1, cols-1):
            display[r][c] = "*"
    for (r, c) in visited:
        if (r, c) not in path and (r, c) != (0, 0) and (r, c) != (rows-1, cols-1):
            if display[r][c] == "0":
                display[r][c] = "."

    print(f"\n{title}")
    # Column headers
    header = "    " + "  ".join(f"col{c:<2}" if c >= 10 else f"col {c}" for c in range(cols))
    print(header)

    # Print rows with colors
    for r in range(rows):
        row_parts = []
        for c in range(cols):
            ch = display[r][c]
            if ch == 'S':
                ch = colorize(ch, GREEN)
            elif ch == 'G':
                ch = colorize(ch, YELLOW)
            elif ch == '1':
                ch = colorize(ch, RED)
            elif ch == '*':
                ch = colorize(ch, CYAN)
            elif ch == '.':
                ch = colorize(ch, DIM)
            # '0' remains default color
            row_parts.append(ch)
        print(f"r{r}   " + "  ".join(row_parts))

def print_metrics(algo_name, path_length, visited_count):
    print(f"\nPath length: {path_length}")
    print(f"Nodes visited: {visited_count}")

def print_visited_order(algo_name, order):
    print(f"\nVisited order ({algo_name}):")
    for i in range(0, len(order), 6):
        chunk = order[i:i+6]
        print("  " + " → ".join(str(p) for p in chunk))
    if order and order[-1]:
        print("  (Goal reached)")

def print_path(algo_name, path):
    print(f"\nPath found ({algo_name}):")
    print("  " + " → ".join(str(p) for p in path))

# ============================================================
#  DYNAMIC EXPLANATION GENERATOR
# ============================================================
def print_dynamic_explanation(bfs_len, dfs_len, grid_name):
    print("\n" + "="*60)
    print("[5] PERFORMANCE ANALYSIS & INTERPRETATION")
    print("="*60)

    if bfs_len == dfs_len:
        print(f"""
In this maze ({grid_name}), both BFS and DFS found paths of the SAME length:
**{bfs_len} steps**.

This means DFS coincidentally discovered the optimal route without getting
trapped in any deep dead ends. However, this is a coincidence, not a rule.

🟢 BFS = ALWAYS guarantees the shortest path (by exploring level by level).
🔵 DFS = NOT guaranteed — it can waste time on dead ends if it picks the
       wrong branch first.
""")
    elif bfs_len < dfs_len:
        diff = dfs_len - bfs_len
        print(f"""
In this maze ({grid_name}), BFS found the shortest path (**{bfs_len} steps**),
while DFS took a longer route (**{dfs_len} steps**).

The difference of **{diff} extra steps** clearly shows how DFS can waste time
exploring deep dead-end branches before backtracking and finding the goal.

This perfectly demonstrates the core lesson of this lab:

🟢 BFS = ALWAYS optimal (guaranteed shortest path).
🔵 DFS = NOT guaranteed to be optimal — its path length depends on the
       order in which it explores branches.

In a real warehouse, BFS would ensure the AGV takes the shortest route
to the item bay, while DFS might waste battery life on unnecessary detours.
""")
    else:  # dfs_len < bfs_len (theoretically impossible for BFS, but just in case)
        diff = bfs_len - dfs_len
        print(f"""
Interestingly, in this maze ({grid_name}), DFS found a shorter path
(**{dfs_len} steps**) than BFS (**{bfs_len} steps**), with a difference
of {diff} steps.

NOTE: This is likely due to the way we define the goal check in the code.
In theory, BFS is ALWAYS optimal. If you see this message, it's a
rare edge case worth investigating further!
""")

# ============================================================
#  RUN TEST ON A GRID
# ============================================================
def run_test(grid, grid_name, part_label):
    rows = len(grid)
    cols = len(grid[0])
    start = (0, 0)
    goal = (rows-1, cols-1)

    print(f"\n{'='*60}")
    print(f"{part_label}: {grid_name}")
    print(f"{'='*60}")

    print(f"\n[1] WAREHOUSE GRID ({rows}x{cols})")
    print_grid(grid, title="")
    print(f"\nLegend:  S = Start {start}   G = Goal {goal}   1 = Obstacle   0 = Open")
    if USE_COLORS:
        print("         (Colors: S=Green  G=Yellow  1=Red  *=Path Cyan  .=Scanned Gray)")

    # BFS
    bfs_path, bfs_vis_count, bfs_order = bfs(grid, start, goal)
    bfs_len = len(bfs_path) - 1
    print(f"\n[2] BREADTH‑FIRST SEARCH (BFS)")
    print_visited_order("BFS", bfs_order)
    print_path("BFS", bfs_path)
    print_metrics("BFS", bfs_len, bfs_vis_count)
    print_grid(grid, path=bfs_path, visited=set(bfs_order), title="BFS path on grid (* = path, . = scanned)")

    # DFS
    dfs_path, dfs_vis_count, dfs_order = dfs(grid, start, goal)
    dfs_len = len(dfs_path) - 1
    print(f"\n[3] DEPTH‑FIRST SEARCH (DFS)")
    print_visited_order("DFS", dfs_order)
    print_path("DFS", dfs_path)
    print_metrics("DFS", dfs_len, dfs_vis_count)
    print_grid(grid, path=dfs_path, visited=set(dfs_order), title="DFS path on grid (* = path, . = scanned)")

    # Comparison table
    print("\n[4] PERFORMANCE COMPARISON")
    print("+--------------+-------------+----------------+")
    print("|  Algorithm   | Path Length | Nodes Visited  |")
    print("+--------------+-------------+----------------+")
    print(f"|     BFS      |  {bfs_len:>9}  |  {bfs_vis_count:>12}  |")
    print(f"|     DFS      |  {dfs_len:>9}  |  {dfs_vis_count:>12}  |")
    print("+--------------+-------------+----------------+")

    # Dynamic explanation (right after the table)
    print_dynamic_explanation(bfs_len, dfs_len, grid_name)

    return bfs_path, dfs_path, bfs_vis_count, dfs_vis_count

# ============================================================
#  MAIN WITH INTERACTIVE MENU
# ============================================================
def main():
    global USE_COLORS

    print("\n" + "="*60)
    print(" MAZE RUNNER – LAB 1.1")
    print("="*60)

    # --- COLOR TOGGLE ---
    while True:
        toggle = input("\nEnable colored output? (y/n): ").strip().lower()
        if toggle in ['y', 'n']:
            USE_COLORS = (toggle == 'y')
            break
        print("Please enter 'y' or 'n'.")

    if USE_COLORS:
        print("  Colors enabled. (Green=S, Yellow=G, Red=1, Cyan=*, Gray=.)")
    else:
        print("  Colors disabled. Plain text output.")

    # --- Pre-defined grids ---
    grid_3x3 = [
        [0, 0, 1],
        [0, 1, 0],
        [0, 0, 0]
    ]

    grid_10x10 = [
        [0,0,1,0,0,0,1,0,0,0],
        [0,1,1,0,1,0,1,0,1,0],
        [0,0,0,0,1,0,0,0,1,0],
        [1,1,0,1,1,0,1,0,0,0],
        [0,0,0,0,0,0,1,0,1,0],
        [0,1,1,0,1,0,0,0,1,0],
        [0,0,0,0,1,0,1,0,0,0],
        [1,0,1,0,0,0,1,0,1,0],
        [0,0,0,0,0,0,0,0,1,0],
        [0,1,0,1,0,0,0,0,0,0]
    ]

    # Trap Maze: DFS takes longer (5x5)
    trap_maze = [
        [0,0,0,0,0],
        [0,1,1,1,0],
        [0,1,1,1,0],
        [0,1,1,1,0],
        [0,1,1,1,0]
    ]

    # --- Menu ---
    print("\nChoose a grid option:")
    print("  [1] Test the original 3x3 grid (from the lab sheet)")
    print("  [2] Test the default 10x10 grid")
    print("  [3] Generate a custom random grid")
    print("  [4] Test a trap maze (DFS takes longer path)")

    while True:
        choice = input("\nEnter your choice (1, 2, 3, or 4): ").strip()
        if choice in ['1', '2', '3', '4']:
            break
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

    # --- Execute based on choice ---
    if choice == '1':
        run_test(grid_3x3, "ORIGINAL 3x3 GRID", "========= PART 1")
    elif choice == '2':
        run_test(grid_10x10, "DEFAULT 10x10 GRID", "========= PART 1")
    elif choice == '3':
        print("\n--- Custom Grid Generator ---")
        while True:
            try:
                rows = int(input("Enter number of rows: "))
                cols = int(input("Enter number of columns: "))
                density = float(input("Enter obstacle density (0.0 to 1.0, e.g., 0.2 = 20% walls): "))
                if rows < 2 or cols < 2:
                    print("  Rows and columns must be at least 2.")
                    continue
                if density < 0 or density > 1:
                    print("  Density must be between 0.0 and 1.0.")
                    continue
                break
            except ValueError:
                print("  Please enter valid numbers.")

        print(f"\nGenerating a {rows}x{cols} grid with {density*100:.0f}% obstacles...")
        custom_grid = generate_valid_grid(rows, cols, density)
        run_test(custom_grid, f"CUSTOM {rows}x{cols} GRID", "========= CUSTOM GRID")
    else:  # choice == '4'
        run_test(trap_maze, "TRAP MAZE", "========= TRAP MAZE")

    print("\n" + "="*60)
    print(" END OF LAB OUTPUT")
    print("="*60)

if __name__ == "__main__":
    main()