-- Predictions table for baseline and future models
CREATE TABLE IF NOT EXISTS predictions (
    id BIGSERIAL PRIMARY KEY,
    player_id BIGINT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    as_of_date DATE NOT NULL DEFAULT CURRENT_DATE,
    model_name TEXT NOT NULL,
    pred_mean NUMERIC NOT NULL,
    pred_std NUMERIC,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (player_id, model_name, as_of_date)
);

CREATE INDEX IF NOT EXISTS idx_predictions_asof_model ON predictions (as_of_date, model_name);

