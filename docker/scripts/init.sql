CREATE TABLE IF NOT EXISTS Note (
        id            SERIAL PRIMARY KEY,
        title         VARCHAR(16)  NOT NULL DEFAULT '',
        content       VARCHAR(255) NOT NULL DEFAULT '',
        completed     BOOLEAN      NOT NULL DEFAULT FALSE,
        created_date  TIMESTAMP    NOT NULL DEFAULT NOW(),
        updated_date  TIMESTAMP    NULL,
        deadline_date TIMESTAMP    NULL
    )