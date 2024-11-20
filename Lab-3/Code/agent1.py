import pygame
import heapq

class Agent1(pygame.sprite.Sprite):
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
        self.total_heuristic = 0  # Store the total Manhattan distance
        self.total_path_cost = 0  # Store the total path cost
        self.completed_tasks_with_costs = []  # Store completed tasks with their costs

    @staticmethod
    def heuristic(a, b):
        """Calculate Manhattan distance."""
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

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
            
            # Calculate cost to reach the task and update total path cost
            path_cost = self.total_heuristic
            self.completed_tasks_with_costs.append((task_number, path_cost))
            self.total_path_cost += path_cost

    def find_nearest_task(self):
        """Find the nearest task based on the shortest path length using A*."""
        nearest_task = None
        shortest_path = None
        for task_position in self.environment.task_locations.keys():
            path, heuristic_value = self.find_path_to(task_position)
            if path:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                    nearest_task = task_position
                    self.total_heuristic = heuristic_value  # Update the total heuristic
        if shortest_path:
            self.path = shortest_path[1:]  # Exclude the current position
            self.moving = True

    def find_path_to(self, target):
        """Find a path to the target position using A* and calculate the total heuristic value."""
        start = tuple(self.position)
        goal = target
        open_set = []
        heapq.heappush(open_set, (0, start, [start], 0))  # Include accumulated heuristic in the tuple
        g_scores = {start: 0}

        while open_set:
            _, current, path, current_heuristic = heapq.heappop(open_set)

            if current == goal:
                return path, current_heuristic

            neighbors = self.get_neighbors(*current)
            for neighbor in neighbors:
                tentative_g_score = g_scores[current] + 1

                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g_score
                    new_heuristic = current_heuristic + self.heuristic(current, neighbor)
                    heapq.heappush(open_set, (tentative_g_score, neighbor, path + [neighbor], new_heuristic))

        return None, 0  # No path found

    def get_neighbors(self, x, y):
        """Get walkable neighboring positions."""
        neighbors = []
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]
        for _, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
