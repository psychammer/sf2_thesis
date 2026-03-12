import retro
from rule_engine import RuleEngine

env = retro.make('StreetFighterIISpecialChampionEdition-Genesis')
obs = env.reset()

rule_engine = RuleEngine()
total_steps = 500

print("Testing Rule Engine...\n")

for step in range(total_steps):
    info = env.data.lookup_all()

    # Get action from rule engine
    action = rule_engine.get_action(info)

    if action is not None:
        print(f"Step {step:>4} | Rule fired: {rule_engine.last_rule:<10} | "
              f"HP: {info['health']:>3} | Enemy HP: {info['enemy_health']:>3}")
    else:
        # No rule fired — use random action (DQN placeholder)
        action = env.action_space.sample()

    obs, reward, done, info = env.step(action)

    if done:
        print("\nMatch ended — resetting...\n")
        obs = env.reset()
        rule_engine.reset()

env.close()
print("\nRule Engine test complete!")