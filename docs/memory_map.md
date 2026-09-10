# Power Quest Memory Map

Public, no-setup-required reference of every confirmed GBC RAM address used by this project. This is the same data stored in the `pq_memory_addresses` Supabase table (see `../supabase/`) and mirrored as plain constants in [`memory_map_reference.py`](memory_map_reference.py) — this table is just the easiest way to browse it.

All addresses are hexadecimal.

## Core Game State

| Name | Address | Notes |
|---|---|---|
| `GAME_STATE_FLAG` | `0xC8B2` | C0: Menu or Overworld, C1: Home, C2: Dialog, C3: Combat |
| `GAME_ROUND_NUMBER` | `0xC240` | |
| `GAME_TIMER` | `0xC248` | |
| `GAME_TIMER_TICKS` | `0xC249` | |

## Player State

| Name | Address | Notes |
|---|---|---|
| `PLAYER_HEALTH_HI` | `0xC292` | |
| `PLAYER_HEALTH_LO` | `0xC293` | |
| `PLAYER_X_POSITION_HI` | `0xC26B` | In-fight or Park Kid X-Position |
| `PLAYER_X_POSITION_LO` | `0xC26C` | |
| `PLAYER_Y_POSITION_HI` | `0xC26D` | In-fight or Park Kid Y-Position |
| `PLAYER_Y_POSITION_LO` | `0xC26E` | |
| `PLAYER_WINS_ROUND` | `0xC242` | |
| `PLAYER_CHARACTER_ID` | `0xC28E` | |
| `PLAYER_ACTION_STATE` | `0xC27F` | 0x00: Idle, 0x04: Jump, 0x08: Block, 0x0A: Crouch, 0x0C: Taking Damage, 0x1D: Stunned, 0x10: A button (Strong), 0x1C: B button (Light) |
| `PLAYER_ACTION_TIMER` | `0xC280` | AKA Stun/Hit Stun Timer |
| `PLAYER_SUPER_BAR_TICKS` | `0xC29D` | |
| `PLAYER_SUPER_BAR_COUNT` | `0xC29E` | |

## Enemy State

| Name | Address | Notes |
|---|---|---|
| `ENEMY_HEALTH_HI` | `0xC2FB` | |
| `ENEMY_HEALTH_LO` | `0xC2FC` | |
| `ENEMY_X_POSITION_HI` | `0xC2D4` | Opponent in fight or Park Kid 2 X |
| `ENEMY_X_POSITION_LO` | `0xC2D5` | |
| `ENEMY_Y_POSITION_HI` | `0xC2D6` | Opponent in fight or Park Kid 2 Y |
| `ENEMY_Y_POSITION_LO` | `0xC2D7` | |
| `ENEMY_WINS_ROUND` | `0xC243` | |
| `ENEMY_ACTION_STATE` | `0xC2E8` | |
| `ENEMY_ACTION_TIMER` | `0xC2E9` | |
| `ENEMY_SUPER_BAR_TICKS` | `0xC306` | |
| `ENEMY_SUPER_BAR_COUNT` | `0xC307` | |

## Story & Character Data

| Name | Address | Notes |
|---|---|---|
| `STORY_PROGRESSION` | `0xCF13` | Marked as 'UNKNOWN' status in analysis file. Appears to repeat for each character. |
| `STORY_WIN_COUNTER` | `0xCF14` | Appears to repeat for each character. |
| `MAX_PARTS_A` | `0xCF15` | |
| `MAX_PARTS_B` | `0xCF16` | |
| `GONG_PARTS_A` | `0xCF19` | |
| `GONG_PARTS_B` | `0xCF1A` | |
| `SPEED_PARTS_A` | `0xCF1D` | |
| `SPEED_PARTS_B` | `0xCF1E` | |
| `AXE_PARTS_A` | `0xCF21` | |
| `AXE_PARTS_B` | `0xCF22` | |
| `LON_PARTS_A` | `0xCF25` | |
| `LON_PARTS_B` | `0xCF26` | |

Found an error or discovered something new? Open an issue or PR — this list grows as more of the game gets reverse-engineered.
