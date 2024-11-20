import pygame 
from environment import Environment

class Agent(pygame.sprite.Sprite):
    AGENT_COLOR = (100, 128, 255) 
    def __init__(self, pos_x, pos_y, speed, envm):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(Agent.AGENT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y 
        self.speed = speed
        self.envm = envm
    
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.speed += 1
            self.rect.x =(self.rect.x - self.speed + self.envm.L) % self.envm.L 
        if keys[pygame.K_RIGHT]:
            self.speed += 1
            self.rect.x = (self.rect.x + self.speed) % self.envm.L 
        if keys[pygame.K_UP]:
            self.speed += 1
            self.rect.y = (self.rect.y - self.speed + self.envm.W) % self.envm.W 
        if keys[pygame.K_DOWN]:
            self.speed += 1
            self.rect.y = (self.rect.y + self.speed) % self.envm.W 
        
        temp_x, temp_y = self.envm.limit_position(self.rect.x, self.rect.y)
        self.rect.x, self.rect.y = temp_x, temp_y 
