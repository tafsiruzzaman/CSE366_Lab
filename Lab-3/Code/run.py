import pygame
import sys
import copy  # For deep copying the environment
from agent1 import Agent1
from agent2 import Agent2
from environment import Environment

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 700
GRID_SIZE = 40
STATUS_WIDTH = 600
BACKGROUND_COLOR = (255, 255, 255)
BARRIER_COLOR = (0, 0, 0)       # Barrier color is black
TASK_COLOR = (255, 0, 0)        # Task color is red
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
MOVEMENT_DELAY = 50  # Milliseconds between movements

def reset_simulation(agent1, environment, original_environment_data):
    """Resets the agent1 and restores the environment to its original state."""
    # Reset the agent1's state
    agent1.position = [0, 0]  # Reset to starting position
    agent1.rect.topleft = (0, 0)
    agent1.task_completed = 0
    agent1.completed_tasks = []
    agent1.completed_tasks_with_costs = []
    agent1.total_path_cost = 0
    agent1.path = []
    agent1.moving = False

    # Restore the environment's state
    environment.task_locations = copy.deepcopy(original_environment_data["task_locations"])
    environment.barrier_locations = copy.deepcopy(original_environment_data["barrier_locations"])

def main():
    pygame.init()

    # Set up display with an additional status panel
    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame AI Grid Simulation")

    # Clock to control frame rate
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Initialize environment and agents
    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=10, num_barriers=15)
    agent1 = Agent1(environment, GRID_SIZE)
    agent2 = Agent2(environment, GRID_SIZE)  # Assuming Agent2's logic is implemented in Agent1 but with UCS
    all_sprites = pygame.sprite.Group()
    all_sprites.add(agent1, agent2)

    # Make a backup of the original environment data
    original_environment_data = {
        "task_locations": copy.deepcopy(environment.task_locations),
        "barrier_locations": copy.deepcopy(environment.barrier_locations),
    }

    # Start buttons for both agents
    button_width, button_height = 150, 50
    button1_x = WINDOW_WIDTH + (STATUS_WIDTH - button_width) // 2
    button1_y = WINDOW_HEIGHT // 2 - button_height - 10  # Position for Agent1 button
    button1_rect = pygame.Rect(button1_x, button1_y, button_width, button_height)

    button2_x = button1_x  # Same horizontal position as button1
    button2_y = button1_y + button_height + 20  # Positioned below Agent1 button
    button2_rect = pygame.Rect(button2_x, button2_y, button_width, button_height)

    # Simulation states
    simulation_started = {"Agent1": False, "Agent2": False}
    active_agent = None  # Keeps track of which agent is running

    # Variables for movement delay
    last_move_time = pygame.time.get_ticks()

    # Main loop
    running = True
    while running:
        clock.tick(60)  # Limit to 60 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    # Reset Agent1 and start its simulation
                    reset_simulation(agent1, environment, original_environment_data)
                    simulation_started["Agent1"] = True
                    simulation_started["Agent2"] = False  # Stop Agent2
                    active_agent = agent1
                    if environment.task_locations:
                        agent1.find_nearest_task()

                if button2_rect.collidepoint(event.pos):
                    # Reset Agent2 and start its simulation
                    reset_simulation(agent2, environment, original_environment_data)
                    simulation_started["Agent2"] = True
                    simulation_started["Agent1"] = False  # Stop Agent1
                    active_agent = agent2
                    if environment.task_locations:
                        agent2.find_nearest_task()

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw grid and barriers
        for x in range(environment.columns):
            for y in range(environment.rows):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw grid lines

        # Draw barriers
        for (bx, by) in environment.barrier_locations:
            barrier_rect = pygame.Rect(bx * GRID_SIZE, by * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BARRIER_COLOR, barrier_rect)

        # Draw tasks with numbers
        for (tx, ty), task_number in environment.task_locations.items():
            task_rect = pygame.Rect(tx * GRID_SIZE, ty * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, TASK_COLOR, task_rect)
            # Draw task number
            task_num_surface = font.render(str(task_number), True, (255, 255, 255))
            task_num_rect = task_num_surface.get_rect(center=task_rect.center)
            screen.blit(task_num_surface, task_num_rect)

        # Draw active agent only
        if active_agent == agent1:
            agent2.kill()  # Remove agent2 from the display
            agent1.add(all_sprites)  # Ensure agent1 is in the sprite group
        elif active_agent == agent2:
            agent1.kill()  # Remove agent1 from the display
            agent2.add(all_sprites)  # Ensure agent2 is in the sprite group
        all_sprites.draw(screen)

        # Display simulation information for both agents
        status_x = WINDOW_WIDTH + 10
        line_height = 30
        y_offset = 20

        for agent_name, agent in [("Agent1", agent1), ("Agent2", agent2)]:
            # Display algorithm name
            algorithm_text = f"{agent_name} - Algorithm: {'A* Search' if agent == agent1 else 'UCS'}"
            algorithm_surface = font.render(algorithm_text, True, TEXT_COLOR)
            screen.blit(algorithm_surface, (status_x, y_offset))

            # Display tasks completed
            task_status_text = f"Tasks Completed: {agent.task_completed}"
            task_status_surface = font.render(task_status_text, True, TEXT_COLOR)
            screen.blit(task_status_surface, (status_x, y_offset + line_height))

            # Display agent position
            position_text = f"Position: {agent.position}"
            position_surface = font.render(position_text, True, TEXT_COLOR)
            screen.blit(position_surface, (status_x, y_offset + 2 * line_height))

            # Display completed tasks with costs
            completed_tasks_text = "Completed Tasks: " + ", ".join(
                [f"{task} (Cost: {cost})" for task, cost in agent.completed_tasks_with_costs]
            )
            completed_tasks_surface = font.render(completed_tasks_text, True, TEXT_COLOR)
            screen.blit(completed_tasks_surface, (status_x, y_offset + 3 * line_height))

            # Display total path cost
            total_path_cost_text = f"Total Path Cost: {agent.total_path_cost}"
            total_path_cost_surface = font.render(total_path_cost_text, True, TEXT_COLOR)
            screen.blit(total_path_cost_surface, (status_x, y_offset + 4 * line_height))

            # Increment y_offset for the next agent
            y_offset += 6 * line_height

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()

        # Calculate button positions dynamically based on the displayed information
        y_offset += 10  # Add some space between the last agent's information and the buttons

        # Button 1
        button1_color = BUTTON_HOVER_COLOR if button1_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        button1_rect.top = y_offset  # Dynamically adjust the button's Y position
        pygame.draw.rect(screen, button1_color, button1_rect)
        button1_surface = font.render("A* Search", True, BUTTON_TEXT_COLOR)
        button1_text_rect = button1_surface.get_rect(center=button1_rect.center)
        screen.blit(button1_surface, button1_text_rect)

        # Button 2
        button2_color = BUTTON_HOVER_COLOR if button2_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        button2_rect.top = button1_rect.bottom + 20  # Position button2 below button1
        pygame.draw.rect(screen, button2_color, button2_rect)
        button2_surface = font.render("UCS Search", True, BUTTON_TEXT_COLOR)
        button2_text_rect = button2_surface.get_rect(center=button2_rect.center)
        screen.blit(button2_surface, button2_text_rect)


        # Automatic movement with delay
        current_time = pygame.time.get_ticks()
        if active_agent and simulation_started[f"Agent{'1' if active_agent == agent1 else '2'}"]:
            if current_time - last_move_time > MOVEMENT_DELAY:
                if not active_agent.moving and environment.task_locations:
                    active_agent.find_nearest_task()
                elif active_agent.moving:
                    active_agent.move()
                last_move_time = current_time

        # Draw the status panel separator
        pygame.draw.line(screen, (0, 0, 0), (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Update the display
        pygame.display.flip()

    # Quit Pygame properly
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
