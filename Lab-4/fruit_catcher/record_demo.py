"""Headless demo recorder: runs the game on a simulated clock and writes an mp4.
Usage: python record_demo.py before|after out.mp4
Not part of the game itself; used only to produce the lab videos."""
import os, sys, random, subprocess
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame

mode, out = sys.argv[1], sys.argv[2]
random.seed(7)
FPS, SECONDS = 60, 10
pygame.init()
screen = pygame.display.set_mode((600, 500))
frame = 0
pygame.time.get_ticks = lambda: int(frame * 1000 / FPS)   # deterministic clock

from game.game_engine import GameEngine
engine = GameEngine(600, 500)
held = {"l": False, "r": False}

class Keys:
    def __getitem__(self, k):
        return (k in (pygame.K_LEFT, pygame.K_a) and held["l"]) or \
               (k in (pygame.K_RIGHT, pygame.K_d) and held["r"])
pygame.key.get_pressed = lambda: Keys()

def bot():
    held["l"] = held["r"] = False
    if mode == "before":          # idle: fruits fall to the floor
        return
    t = frame / FPS
    good = [f for f in engine.fruits if not getattr(f, "is_bomb", False)]
    bombs = [f for f in engine.fruits if getattr(f, "is_bomb", False)]
    target = max(good, key=lambda f: f.y) if good else None
    if 3.0 < t < 4.0:             # deliberately drift away -> a miss costs a life
        held["l"] = True; return
    if 6.0 < t < 8.5 and bombs:   # deliberately catch a bomb once
        target = max(bombs, key=lambda f: f.y)
        if getattr(engine, "_bomb_hit", False): target = max(good, key=lambda f: f.y) if good else None
    if target:
        cx = engine.basket.x + engine.basket.width / 2
        if target.x < cx - 6: held["l"] = True
        elif target.x > cx + 6: held["r"] = True

ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                       "-s", "600x500", "-r", str(FPS), "-i", "-", "-pix_fmt", "yuv420p", out],
                      stdin=subprocess.PIPE)
for frame in range(FPS * SECONDS):
    bot()
    engine.update()
    engine.render(screen)
    ff.stdin.write(pygame.image.tostring(screen, "RGB"))
ff.stdin.close(); ff.wait()
print("final score", engine.score, "lives", getattr(engine, "lives", None), engine.game_state)
