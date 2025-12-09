# Imports
import numpy as np
import pq_memory_map as memory_map
import random
from pyboy import PyBoy
from pyboy.utils import WindowEvent
from game_state import GameState

# Q-Learning Constants (moved to global scope)
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON_DECAY = 0.9999
MIN_EPSILON = 0.01

# Action Space
ACTION_DO_NOTHING = 0
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_JUMP = 3
ACTION_CROUCH = 4
ACTION_STRONG = 5
ACTION_LIGHT = 6

ACTION_SPACE = [
    ACTION_DO_NOTHING,
    ACTION_MOVE_LEFT,
    ACTION_MOVE_RIGHT,
    ACTION_JUMP,
    ACTION_CROUCH,
    ACTION_STRONG,
    ACTION_LIGHT
]

# Menu navigation constants
MENU_WAIT_LONG = 600
MENU_WAIT_MEDIUM = 180
MENU_WAIT_SHORT = 20
MENU_WAIT_TINY = 5

# Game state constants for better readability
GAME_STATE_MENU = 0xC0
GAME_STATE_HOME = 0xC1
GAME_STATE_DIALOGUE = 0xC2
GAME_STATE_COMBAT = 0xC3

def get_game_state_name(state_flag):
    """Convert game state flag to human-readable name."""
    state_names = {
        GAME_STATE_MENU: "Menu",
        GAME_STATE_HOME: "Home",
        GAME_STATE_DIALOGUE: "Dialogue",
        GAME_STATE_COMBAT: "Combat"
    }
    return state_names.get(state_flag, f"Unknown(0x{state_flag:02X})")


# Navigates initial menus to select English then 
# start the single player game.
def navigate_to_gameplay(pyboy):
    """
    This function will select the correct language and 
    start the game.
    """
    print("Making menu selections.")

    for _ in range(MENU_WAIT_LONG):
        pyboy.tick()

    pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
    for _ in range(MENU_WAIT_TINY):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)

    for _ in range(MENU_WAIT_SHORT):
        pyboy.tick()

    pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
    for _ in range(MENU_WAIT_TINY):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)

    for _ in range(MENU_WAIT_SHORT):
        pyboy.tick()

    pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
    for _ in range(MENU_WAIT_TINY):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)

    for _ in range(MENU_WAIT_MEDIUM):
        pyboy.tick()

    pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
    for _ in range(MENU_WAIT_TINY):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
    for _ in range(MENU_WAIT_SHORT):
        pyboy.tick()
    pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
    for _ in range(MENU_WAIT_TINY):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)


    for _ in range(MENU_WAIT_SHORT):
        pyboy.tick()
    pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
    for _ in range(MENU_WAIT_TINY):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
    for _ in range(MENU_WAIT_SHORT):
        pyboy.tick()
    pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
    for _ in range(MENU_WAIT_TINY):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
    for _ in range(120):
        pyboy.tick()
    pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
    for _ in range(MENU_WAIT_TINY):
        pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)

def calculate_reward_delta(state_key, current_game_state, last_game_state, positive_reward, negative_reward):
    """
    A generic function to calculate reward based on the change in a single state variable.
    
    Args:
        current_state (dict): The current snapshot of the game state.
        last_state (dict): The game state from the previous frame.
        state_key (str): The dictionary key for the state variable to check (e.g., "player_health").
        positive_reward (float): The reward to give for each point of positive change.
        negative_reward (float): The penalty to give for each point of negative change.
        
    Returns:
        float: The calculated reward or penalty.
    """
    try:
        delta = current_game_state[state_key] - last_game_state[state_key]

        if delta > 0:
            return positive_reward * delta
        elif delta < 0:
            return negative_reward * abs(delta)

        return 0
    except KeyError:
        print(f"Warning: State key '{state_key}' not found in game state")
        return 0


