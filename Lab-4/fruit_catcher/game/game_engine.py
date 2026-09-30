import pygame
from game.basket import Basket
from game.fruit import Fruit
from game.particles import ParticleEmitter

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.basket = Basket(width, height)
        self.fruits = []

        self.score = 0
        self.lives = 3
        self.base_spawn_delay = 750
        self.spawn_delay = self.base_spawn_delay
        self.min_spawn_delay = 300
        self.speed_boost = 0.0
        self.max_speed_boost = 5.0
        self.particles = ParticleEmitter()
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    def update_difficulty(self):
        # Every point makes spawns slightly faster and new fruit slightly quicker.
        self.spawn_delay = max(self.min_spawn_delay, self.base_spawn_delay - self.score * 15)
        self.speed_boost = min(self.max_speed_boost, self.score * 0.12)

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            self.game_state = "GAME_OVER"

    def update(self):
        if self.game_state != "PLAYING":
            return
        self.particles.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.basket.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.basket.move_right()

        now = pygame.time.get_ticks()
        if now - self.last_spawn_time >= self.spawn_delay:
            self.fruits.append(Fruit(self.width, self.speed_boost))
            self.last_spawn_time = now

        basket_rect = self.basket.rect
        for fruit in self.fruits[:]:
            fruit.update()

            if basket_rect.colliderect(fruit.rect):
                if fruit.is_bomb:
                    # Hazard caught: lose a life, no points.
                    self.particles.burst(fruit.x, basket_rect.top, (255, 140, 40), 22)
                    self.lose_life()
                else:
                    self.score += 1
                    self.update_difficulty()
                    self.particles.burst(fruit.x, basket_rect.top, fruit.color)
                self.fruits.remove(fruit)
                continue

            if fruit.is_missed(self.height):
                # Dropped bombs are harmless; dropped fruit costs a life (no score).
                if not fruit.is_bomb:
                    self.particles.burst(fruit.x, self.height - 25, fruit.color)
                    self.lose_life()
                self.fruits.remove(fruit)

    def reset(self):
        self.basket = Basket(self.width, self.height)
        self.fruits.clear()
        self.particles.clear()
        self.score = 0
        self.spawn_delay = self.base_spawn_delay
        self.speed_boost = 0.0
        self.lives = 3
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

    def render(self, screen):
        screen.fill((28, 32, 40))

        ground_y = self.height - 25
        pygame.draw.rect(screen, (45, 50, 60), (0, ground_y, self.width, 25))

        self.basket.render(screen)
        for fruit in self.fruits:
            fruit.render(screen)
        self.particles.render(screen)

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (25, 20))

        lives_surf = self.font_medium.render(f"Lives: {self.lives}", True, (240, 80, 80))
        screen.blit(lives_surf, (self.width - lives_surf.get_width() - 25, 20))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("GAME OVER", True, (235, 70, 70))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_surf = self.font_medium.render(f"Final Score: {self.score}", True, (255, 255, 255))
            screen.blit(final_surf, (self.width // 2 - final_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_medium.render("Press [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))