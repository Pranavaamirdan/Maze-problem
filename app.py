import random
from collections import deque # Using deque for efficient queue operations in BFS

# --- Constants ---
GRID_SIZE = 16
GRID_DIM = GRID_SIZE + 2
WALL_DENSITY = 0.35  

# Define positions (x, y)
START_POS = (1, 1)                 
END_POS = (GRID_SIZE, GRID_SIZE)    

# --- 1. Maze Generation ---

def generate_maze():
    """Generates a random 18x18 grid using 1s (walls) and 0s (passages)."""
    maze = []
    
    for y in range(GRID_DIM):
        row = []
        for x in range(GRID_DIM):
            
            # Outer boundary walls (1)
            if x == 0 or x == GRID_DIM - 1 or y == 0 or y == GRID_DIM - 1:
                row.append(1)
            
            # Inner Random Walls (1)
            elif random.random() < WALL_DENSITY:
                row.append(1)
            
            # Passage (0)
            else:
                row.append(0)
                
        maze.append(row)
        
    return maze

# --- 2. Pathfinding Algorithm (Breadth-First Search - BFS) ---

def bfs_solver(maze):
    """
    Finds the shortest path from START_POS to END_POS using BFS.
    Returns the path as a list of (x, y) tuples or None if no path exists.
    """
    
    # Queue for BFS: stores tuples of (x, y, path_history)
    # path_history is needed to reconstruct the path later
    queue = deque([ (START_POS[0], START_POS[1], [START_POS]) ])
    
    # Set to track visited cells to avoid cycles and redundant checks
    visited = {START_POS}
    
    # Directions: Up, Down, Left, Right (dx, dy)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)] 
    
    while queue:
        cx, cy, path = queue.popleft()
        
        if (cx, cy) == END_POS:
            return path # Path found!
        
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            
            # Check if the neighbor is valid:
            # 1. Within bounds
            # 2. Not a wall (value must be 0)
            # 3. Not visited yet
            if 0 <= nx < GRID_DIM and 0 <= ny < GRID_DIM:
                if maze[ny][nx] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    new_path = path + [(nx, ny)]
                    queue.append((nx, ny, new_path))
                    
    return None # No path found

# --- 3. Display Solution ---

def display_solution(maze, path):
    """Prints the maze with the solution path marked by '*'."""
    
    print("\n" + "=" * (GRID_DIM * 2))
    print("🤖 Solution Found:")
    
    for y in range(GRID_DIM):
        row_str = ""
        for x in range(GRID_DIM):
            position = (x, y)
            
            if position == START_POS:
                row_str += "S " # Start
            elif position == END_POS:
                row_str += "E " # End
            elif position in path:
                row_str += "* " # Path
            else:
                row_str += str(maze[y][x]) + " " # Wall (1) or Passage (0)
                
        print(row_str)
        
    print("=" * (GRID_DIM * 2) + "\n")
    print(f"Path Length: {len(path) - 1 if path else 'N/A'}")
    print("1 = Wall, 0 = Passage, S = Start, E = End, * = Path")


# --- Main Execution ---

if __name__ == "__main__":
    
    # We loop until a solvable maze is generated, as the random method doesn't guarantee one.
    path_found = None
    while path_found is None:
        current_maze = generate_maze()
        path_found = bfs_solver(current_maze)
        
        if path_found is None:
            print("Maze generated was unsolvable. Retrying...")

    print("Successfully generated a solvable maze!")
    display_solution(current_maze, path_found)