def calculate_reward(current_game_state, last_game_state):
    """Calculate reward based on delta between states."""
    try:
        total_reward = -0.01

        total_reward += calculate_reward_delta("enemy_health", current_game_state, last_game_state, 0, 1)
        total_reward += calculate_reward_delta("player_health", current_game_state, last_game_state, 0, -1)
        total_reward += calculate_reward_delta("player_wins", current_game_state, last_game_state, 500, 0)
        total_reward += calculate_reward_delta("enemy_wins", current_game_state, last_game_state, 0, -500)
        
        if total_reward != -0.01:
            print(f"Reward this tick: {total_reward}")
        return total_reward
    except Exception as e:
        print(f"Error calculating reward: {e}")
        return -0.01


def game_state_fight(pyboy, game, q_table, last_game_state, discretized_last_game_state, epsilon):
    """
    Handle the fighting game state using Q-learning.
    
    Args:
        pyboy: PyBoy instance
        game: GameState instance
        q_table: Q-learning table
        last_game_state: Previous game state
        discretized_last_game_state: Previous discretized state
        epsilon: Exploration rate
        
    Returns:
        tuple: Updated q_table, current_game_state, discretized_current_game_state, epsilon
    """
    try:
        # Epsilon-greedy action selection
        if random.uniform(0, 1) < epsilon:
            action = random.choice(ACTION_SPACE)
        else:
            action = np.argmax(q_table[discretized_last_game_state])

        # Execute action
        if action == ACTION_DO_NOTHING:
            for _ in range(10):
                pyboy.tick()
        elif action == ACTION_MOVE_LEFT:
            pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
            for _ in range(10):
                pyboy.tick()
            pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        elif action == ACTION_MOVE_RIGHT:
            pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
            for _ in range(10):
                pyboy.tick()
            pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        elif action == ACTION_CROUCH:
            pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
            for _ in range(10):
                pyboy.tick()
            pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
        elif action == ACTION_JUMP:
            pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
            for _ in range(10):
                pyboy.tick()
            pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)
        elif action == ACTION_STRONG:
            pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
            for _ in range(10):
                pyboy.tick()
            pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
        elif action == ACTION_LIGHT:
            pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
            for _ in range(10):
                pyboy.tick()
            pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)

        # Get current state and calculate reward
        current_game_state = game.get_state_snapshot()
        reward = calculate_reward(current_game_state, last_game_state)
        discretized_current_game_state = game.get_discretized_state()

        # Initialize Q-table entry if needed
        if discretized_current_game_state not in q_table:
            q_table[discretized_current_game_state] = np.zeros(len(ACTION_SPACE))

        # Q-learning update
        old_value = q_table[discretized_last_game_state][action]
        next_max = np.max(q_table[discretized_current_game_state])

        new_value = old_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * next_max - old_value)
        q_table[discretized_last_game_state][action] = new_value

        # Update epsilon
        if epsilon > MIN_EPSILON:
            epsilon *= EPSILON_DECAY
        
        return q_table, current_game_state, discretized_current_game_state, epsilon
        
    except Exception as e:
        print(f"Error in game_state_fight: {e}")
        return q_table, last_game_state, discretized_last_game_state, epsilon


