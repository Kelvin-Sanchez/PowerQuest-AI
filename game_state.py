import pq_memory_map

class GameState:
    """
    A class to manage reading and interpreting the game's state from memory.
    This acts as a live interface to the emulator's memory.
    """

    def __init__(self, pyboy):
        self.pyboy = pyboy
        self._validate_memory_access()

    def _validate_memory_access(self):
        """Validate that we can access the required memory addresses."""
        try:
            # Test a few key memory addresses
            _ = self.pyboy.memory[pq_memory_map.GAME_STATE_FLAG]
            _ = self.pyboy.memory[pq_memory_map.PLAYER_HEALTH_HI]
            _ = self.pyboy.memory[pq_memory_map.ENEMY_HEALTH_HI]
        except Exception as e:
            raise ValueError(f"Cannot access required memory addresses: {e}")

    def _safe_memory_read(self, address, default=0):
        """Safely read from memory with error handling."""
        try:
            return self.pyboy.memory[address]
        except Exception as e:
            print(f"Warning: Cannot read memory address 0x{address:04X}: {e}")
            return default

    @property
    def player_health(self):
        """This property reads the two health bytes and combines them into a single value."""
        try:
            hi = self._safe_memory_read(pq_memory_map.PLAYER_HEALTH_HI)
            lo = self._safe_memory_read(pq_memory_map.PLAYER_HEALTH_LO)
            return (hi << 8) + lo
        except Exception as e:
            print(f"Error reading player health: {e}")
            return 0
 
    @property
    def enemy_health(self):
        """This property reads the two health bytes and combines them into a single value."""
        try:
            hi = self._safe_memory_read(pq_memory_map.ENEMY_HEALTH_HI)
            lo = self._safe_memory_read(pq_memory_map.ENEMY_HEALTH_LO)
            return (hi << 8) + lo
        except Exception as e:
            print(f"Error reading enemy health: {e}")
            return 0

    @property
    def player_wins(self):
        """This property reads the rounds won for player."""
        return self._safe_memory_read(pq_memory_map.PLAYER_WINS_ROUND)

    @property
    def enemy_wins(self):
        """This property reads the rounds won for enemy."""
        return self._safe_memory_read(pq_memory_map.ENEMY_WINS_ROUND)

    @property
    def player_x_position(self):
        """This property reads player X position in a fight."""
        return self._safe_memory_read(pq_memory_map.PLAYER_X_POSITION_HI)

    @property
    def player_y_position(self):
        """This property reads player Y position in a fight."""
        return self._safe_memory_read(pq_memory_map.PLAYER_Y_POSITION_HI)

    @property
    def enemy_x_position(self):
        """This property reads enemy X position in a fight."""
        return self._safe_memory_read(pq_memory_map.ENEMY_X_POSITION_HI)

    @property
    def enemy_y_position(self):
        """This property reads enemy Y position in a fight."""
        return self._safe_memory_read(pq_memory_map.ENEMY_Y_POSITION_HI)

    @property
    def game_state_flag(self):
        """Get the current game state flag."""
        return self._safe_memory_read(pq_memory_map.GAME_STATE_FLAG)

    def get_discretized_state(self):
        """
        Takes continuous values and puts them into discrete buckets for the Q-Table.
        """
        try:
            if self.player_health > 18000: 
                player_health_bucket = "High"
            elif self.player_health > 6000: 
                player_health_bucket = "Medium"
            else: 
                player_health_bucket = "Low"

            if self.enemy_health > 18000: 
                enemy_health_bucket = "High"
            elif self.enemy_health > 6000: 
                enemy_health_bucket = "Medium"
            else: 
                enemy_health_bucket = "Low"

            distance = abs(self.player_x_position - self.enemy_x_position)
            if distance < 40: 
                distance_bucket = "Close"
            elif distance < 80: 
                distance_bucket = "Mid"
            else: 
                distance_bucket = "Far"

            return (player_health_bucket, enemy_health_bucket, distance_bucket)
        except Exception as e:
            print(f"Error discretizing state: {e}")
            return ("Low", "Low", "Far")  # Default safe state

    def get_state_snapshot(self):
        """
        Takes a snapshot of the current game state and returns it as a dictionary.
        This is useful for saving a state in time to compare against later.
        """
        try:
            return {
                "player_health": self.player_health,
                "enemy_health": self.enemy_health,
                "player_wins": self.player_wins,
                "enemy_wins": self.enemy_wins,
                "player_x_position": self.player_x_position,
                "player_y_position": self.player_y_position,
                "enemy_x_position": self.enemy_x_position,
                "enemy_y_position": self.enemy_y_position,
                "game_state_flag": self.game_state_flag
            }
        except Exception as e:
            print(f"Error getting state snapshot: {e}")
            return {
                "player_health": 0,
                "enemy_health": 0,
                "player_wins": 0,
                "enemy_wins": 0,
                "player_x_position": 0,
                "player_y_position": 0,
                "enemy_x_position": 0,
                "enemy_y_position": 0,
                "game_state_flag": 0
            }
