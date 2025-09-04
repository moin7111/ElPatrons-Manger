CREATE TABLE IF NOT EXISTS job_runs (
    id BIGSERIAL PRIMARY KEY,
    job_name TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'started',
    details JSONB
);

CREATE INDEX IF NOT EXISTS idx_job_runs_name_time ON job_runs (job_name, started_at DESC);

