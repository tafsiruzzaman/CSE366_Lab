import pygame 

class Environment:
    def __init__(self, L, W):
        pygame.init()
        self.L = L 
        self.W = W 
        self.screen = pygame.display.set_mode((L, W))
        pygame.display.set_caption("CSE366 Lab-1")
        self.font = pygame.font.Font(None, 36)

    def limit_position(self, x, y):
        if x < 0:
            x = 0
        if x > self.L:
            x = self.L 
        
        if y < 0:
            y = 0
        if y > self.W:
            y = self.W 
        return x, y