import random

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

if __name__ == "__main__":
    maze_size = 3
    print(f"Generating a {maze_size}x{maze_size} maze...")
    
    my_maze = Maze(maze_size)
    
    my_maze.generate_maze()
    
    my_maze.display()