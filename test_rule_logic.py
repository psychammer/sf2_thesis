from rule_engine import RuleEngine

rule_engine = RuleEngine()

# Simulate different game states
test_states = [
    {'health': 176, 'enemy_health': 176, 'label': 'Full health both'},
    {'health': 176, 'enemy_health': 78,  'label': 'Enemy moderately hurt'},
    {'health': 176, 'enemy_health': 18,  'label': 'Enemy almost dead'},
    {'health': 25,  'enemy_health': 176, 'label': 'Agent critically low'},
    {'health': 25,  'enemy_health': 18,  'label': 'Both low health'},
]

print("=" * 55)
print("Rule Engine Logic Test")
print("=" * 55)

for state in test_states:
    rule_engine.reset()
    action = rule_engine.get_action(state)

    rule_fired = rule_engine.last_rule if action is not None else 'None (DQN decides)'
    action_taken = action if action is not None else 'Passed to DQN'

    print(f"\nScenario : {state['label']}")
    print(f"HP       : {state['health']} | Enemy HP: {state['enemy_health']}")
    print(f"Rule     : {rule_fired}")
    print(f"Action   : {action_taken}")

print("\n" + "=" * 55)
print("Logic test complete!")