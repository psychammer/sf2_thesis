import retro
import numpy as np
import pygame

pygame.init()

env = retro.make(game='StreetFighterIISpecialChampionEdition-Genesis')
obs = env.reset()

# Handle Gymnasium-style reset
if isinstance(obs, tuple):
    obs, info = obs

height, width, channels = obs.shape
screen = pygame.display.set_mode((width * 2, height * 2))
pygame.display.set_caption("Street Fighter II - AI Agent")

clock = pygame.time.Clock()
step = 0

while step < 20000:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            env.close()
            quit()

    action = env.action_space.sample()
    result = env.step(action)

    # Handle both old and new API
    if len(result) == 5:
        obs, reward, terminated, truncated, info = result
        done = terminated or truncated
    else:
        obs, reward, done, info = result

    frame = np.transpose(obs, (1, 0, 2))
    surface = pygame.surfarray.make_surface(frame)
    scaled = pygame.transform.scale(surface, (width * 2, height * 2))
    screen.blit(scaled, (0, 0))
    pygame.display.flip()

    if step % 50 == 0:
        print(f"Step {step}")

    if done:
        reset_result = env.reset()
        obs = reset_result[0] if isinstance(reset_result, tuple) else reset_result

    clock.tick(60)
    step += 1

env.close()
pygame.quit()
print("Done!")
print(info)