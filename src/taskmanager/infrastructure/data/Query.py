CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS Note (
        id            SERIAL PRIMARY KEY,
        title         VARCHAR(16)  NOT NULL DEFAULT '',
        content       VARCHAR(255) NOT NULL DEFAULT '',
        completed     BOOLEAN      NOT NULL DEFAULT FALSE,
        created_date  TIMESTAMP    NOT NULL DEFAULT NOW(),
        updated_date  TIMESTAMP,
        deadline_date TIMESTAMP
    )
"""

INSERT = """
    INSERT INTO Note (title, content, completed, created_date, updated_date, deadline_date)
    VALUES (%(title)s, %(content)s, %(completed)s, %(created_date)s, %(updated_date)s, %(deadline_date)s)
    RETURNING id
"""

SELECT_BY_ID = """
    SELECT id, title, content, completed, created_date, updated_date, deadline_date
    FROM Note
    WHERE id = %(id)s
"""

EXISTS_BY_ID = """
    SELECT EXISTS (
        SELECT 1 FROM Note WHERE id = %(id)s
    )
"""

SELECT_ALL = """
    SELECT id, title, content, completed, created_date, updated_date, deadline_date
    FROM Note
"""

SET_COMPLETED = """
    UPDATE Note
    SET completed     = %(completed)s,
        deadline_date = %(deadline_date)s
    WHERE id = %(id)s
"""

SELECT_EXPIRED = """
    SELECT id, title, content, completed, created_date, updated_date, deadline_date
    FROM Note
    WHERE deadline_date < %(now)s
"""

UPDATE = """
    UPDATE Note
    SET title         = COALESCE(%(title)s,         title),
        content       = COALESCE(%(content)s,       content),
        completed     = COALESCE(%(completed)s,     completed),
        deadline_date = COALESCE(%(deadline_date)s, deadline_date),
        updated_date  = %(updated_date)s
    WHERE id = %(id)s
    RETURNING *
"""

DELETE_BY_ID = """
    DELETE FROM Note WHERE id = %(id)s
"""

DELETE_ALL = """
    DELETE FROM Note
"""

EXISTS_ANY = """
    SELECT EXISTS (
        SELECT 1 FROM Note
    )
"""