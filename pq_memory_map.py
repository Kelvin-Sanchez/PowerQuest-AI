"""
Power Quest - Game Boy Memory Map

Loads confirmed memory addresses from the pq_memory_addresses table in
Supabase (see supabase/migrations/), instead of hardcoding them here. Each
row's `name` becomes a module-level constant, so existing usage elsewhere
in this project (e.g. `pq_memory_map.GAME_STATE_FLAG`) is unchanged.

Requires SUPABASE_URL and SUPABASE_KEY in the environment (or a .env file).
"""

import os as _os
import sys as _sys

from dotenv import load_dotenv as _load_dotenv
from supabase import create_client as _create_client

_load_dotenv()

try:
    _SUPABASE_URL = _os.environ["SUPABASE_URL"]
    _SUPABASE_KEY = _os.environ["SUPABASE_KEY"]
except KeyError as e:
    raise RuntimeError(
        "Missing SUPABASE_URL / SUPABASE_KEY. Set them as environment "
        "variables or in a .env file before importing pq_memory_map."
    ) from e

_client = _create_client(_SUPABASE_URL, _SUPABASE_KEY)
_response = _client.table("pq_memory_addresses").select("name, address").execute()

if not _response.data:
    raise RuntimeError(
        "pq_memory_addresses returned no rows. Has supabase/seed_memory_map.py "
        "been run against this project yet?"
    )

for _row in _response.data:
    setattr(_sys.modules[__name__], _row["name"], _row["address"])