def handle_dialogue(pyboy, game, dialogue_timeout=50):
    """
    Handle dialogue encounters more intelligently.
    
    Args:
        pyboy: PyBoy instance
        game: GameState instance
        dialogue_timeout: Maximum number of ticks to spend in dialogue
        
    Returns:
        bool: True if dialogue was handled successfully, False if timeout
    """
    print(f"Handling dialogue encounter...")
    
    # Try different dialogue handling strategies
    strategies = [
        # Strategy 1: Press A with short delays
        lambda: (pyboy.send_input(WindowEvent.PRESS_BUTTON_A), 
                [pyboy.tick() for _ in range(3)],
                pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)),
        
        # Strategy 2: Press A with longer delays
        lambda: (pyboy.send_input(WindowEvent.PRESS_BUTTON_A),
                [pyboy.tick() for _ in range(10)],
                pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)),
        
        # Strategy 3: Press B instead of A
        lambda: (pyboy.send_input(WindowEvent.PRESS_BUTTON_B),
                [pyboy.tick() for _ in range(5)],
                pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)),
        
        # Strategy 4: Press Start
        lambda: (pyboy.send_input(WindowEvent.PRESS_BUTTON_START),
                [pyboy.tick() for _ in range(5)],
                pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)),
    ]
    
    ticks_in_dialogue = 0
    strategy_index = 0
    consecutive_same_state = 0
    last_state = None
    
    while ticks_in_dialogue < dialogue_timeout:
        current_state = game.game_state_flag
        
        # Check if we're still in dialogue
        if current_state in [GAME_STATE_MENU, GAME_STATE_HOME, GAME_STATE_DIALOGUE]:  # Dialogue states
            if current_state == last_state:
                consecutive_same_state += 1
            else:
                consecutive_same_state = 0
                print(f"Dialogue state changed to: {get_game_state_name(current_state)}")
            
            # If we've been in the same state for too long, try a different strategy
            if consecutive_same_state > 5 and strategy_index < len(strategies):
                try:
                    strategies[strategy_index]()
                    print(f"Tried dialogue strategy {strategy_index + 1} (stuck in {get_game_state_name(current_state)})")
                except Exception as e:
                    print(f"Error with dialogue strategy {strategy_index + 1}: {e}")
                
                strategy_index += 1
                consecutive_same_state = 0
            else:
                # Standard dialogue handling
                pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
                for _ in range(5):
                    pyboy.tick()
                pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
            
            last_state = current_state
            ticks_in_dialogue += 10
        else:
            print(f"Dialogue resolved! New state: {get_game_state_name(current_state)}")
            return True
    
    print(f"Dialogue timeout reached after {dialogue_timeout} ticks")
    return False


def main():
    """Main function to run the PowerQuest AI agent."""
    q_table = {}
    epsilon = 1.0
    consecutive_errors = 0
    max_consecutive_errors = 10

    # Attempt to open ROM.
    try:
        pyboy = PyBoy('PowerQuest.gb')
    except Exception as e:
        print(f"Error initializing PyBoy: {e}")
        return
    
    try:
        game = GameState(pyboy)
    except Exception as e:
        print(f"Error initializing GameState: {e}")
        pyboy.stop()
        return
    
    navigate_to_gameplay(pyboy)
    print("PyBoy initialized. Starting the game with the correct loop...")
    
    last_game_state = game.get_state_snapshot()
    discretized_last_game_state = game.get_discretized_state()

    if discretized_last_game_state not in q_table:
        q_table[discretized_last_game_state] = np.zeros(len(ACTION_SPACE))

    # Main game loop
    while pyboy.tick() != WindowEvent.QUIT:
        try:
            current_state_flag = game.game_state_flag
            state_name = get_game_state_name(current_state_flag)
            print(f"Current game state: {state_name} (0x{current_state_flag:02X})")
            
            if current_state_flag == GAME_STATE_COMBAT:  # Combat state
                q_table, current_game_state, discretized_current_game_state, epsilon = game_state_fight(
                    pyboy, game, q_table, last_game_state, discretized_last_game_state, epsilon
                )
                last_game_state = current_game_state
                discretized_last_game_state = discretized_current_game_state
                consecutive_errors = 0  # Reset error counter on successful combat
            else:
                # Handle dialogue more intelligently
                dialogue_success = handle_dialogue(pyboy, game)
                if dialogue_success:
                    last_game_state = game.get_state_snapshot()
                    discretized_last_game_state = game.get_discretized_state()
                    consecutive_errors = 0  # Reset error counter on successful dialogue
                else:
                    consecutive_errors += 1
                    print(f"Dialogue handling failed (error #{consecutive_errors})")
                    
                    # If we have too many consecutive errors, try to reset
                    if consecutive_errors >= max_consecutive_errors:
                        print("Too many consecutive errors, attempting game reset...")
                        # Try to reset by pressing Start multiple times
                        for _ in range(3):
                            pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
                            for _ in range(10):
                                pyboy.tick()
                            pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)
                        consecutive_errors = 0
                    
        except Exception as e:
            consecutive_errors += 1
            print(f"Error in main loop: {e}")
            if consecutive_errors >= max_consecutive_errors:
                print("Too many errors, stopping execution")
                break
            
    pyboy.stop()
    print("Game window closed. Script finished.")


if __name__ == "__main__":
    main()
