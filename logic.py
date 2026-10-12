import sqlite3


class TaskManager:
    def __init__(self, database):
        self.database = database

    def get_connection(self):
        return sqlite3.connect(self.database)

    def create_table(self):
        with self.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    user_id INTEGER NOT NULL
                )
                """
            )

    def add_task(self, user_id, name, description=""):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO tasks (name, description, user_id)
                VALUES (?, ?, ?)
                """,
                (name, description, user_id)
            )

    def delete_task(self, task_name, user_id):
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                DELETE FROM tasks
                WHERE id = (
                    SELECT id
                    FROM tasks
                    WHERE name = ? AND user_id = ?
                    ORDER BY id
                    LIMIT 1
                )
                """,
                (task_name, user_id)
            )
            return cursor.rowcount > 0

    def show_task_all(self, user_id):
        with self.get_connection() as conn:
            return conn.execute(
                """
                SELECT name
                FROM tasks
                WHERE user_id = ?
                ORDER BY id
                """,
                (user_id,)
            ).fetchall()

    def show_task_many(self, user_id, amount):
        with self.get_connection() as conn:
            return conn.execute(
                """
                SELECT name
                FROM tasks
                WHERE user_id = ?
                ORDER BY id
                LIMIT ?
                """,
                (user_id, amount)
            ).fetchall()
