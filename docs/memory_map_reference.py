# =================================================================
# Power Quest - Game Boy Memory Map (public reference copy)
#
# This is a static, no-setup-required copy of what's actually stored in
# the pq_memory_addresses Supabase table (see ../supabase/). The running
# agent reads from Supabase via pq_memory_map.py at the project root;
# this file exists purely so anyone can browse or copy-paste the known
# addresses without a Supabase account. If you edit one, update the other.
#
# All addresses are in hexadecimal format.
# Source: User-provided comprehensive analysis.
# =================================================================

# --- Core Game State ---
# This is the most important flag for controlling the AI's overall behavior.
# C0: Menu or Overworld, C1: Home, C2: Dialog, C3: Combat
GAME_STATE_FLAG = 0xC8B2

GAME_ROUND_NUMBER = 0xC240
GAME_TIMER = 0xC248
GAME_TIMER_TICKS = 0xC249


# --- Player State ---
PLAYER_HEALTH_HI = 0xC292
PLAYER_HEALTH_LO = 0xC293
PLAYER_X_POSITION_HI = 0xC26B # In-fight or Park Kid X-Position
PLAYER_X_POSITION_LO = 0xC26C
PLAYER_Y_POSITION_HI = 0xC26D # In-fight or Park Kid Y-Position
PLAYER_Y_POSITION_LO = 0xC26E
PLAYER_WINS_ROUND = 0xC242
PLAYER_CHARACTER_ID = 0xC28E

# Player Action/Animation State.
# 0x00: Idle, 0x04: Jump, 0x08: Block, 0x0A: Crouch, 0x0C: Taking Damage, 0x1D: Stunned,
# 0x10: A button (Strong), 0x1C: B button (Light)
PLAYER_ACTION_STATE = 0xC27F
PLAYER_ACTION_TIMER = 0xC280 # AKA Stun/Hit Stun Timer

PLAYER_SUPER_BAR_TICKS = 0xC29D
PLAYER_SUPER_BAR_COUNT = 0xC29E


# --- Enemy State ---
ENEMY_HEALTH_HI = 0xC2FB
ENEMY_HEALTH_LO = 0xC2FC
ENEMY_X_POSITION_HI = 0xC2D4 # Opponent in fight or Park Kid 2 X
ENEMY_X_POSITION_LO = 0xC2D5
ENEMY_Y_POSITION_HI = 0xC2D6 # Opponent in fight or Park Kid 2 Y
ENEMY_Y_POSITION_LO = 0xC2D7
ENEMY_WINS_ROUND = 0xC243

ENEMY_ACTION_STATE = 0xC2E8
ENEMY_ACTION_TIMER = 0xC2E9

ENEMY_SUPER_BAR_TICKS = 0xC306
ENEMY_SUPER_BAR_COUNT = 0xC307


# --- Character-Specific & Story Data ---
# These bytes hold data related to story mode and character parts.
STORY_PROGRESSION = 0xCF13 # Note: Marked as 'UNKNOWN' status in analysis file. Appears to repeat for each character.
STORY_WIN_COUNTER = 0xCF14 # Note: Appears to repeat for each character.

MAX_PARTS_A = 0xCF15
MAX_PARTS_B = 0xCF16
GONG_PARTS_A = 0xCF19
GONG_PARTS_B = 0xCF1A
SPEED_PARTS_A = 0xCF1D
SPEED_PARTS_B = 0xCF1E
AXE_PARTS_A = 0xCF21
AXE_PARTS_B = 0xCF22
LON_PARTS_A = 0xCF25
LON_PARTS_B = 0xCF26
