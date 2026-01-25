import pygame
import random

from circleshape import CircleShape
from constants import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: int, y: int, radius: int):
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        radius = self.radius - ASTEROID_MIN_RADIUS
        split1 = Asteroid(self.position.x, self.position.y, radius)
        split2 = Asteroid(self.position.x, self.position.y, radius)

        rot = random.randint(20, 50)
        split1.velocity = (self.velocity * 1.2).rotate(rot)
        split2.velocity = (self.velocity * 1.2).rotate(-rot)
