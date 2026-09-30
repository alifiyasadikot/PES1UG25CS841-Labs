import random
import pygame

class Fruit:
    BOMB_COLOR = (40, 40, 40)

    def __init__(self, screen_width, speed_boost=0.0, bomb_chance=0.15):
        self.screen_width = screen_width
        self.is_bomb = random.random() < bomb_chance
        self.radius = 14
        self.x = random.randint(30, screen_width - 30)
        self.y = -self.radius * 2
        self.speed = random.uniform(4.0, 6.5) + speed_boost
        if self.is_bomb:
            self.color = self.BOMB_COLOR
        else:
            self.color = random.choice([
                (230, 45, 45),   # Apple
                (245, 140, 30),  # Orange
                (160, 60, 200),  # Grape
            ])

    def update(self):
        self.y += self.speed

    def is_missed(self, screen_height):
        return self.y > screen_height

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def render(self, surface):
        center = (int(self.x), int(self.y))
        if self.is_bomb:
            self._render_bomb(surface, center)
            return
        pygame.draw.circle(surface, self.color, center, self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x - 4), int(self.y - 4)), 3)

    def _render_bomb(self, surface, center):
        cx, cy = center
        pygame.draw.circle(surface, self.BOMB_COLOR, center, self.radius)
        pygame.draw.circle(surface, (90, 90, 90), center, self.radius, width=2)
        # spikes
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
            k = 0.7 if dx and dy else 1.0
            a = (cx + dx * self.radius * k, cy + dy * self.radius * k)
            b = (cx + dx * (self.radius + 5) * k, cy + dy * (self.radius + 5) * k)
            pygame.draw.line(surface, (120, 120, 120), a, b, 3)
        # glowing red core marks it as a hazard
        pygame.draw.circle(surface, (235, 60, 60), (cx, cy), 4)
