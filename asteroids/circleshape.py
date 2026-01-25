from typing import Self

import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, radius: int):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface):
        # must override
        pass

    def update(self, dt: float):
        # must override
        pass

    def collides_with(self, other: Self):
        dist = self.position.distance_to(other.position)
        return dist <= (self.radius + other.radius)
