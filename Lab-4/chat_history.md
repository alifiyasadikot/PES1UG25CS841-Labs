# Lab 4 – Vibe Coding Chat History (PES1UG25CS841, Fruit Catcher Repair Lab)

**Tool used:** Claude (Cowork). Repo: SETAPESU26/64_fruit_catcher (assigned to PES1UG25CS841 in the Sec-F link sheet).

## Prompt 1 – setup
> Use vibe coding tools to fix the broken code and add features (handout + repo-link sheet attached, SRN PES1UG25CS841).

Claude located the repo for my SRN, cloned it and read all files. It confirmed the bug in `game_engine.update()`: a missed fruit did `self.score += 1` and never touched `self.lives`.

## Prompt 2 – "before" evidence
Claude wrote a headless recorder (`record_demo.py`, simulated clock, fixed seed) and recorded `before.mp4` with the basket idle: score climbed to 11 while lives stayed at 3.

## Prompt 3 – implementation (Tasks 1-4, one pass)
- **Task 1:** missed fruit -> `lose_life()` (lives -1, `GAME_OVER` at 0, lives clamped at 0); score only rises on basket catches.
- **Task 2:** `Fruit(is_bomb=...)`, 15% spawn chance, drawn as a dark spiked ball with red core; catching one costs a life and gives no points; a dropped bomb is harmless.
- **Task 3:** `update_difficulty()`: `spawn_delay = max(300, 750 - 15*score)`, `speed_boost = min(5, 0.12*score)` passed to new fruit.
- **Task 4:** new `game/particles.py` (`Particle`, `ParticleEmitter`): droplets in the fruit's colour burst at the basket rim on catch and at the floor on a miss; orange burst for bombs. Cleared on reset.

Note: original files use CRLF line endings; Claude restored them so the git diff stays minimal.

## Prompt 4 – verification
Claude asserted with a script: miss -> lives 2, score 0; three misses -> GAME_OVER; R reset -> 3 lives, score 0, no fruit; bomb catch -> -1 life, score 0; missed bomb -> no penalty; score 20 -> delay 450 ms, boost 2.4; catch -> particles exist. All passed. `after.mp4` recorded (catches, one miss, one bomb hit, splashes, rising speed). Frames were viewed to confirm rendering.

## Prompt count
Working solution reached in one implementation pass plus one demo-script tweak (the first bot run ended in Game Over too early).
