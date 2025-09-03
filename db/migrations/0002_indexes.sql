-- Helpful indexes for core tables
CREATE INDEX IF NOT EXISTS idx_players_name ON players (name);
CREATE INDEX IF NOT EXISTS idx_players_team ON players (team);
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches (match_date);
CREATE INDEX IF NOT EXISTS idx_fantasy_points_player_match ON fantasy_points (player_id, match_id);

