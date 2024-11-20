import pygame 
import sys
from agent import Agent
from environment import Environment

def main():
    BACKGROUND_COLOR = (255, 255, 255)
    TEXT_COLOR = (0, 0, 0)
    envm = Environment(700, 400)
    agent = Agent(0, 30, 1, envm)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(agent)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        agent.move(keys)

        envm.screen.fill(BACKGROUND_COLOR)

        all_sprites.draw(envm.screen)

        frame_text = envm.font.render(f"Position: {agent.rect.x}, {agent.rect.y}                                                 Speed: {agent.speed}", True, TEXT_COLOR)
        envm.screen.blit(frame_text, (0, 0))


        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
