import math
import random
import pygame


class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(math.pi, 2 * math.pi)   # burst upward
        speed = random.uniform(1.5, 5.0)
        self.x, self.y = x, y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.radius = random.uniform(2, 4.5)
        self.color = color
        self.life = random.randint(25, 45)
        self.max_life = self.life

    def update(self):
        self.vy += 0.25          # gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    @property
    def alive(self):
        return self.life > 0

    def render(self, surface):
        r = max(1, int(self.radius * self.life / self.max_life))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), r)


class ParticleEmitter:
    """Lightweight emitter: burst() spawns droplets, update()/render() manage them."""

    def __init__(self):
        self.particles = []

    def burst(self, x, y, color, count=14):
        self.particles.extend(Particle(x, y, color) for _ in range(count))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]

    def render(self, surface):
        for p in self.particles:
            p.render(surface)

    def clear(self):
        self.particles.clear()
