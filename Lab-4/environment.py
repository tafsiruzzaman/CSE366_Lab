import pygame
import numpy as np


class Environment:
    def __init__(self, num_classes, num_students):
        """
        Initializes the environment with the number of classes, students, and relevant data.
        """
        self.num_classes = num_classes
        self.num_students = num_students
       
        # Randomly generate class durations (1-2 hours) and priorities (scale 1-5)
        self.class_durations = np.random.randint(1, 3, size=num_classes)  # Class duration 1 or 2 hours
        self.class_priorities = np.random.randint(1, 6, size=num_classes)  # Class priority scale 1-5
       
        # Random availability for each student (each student has a list of available time slots)
        self.student_availabilities = np.random.randint(0, 2, size=(num_students, 24))  # 24 possible time slots
       
        # Random preference for each student (how much they prefer a specific time slot)
        self.student_preferences = np.random.randint(1, 6, size=(num_students, 24))  # Preference scale 1-5
        self.pref = np.random.uniform(0.5, 1.5, size=num_students)
       
    def generate_assignments(self):
        """
        Randomly assigns classes to students for the initial generation in the genetic algorithm.
        """
        return [np.random.randint(0, self.num_students, size=self.num_classes) for _ in range(50)]


    def draw_grid(self, screen, font, class_assignments):
        """
        Draws a grid representing the class assignments on the Pygame screen.
        Each row is a student, and each column is a class. Colors represent class durations,
        and the priority and duration are displayed inside the grid.
        """
        screen.fill((255, 255, 255))  # Background color
       
        # Color gradient for durations (1-2 hours)
        color_map = [(0, 0, 255), (0, 0, 139)] 
       
        # Set spacing and margins
        cell_size = 60
        margin_left = 150
        margin_top = 100


        # Display class names on the top (X-axis labels)
        for col in range(self.num_classes):
            class_text = font.render(f"{col + 1}", True, (0, 0, 0))
            screen.blit(class_text, (margin_left + col * cell_size + cell_size // 3, margin_top - 30))


        # Draw each student row with assigned classes
        for row in range(self.num_students):
            # Display student availability on the left of each row
            availability_text = font.render(f"Preference: {self.pref[row]:.2f}", True, (0, 0, 0))
            screen.blit(availability_text, (10, margin_top + row * cell_size + cell_size // 3))


            for col in range(self.num_classes):
                # Determine if this class is assigned to the current student
                assigned_student = class_assignments[col]
               
                # Set color based on class duration (1 or 2 hours)
                color = color_map[self.class_durations[col] - 1] if assigned_student == row else (200, 200, 200)
               
                # Draw the cell (for each student's schedule for each class)
                cell_rect = pygame.Rect(
                    margin_left + col * cell_size,
                    margin_top + row * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(screen, color, cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)  # Draw cell border
               
                # Display class priority and duration inside the cell
                priority_text = font.render(f"P{self.class_priorities[col]}", True, (255, 255, 255) if assigned_student == row else (0, 0, 0))
                duration_text = font.render(f"{self.class_durations[col]}h", True, (255, 255, 255) if assigned_student == row else (0, 0, 0))
                screen.blit(priority_text, (cell_rect.x + 5, cell_rect.y + 5))
                screen.blit(duration_text, (cell_rect.x + 5, cell_rect.y + 25))


                # Highlight conflicts (if a class is assigned to a student when they are not available)
                if self.student_availabilities[row, assigned_student] == 0:
                    conflict_rect = pygame.Rect(cell_rect.x, cell_rect.y, cell_rect.width, cell_rect.height)
                    pygame.draw.rect(screen, (128, 128, 0), conflict_rect, 3)  # Mustard yellow border for conflicts
