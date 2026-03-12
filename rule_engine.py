import numpy as np

# Action button mapping for Street Fighter II (MultiBinary(12))
# [B, A, MODE, START, UP, DOWN, LEFT, RIGHT, C, Y, X, Z]
BUTTONS = {
    'B': 0,      # Light Punch
    'A': 1,      # Light Kick
    'MODE': 2,
    'START': 3,
    'UP': 4,
    'DOWN': 5,
    'LEFT': 6,
    'RIGHT': 7,
    'C': 8,      # Heavy Punch
    'Y': 9,      # Medium Punch
    'X': 10,     # Heavy Kick
    'Z': 11      # Medium Kick
}

def make_action(buttons_pressed):
    """Convert a list of button names into a binary action array."""
    action = [0] * 12
    for btn in buttons_pressed:
        if btn in BUTTONS:
            action[BUTTONS[btn]] = 1
    return action

# ------------------------------------
# Combo Sequences
# Each combo is a list of (action, duration_in_frames)
# ------------------------------------

# Basic jab combo (safe, fast)
COMBO_JAB = [
    (make_action(['B']), 5),
    (make_action([]), 3),
    (make_action(['B']), 5),
    (make_action([]), 3),
    (make_action(['Y']), 8),
]

# Heavy punish combo (use when opponent is stunned)
COMBO_PUNISH = [
    (make_action(['C']), 8),
    (make_action([]), 4),
    (make_action(['X']), 8),
    (make_action([]), 4),
    (make_action(['C']), 10),
]

# Escape move (use when cornered)
COMBO_ESCAPE = [
    (make_action(['UP', 'RIGHT']), 6),
    (make_action([]), 4),
    (make_action(['B']), 5),
]

# Finishing combo (use when enemy is low health)
COMBO_FINISH = [
    (make_action(['C']), 8),
    (make_action([]), 3),
    (make_action(['X']), 8),
    (make_action([]), 3),
    (make_action(['C']), 8),
    (make_action([]), 3),
    (make_action(['X']), 10),
]

# Defensive move (use when agent is low health)
COMBO_DEFEND = [
    (make_action(['LEFT']), 6),
    (make_action(['DOWN', 'LEFT']), 6),
    (make_action(['DOWN']), 6),
]


class RuleEngine:
    def __init__(self):
        self.current_combo = None      # Active combo sequence
        self.combo_step = 0            # Current step in the combo
        self.frame_counter = 0         # Frame counter for current step
        self.last_rule = None          # For logging which rule fired

    def _start_combo(self, combo, rule_name):
        """Start executing a new combo sequence."""
        self.current_combo = combo
        self.combo_step = 0
        self.frame_counter = 0
        self.last_rule = rule_name

    def _execute_combo(self):
        """
        Execute the current step of an active combo.
        Returns the action for this frame, or None if combo is finished.
        """
        if self.current_combo is None:
            return None

        if self.combo_step >= len(self.current_combo):
            # Combo finished
            self.current_combo = None
            self.combo_step = 0
            self.frame_counter = 0
            return None

        action, duration = self.current_combo[self.combo_step]
        self.frame_counter += 1

        if self.frame_counter >= duration:
            # Move to next step
            self.combo_step += 1
            self.frame_counter = 0

        return action

    def get_action(self, info):
        """
        Evaluate the game state and return a rule-based action.
        Returns None if no rule applies (DQN takes over).

        Parameters:
            info (dict): Game state from gym-retro
                         Keys: health, enemy_health, matches_won,
                               enemy_matches_won, score, continuetimer

        Returns:
            action (list or None)
        """

        agent_health = info.get('health', 176)
        enemy_health = info.get('enemy_health', 176)

        # --- If a combo is already running, continue it ---
        if self.current_combo is not None:
            action = self._execute_combo()
            if action is not None:
                return action

        # --- Rule 1: Enemy is stunned (very low health) → Punish combo ---
        if enemy_health <= 20:
            self._start_combo(COMBO_FINISH, 'FINISH')
            return self._execute_combo()

        # --- Rule 2: Agent is critically low on health → Defend ---
        if agent_health <= 30:
            self._start_combo(COMBO_DEFEND, 'DEFEND')
            return self._execute_combo()

        # --- Rule 3: Enemy health is moderate → Punish ---
        if enemy_health <= 80:
            self._start_combo(COMBO_PUNISH, 'PUNISH')
            return self._execute_combo()

        # --- Rule 4: Default → No rule applies, let DQN decide ---
        return None


    def reset(self):
        """Reset the rule engine state at the start of a new episode."""
        self.current_combo = None
        self.combo_step = 0
        self.frame_counter = 0
        self.last_rule = None