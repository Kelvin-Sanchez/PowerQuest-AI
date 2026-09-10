-- Memory-map table for PowerQuest-AI.
-- Replaces the Google Sheet as the source of truth for known GBC RAM addresses.

create table pq_memory_addresses (
  id serial primary key,
  name text unique not null,        -- Python constant name, e.g. GAME_STATE_FLAG
  address integer not null,         -- decimal value of the hex RAM address
  category text not null,           -- Core Game State / Player State / Enemy State / Story & Character Data
  notes text                        -- known behavior, enum values, or caveats
);

-- This is non-sensitive reference data the AI agent reads at runtime via the
-- anon key, so it should be publicly readable. It should NOT be publicly
-- writable -- only the one-time seed script (using the service_role key,
-- which bypasses RLS) should insert into it.
alter table pq_memory_addresses enable row level security;

create policy "Public read access"
  on pq_memory_addresses
  for select
  to anon, authenticated
  using (true);
