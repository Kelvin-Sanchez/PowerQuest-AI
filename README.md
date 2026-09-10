# PowerQuest-AI
This project is on hold since I have had limited time to work on it. Needs heavy work to clean up and I left it in a slightly broken state as it only plays 1 player mode. I wanted to combine forensic techniques along with my exploration of machine learning. Q-learning models are relatively simple to implement so I decided to chose this as a starting point. 

Q learning model aimed at playing Power Quest for GBC. I expected most of the memory addresses to be defined in some public github, but I could not find it. Worse yet even GameShark codes are now difficult to find, which are ultimately what I used as a starting point. If you would like to see what I have discovered please use the link below. I request if you find any error to please send me a message so I can fix it.

https://docs.google.com/spreadsheets/d/15lx8YEUK4b-5sYlNhvxxmbK20SW4R7NoCAj1Fd_A5iY/edit?usp=sharing

This sheet was the source of truth for memory addresses; it's now been migrated into Supabase (see below), which also fixes the codebase's dependency on a `pq_memory_map.py` that didn't exist in this repo.

## Memory Map (Supabase)

Memory addresses now live in a Supabase Postgres table (`pq_memory_addresses`) instead of being hand-maintained in a static file. `pq_memory_map.py` loads every row from that table at import time and exposes it as a module-level constant (e.g. `pq_memory_map.GAME_STATE_FLAG`), so nothing else in the codebase (`game_state.py`, `main.py`) needed to change.

The table has Row Level Security enabled: `anon`/`authenticated` can only `SELECT`, since this is non-sensitive reference data the running game agent needs to read but should never be able to modify. Seeding is the one operation that needs to bypass RLS, so it uses the `service_role` key instead of the public anon key.

Setup:
1. Create a Supabase project and apply `supabase/migrations/20260910145732_create_pq_memory_addresses.sql` against it (via the Supabase CLI, GitHub integration, or pasted into the SQL editor).
2. Set `SUPABASE_URL` and `SUPABASE_KEY` (anon key) as environment variables, or in a local `.env` file (already gitignored — never commit this). This is all `pq_memory_map.py` needs at runtime.
3. To (re)seed the table, also set `SUPABASE_SERVICE_KEY` (service_role key) and run `python supabase/seed_memory_map.py` once. This key should only ever be used locally for this step, never deployed with the running agent.
