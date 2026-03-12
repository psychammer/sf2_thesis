import retro

env = retro.make(game='StreetFighterIISpecialChampionEdition-Genesis')
obs = env.reset()

print("Environment loaded!")
print("Observation shape:", obs.shape)
print("Action space:", env.action_space)
print("Game state variables:", env.data.lookup_all())

# Run 100 random actions
for i in range(100):
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    if i % 20 == 0:
        print(f"Step {i} | Reward: {reward} | Info: {info}")
    if done:
        obs = env.reset()

env.close()
print("Test complete!")