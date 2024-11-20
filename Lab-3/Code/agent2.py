import pygame
import heapq

class Agent2(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  # Agent color is blue
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]  # Starting at the top-left corner of the grid
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []  # List of positions to follow
        self.moving = False  # Flag to indicate if the agent is moving
        self.total_path_cost = 0  # Store the total path cost
        self.completed_tasks_with_costs = []  # Store completed tasks with their costs

    def move(self):
        """Move the agent along the path."""
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.check_task_completion()
        else:
            self.moving = False  # Stop moving when path is exhausted

    def check_task_completion(self):
        """Check if the agent has reached a task location."""
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            self.completed_tasks.append(task_number)
            
            # Use the actual path cost returned by UCS
            path_cost = self.current_task_cost
            self.completed_tasks_with_costs.append((task_number, path_cost))
            self.total_path_cost += path_cost  # Add this task's cost to the total path cost

    def find_nearest_task(self):
        """Find the nearest task based on the shortest path length using UCS."""
        nearest_task = None
        shortest_path = None
        shortest_cost = float('inf')
        for task_position in self.environment.task_locations.keys():
            path, cost = self.find_path_to(task_position)
            if path and cost < shortest_cost:
                shortest_path = path
                nearest_task = task_position
                shortest_cost = cost
        if shortest_path:
            self.path = shortest_path[1:]  # Exclude the current position
            self.current_task_path = shortest_path  # Store the path to calculate the cost
            self.current_task_cost = shortest_cost  # Store the cost of the path
            self.moving = True

    def find_path_to(self, target):
        """Find a path to the target position using Uniform Cost Search (UCS)."""
        start = tuple(self.position)
        goal = target
        queue = [(0, start, [start])]  # (cost, current_position, path_so_far)
        visited = set()

        while queue:
            cost, current, path = heapq.heappop(queue)
            if current not in visited:
                visited.add(current)
                if current == goal:
                    return path, cost  # Return the path and its cost
                neighbors = self.get_neighbors(*current)
                for neighbor in neighbors:
                    # Assume uniform cost of 1 for each step
                    heapq.heappush(queue, (cost + 1, neighbor, path + [neighbor]))
        return None, float('inf')  # No path found


    def get_neighbors(self, x, y):
        """Get walkable neighboring positions."""
        neighbors = []
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]
        for _, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
