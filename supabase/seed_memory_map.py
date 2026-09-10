"""
One-time migration: loads the known PowerQuest memory addresses into the
pq_memory_addresses Supabase table (see supabase/migrations/). Run this once after
creating the table.

Uses the service_role key rather than the anon key, since the table's RLS
policy only grants anon/authenticated SELECT -- inserting requires bypassing
RLS. Requires SUPABASE_URL and SUPABASE_SERVICE_KEY in the environment (or a
.env file). SUPABASE_SERVICE_KEY should only ever be used locally for this
one-time seed step, never embedded in the running game agent.
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

ROWS = [
    # --- Core Game State ---
    {
        "name": "GAME_STATE_FLAG",
        "address": 0xC8B2,
        "category": "Core Game State",
        "notes": "C0: Menu or Overworld, C1: Home, C2: Dialog, C3: Combat",
    },
    {"name": "GAME_ROUND_NUMBER", "address": 0xC240, "category": "Core Game State", "notes": None},
    {"name": "GAME_TIMER", "address": 0xC248, "category": "Core Game State", "notes": None},
    {"name": "GAME_TIMER_TICKS", "address": 0xC249, "category": "Core Game State", "notes": None},

    # --- Player State ---
    {"name": "PLAYER_HEALTH_HI", "address": 0xC292, "category": "Player State", "notes": None},
    {"name": "PLAYER_HEALTH_LO", "address": 0xC293, "category": "Player State", "notes": None},
    {
        "name": "PLAYER_X_POSITION_HI",
        "address": 0xC26B,
        "category": "Player State",
        "notes": "In-fight or Park Kid X-Position",
    },
    {"name": "PLAYER_X_POSITION_LO", "address": 0xC26C, "category": "Player State", "notes": None},
    {
        "name": "PLAYER_Y_POSITION_HI",
        "address": 0xC26D,
        "category": "Player State",
        "notes": "In-fight or Park Kid Y-Position",
    },
    {"name": "PLAYER_Y_POSITION_LO", "address": 0xC26E, "category": "Player State", "notes": None},
    {"name": "PLAYER_WINS_ROUND", "address": 0xC242, "category": "Player State", "notes": None},
    {"name": "PLAYER_CHARACTER_ID", "address": 0xC28E, "category": "Player State", "notes": None},
    {
        "name": "PLAYER_ACTION_STATE",
        "address": 0xC27F,
        "category": "Player State",
        "notes": (
            "0x00: Idle, 0x04: Jump, 0x08: Block, 0x0A: Crouch, 0x0C: Taking Damage, "
            "0x1D: Stunned, 0x10: A button (Strong), 0x1C: B button (Light)"
        ),
    },
    {
        "name": "PLAYER_ACTION_TIMER",
        "address": 0xC280,
        "category": "Player State",
        "notes": "AKA Stun/Hit Stun Timer",
    },
    {"name": "PLAYER_SUPER_BAR_TICKS", "address": 0xC29D, "category": "Player State", "notes": None},
    {"name": "PLAYER_SUPER_BAR_COUNT", "address": 0xC29E, "category": "Player State", "notes": None},

    # --- Enemy State ---
    {"name": "ENEMY_HEALTH_HI", "address": 0xC2FB, "category": "Enemy State", "notes": None},
    {"name": "ENEMY_HEALTH_LO", "address": 0xC2FC, "category": "Enemy State", "notes": None},
    {
        "name": "ENEMY_X_POSITION_HI",
        "address": 0xC2D4,
        "category": "Enemy State",
        "notes": "Opponent in fight or Park Kid 2 X",
    },
    {"name": "ENEMY_X_POSITION_LO", "address": 0xC2D5, "category": "Enemy State", "notes": None},
    {
        "name": "ENEMY_Y_POSITION_HI",
        "address": 0xC2D6,
        "category": "Enemy State",
        "notes": "Opponent in fight or Park Kid 2 Y",
    },
    {"name": "ENEMY_Y_POSITION_LO", "address": 0xC2D7, "category": "Enemy State", "notes": None},
    {"name": "ENEMY_WINS_ROUND", "address": 0xC243, "category": "Enemy State", "notes": None},
    {"name": "ENEMY_ACTION_STATE", "address": 0xC2E8, "category": "Enemy State", "notes": None},
    {"name": "ENEMY_ACTION_TIMER", "address": 0xC2E9, "category": "Enemy State", "notes": None},
    {"name": "ENEMY_SUPER_BAR_TICKS", "address": 0xC306, "category": "Enemy State", "notes": None},
    {"name": "ENEMY_SUPER_BAR_COUNT", "address": 0xC307, "category": "Enemy State", "notes": None},

    # --- Character-Specific & Story Data ---
    {
        "name": "STORY_PROGRESSION",
        "address": 0xCF13,
        "category": "Story & Character Data",
        "notes": "Marked as 'UNKNOWN' status in analysis file. Appears to repeat for each character.",
    },
    {
        "name": "STORY_WIN_COUNTER",
        "address": 0xCF14,
        "category": "Story & Character Data",
        "notes": "Appears to repeat for each character.",
    },
    {"name": "MAX_PARTS_A", "address": 0xCF15, "category": "Story & Character Data", "notes": None},
    {"name": "MAX_PARTS_B", "address": 0xCF16, "category": "Story & Character Data", "notes": None},
    {"name": "GONG_PARTS_A", "address": 0xCF19, "category": "Story & Character Data", "notes": None},
    {"name": "GONG_PARTS_B", "address": 0xCF1A, "category": "Story & Character Data", "notes": None},
    {"name": "SPEED_PARTS_A", "address": 0xCF1D, "category": "Story & Character Data", "notes": None},
    {"name": "SPEED_PARTS_B", "address": 0xCF1E, "category": "Story & Character Data", "notes": None},
    {"name": "AXE_PARTS_A", "address": 0xCF21, "category": "Story & Character Data", "notes": None},
    {"name": "AXE_PARTS_B", "address": 0xCF22, "category": "Story & Character Data", "notes": None},
    {"name": "LON_PARTS_A", "address": 0xCF25, "category": "Story & Character Data", "notes": None},
    {"name": "LON_PARTS_B", "address": 0xCF26, "category": "Story & Character Data", "notes": None},
]


def main():
    client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    result = client.table("pq_memory_addresses").upsert(ROWS, on_conflict="name").execute()
    print(f"Upserted {len(result.data)} rows into pq_memory_addresses.")


if __name__ == "__main__":
    main()
