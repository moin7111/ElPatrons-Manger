-- View for latest predictions per player/model
CREATE OR REPLACE VIEW predictions_latest AS
SELECT p.*
FROM predictions p
JOIN (
    SELECT player_id, model_name, MAX(as_of_date) AS max_date
    FROM predictions
    GROUP BY player_id, model_name
) t
  ON p.player_id = t.player_id
 AND p.model_name = t.model_name
 AND p.as_of_date = t.max_date;

