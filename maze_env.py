import random
import matplotlib.pyplot as plt
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import Operator
from utils import Direction, make_direction_ket, apply_direction

class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False # flag for generation algorithm

class Maze:
    def __init__(self, m):
        if m < 2:
            raise ValueError("Maze dimensions must be at least 2x2.")
        self.m = m
        self.grid = [[Room(x, y) for y in range(m)] for x in range(m)]

    def _get_neighbors(self, room):
        neighbors = []
        x, y = room.x, room.y
        
        if y > 0 and not self.grid[x][y-1].visited:
            neighbors.append(self.grid[x][y-1])
        if y < self.m - 1 and not self.grid[x][y+1].visited:
            neighbors.append(self.grid[x][y+1])
        if x < self.m - 1 and not self.grid[x+1][y].visited:
            neighbors.append(self.grid[x+1][y])
        if x > 0 and not self.grid[x-1][y].visited:
            neighbors.append(self.grid[x-1][y])
            
        return neighbors

    def _remove_walls(self, current_room, next_room):
        dx = current_room.x - next_room.x
        dy = current_room.y - next_room.y

        if dx == 1:
            current_room.walls['W'] = False
            next_room.walls['E'] = False
        elif dx == -1:
            current_room.walls['E'] = False
            next_room.walls['W'] = False
        elif dy == 1:
            current_room.walls['N'] = False
            next_room.walls['S'] = False
        elif dy == -1:
            current_room.walls['S'] = False
            next_room.walls['N'] = False

    def generate_maze(self):
        # generating maze w/Recursive backtracker algorithm
        start_x, start_y = random.randint(0, self.m-1), random.randint(0, self.m-1)
        current_room = self.grid[start_x][start_y]
        current_room.visited = True
        
        stack = [current_room]

        while stack:
            current_room = stack[-1]
            neighbors = self._get_neighbors(current_room)
            
            if neighbors:
                next_room = random.choice(neighbors)
                self._remove_walls(current_room, next_room)
                next_room.visited = True
                stack.append(next_room)
            else:
                stack.pop()
        
        for row in self.grid:
            for room in row:
                room.visited = False

    def display(self):
        # just printing the maze in a simple text format
        print(" " + "_" * (self.m * 2 - 1))
        for y in range(self.m):
            line = "|"
            for x in range(self.m):
                line += " " if self.grid[x][y].walls['S'] else "_"
                if self.grid[x][y].walls['E']:
                    line += "|"
                else:
                    line += " "
            print(line)

    def plot(self, start_coords=None, end_coords=None):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect('equal')
        ax.axis('off')

        ax.set_xlim(-0.5, self.m - 0.5)
        ax.set_ylim(-0.5, self.m - 0.5)

        for x in range(self.m):
            for y in range(self.m):
                room = self.grid[x][y]

                plot_y = self.m - 1 - y

                if room.walls['N']:
                    ax.plot([x-0.5, x+0.5], [plot_y+0.5, plot_y+0.5], color='black', lw=2)
                if room.walls['S']:
                    ax.plot([x-0.5, x+0.5], [plot_y-0.5, plot_y-0.5], color='black', lw=2)
                if room.walls['E']:
                    ax.plot([x+0.5, x+0.5], [plot_y-0.5, plot_y+0.5], color='black', lw=2)
                if room.walls['W']:
                    ax.plot([x-0.5, x-0.5], [plot_y-0.5, plot_y+0.5], color='black', lw=2)

        if start_coords:
            ax.plot(start_coords[0], self.m - 1 - start_coords[1], 'go', markersize=10, label='Start')
        if end_coords:
            ax.plot(end_coords[0], self.m - 1 - end_coords[1], 'ro', markersize=10, label='End')

        plt.legend()
        plt.show()
    
    def make_indiv_reg(self):
        pass

    """
    returns an operator
    """
    def _dfs_mir(self, last: Direction, ic: int, jc: int, done: bool, steps_remaining: int) -> Operator:
        invlast = { "N": "S", "S": "N", "E": "W", "W": "E" }[last];
        range_all_qubits = list(range(0, 2*steps_remaining))

        op = QuantumCircuit(2 * steps_remaining);

        if steps_remaining == 0:
            return op
        
        open_directions = []

        for d in ["N", "E", "S", "W"]:
            if not (d == invlast or self.grid[ic][jc].walls[d]):
                open_directions.append(d)  # imagine if i used list comprehension for this...
        
        if len(open_directions) == 0:
            done = True

        if done:
            (i_n, j_n) = apply_direction(invlast, ic, jc)
            
            op.append(make_direction_ket(invlast), [0, 1])
            op.append(
                self._dfs_mir(invlast, i_n, j_n, True, steps_remaining - 1),
                list(range(2, 2*steps_remaining))
            )
            
            Operator(op)
            
            return op
        
        op.append(make_equal_superposition(open_directions), [0, 1])

        for d in open_directions:
            (i_n, j_n) = apply_direction(invlast, ic, jc)

            dfs_n = self._dfs_mir(d, i_n, j_n, False, steps_remaining - 1)
            advance_dfs = lambda ctrl_state : op.append(dfs_n.control(2, ctrl_state=ctrl_state), range_all_qubits)

            match d:
                case "N":
                    advance_dfs("00")
                case "E":
                    advance_dfs("01")
                case "S":
                    advance_dfs("10")
                case "W":
                    advance_dfs("11")

        Operator(op)

        return op


if __name__ == "__main__":
    maze_size = 10
    print(f"Generating a {maze_size}x{maze_size} maze...")
    
    my_maze = Maze(maze_size)
    
    my_maze.generate_maze()
    
    my_maze.display()
    
    print("Displaying graphical plot...")
    my_maze.plot(start_coords=(0, 0), end_coords=(maze_size-1, maze_size-1))