SELECT_ONE = "SELECT 1"
SELECT_USER = "SELECT username FROM user_history ORDER BY date DESC LIMIT 1"
CREATE_USER_TABLE = """
CREATE TABLE IF NOT EXISTS user_history
(
    username varchar(50),
    date timestamp
);
"""
# The `%s` is filled in by psycopg2. Never build SQL with .format() or f-strings
# from user input: that allows SQL injection.
INSERT_USER = "INSERT INTO user_history (username, date) VALUES (%s, NOW())"
