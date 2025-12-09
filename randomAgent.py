# Imports
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import random
import numpy as np

# Game States found from Memory Analysis, using mGBA
PLAYER_HEALTH_HI = 0xC292
PLAYER_HEALTH_LO = 0xC293
PLAYER_WINS = 0xC242

ENEMY_HEALTH_HI = 0xC2FB
ENEMY_HEALTH_LO = 0xC2FC
ENEMY_WINS = 0xC243

# Action Space
ACTION_DO_NOTHING = 0
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_JUMP = 3
ACTION_CROUCH = 4
ACTION_STRONG = 5
ACTION_LIGHT = 6

action_space = [
        ACTION_DO_NOTHING,
    ACTION_MOVE_LEFT,
    ACTION_MOVE_RIGHT,
    ACTION_JUMP,
    ACTION_CROUCH,
    ACTION_STRONG,
    ACTION_LIGHT
]

# Navigates initial menus to select English then 
# start the single player game.
def navigate_to_gameplay(pyboy):
    """
    This function will select the correct language and 
    start the game.
    """
    print("Making menu selections.")

    for _ in range(600):
        pyboy.tick()

    pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
    for _ in range(5):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)

    for _ in range(20):
        pyboy.tick()

    pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
    for _ in range(5):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)

    for _ in range(20):
        pyboy.tick()

    pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
    for _ in range(5):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)

    for _ in range(180):
        pyboy.tick()

    pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
    for _ in range(5):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)


def get_game_state(pyboy):
    """
    Read values from memory and store them in a dictionary.
    """
    player_health = (pyboy.memory[PLAYER_HEALTH_HI] << 8) + pyboy.memory[PLAYER_HEALTH_LO]
    enemy_health = (pyboy.memory[ENEMY_HEALTH_HI] << 8) + pyboy.memory[ENEMY_HEALTH_LO]

    state = {
        "player_health": player_health,
        "enemy_health": enemy_health,
        "player_wins": pyboy.memory[PLAYER_WINS],
        "enemy_wins": pyboy.memory[ENEMY_WINS]
    }
    return state

def calculate_reward(current_game_state, last_game_state):
    """Calculate reward based on delta between states."""

    player_health_delta = current_game_state["player_health"] - last_game_state["player_health"]
    enemy_health_delta = current_game_state["enemy_health"] - last_game_state["enemy_health"]

    reward = 0

    if enemy_health_delta < 0:
        reward += 10
    if player_health_delta < 0:
        reward -= 10
    return reward



q_table = {}

LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
epsilon = 1.0
EPSILON_DECAY = 0.9999
MIN_EPSILON = 0.01

def main():
    # Attempt to open ROM.
    try:
        pyboy = PyBoy('PowerQuest.gb')
    except Exception as e:
        print(f"Error initializing PyBoy: {e}")
        return

    navigate_to_gameplay(pyboy)
    print("PyBoy initialized. Starting the game with the correct loop...")
    
    last_game_state = get_game_state(pyboy)
    while pyboy.tick() != WindowEvent.QUIT:

        current_game_state = get_game_state(pyboy)
        if reward != 0:
            print(f"State: {current_game_state}, Reward: {reward}")
        
        last_game_state = current_game_state

        action = random.choice(action_space)

        if action == ACTION_DO_NOTHING:
            pass
        elif action == ACTION_MOVE_LEFT:
            pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
        elif action == ACTION_MOVE_RIGHT:
            pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
        elif action == ACTION_CROUCH:
            pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
        elif action == ACTION_JUMP:
            pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
        elif action == ACTION_STRONG:
            pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
        elif action == ACTION_LIGHT:
            pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
        for _ in range(10):
            pyboy.tick()
 
        pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
        pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)
        pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
        pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)

    pyboy.stop()
    print("Game window closed. Script finished.")

if __name__ == "__main__":
    main()
