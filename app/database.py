"""This module contains the TasksDatabase, which is used to interact with the SQLite database."""

import sqlite3
from enum import Enum
from typing import Any, Generator

from .models import Task, UpdateTask


class TasksDatabase:
    """A class representing a tasks database."""

    def __init__(self, database_file: str) -> None:
        """Initialize the TasksDatabase instance.

        Args:
            database_file: The path to the SQLite database file.
        """
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        self._create_tasks_table()

    def _create_tasks_table(self) -> None:
        """Create the tasks table if it doesn't exist."""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            description TEXT,
                            status TEXT,
                            priority INTEGER,
                            created_at TEXT,
                            updated_at TEXT
                        )"""
        )
        self.conn.commit()

    def _generate_id(self) -> int:
        """Generate a unique ID for a task."""
        self.cursor.execute("SELECT MAX(id) FROM tasks")
        result = self.cursor.fetchone()
        max_id = result[0] if result[0] else 0
        return max_id + 1

    def create_task(self, task: Task) -> Task:
        """Insert a task into the database."""
        task.task_id = self._generate_id()
        self.cursor.execute(
            """INSERT INTO tasks (id, title, description, status, priority, created_at, updated_at)
                          VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                task.task_id,
                task.title,
                task.description,
                task.status,
                task.priority,
                task.created_at,
                task.updated_at,
            ),
        )
        self.conn.commit()

        return task

    def get_task(self, task_id: int) -> Task:
        """Retrieve a task from the database."""
        self.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = self.cursor.fetchone()
        return Task(
            task_id=task[0],
            title=task[1],
            description=task[2],
            status=task[3],
            priority=task[4],
            created_at=task[5],
            updated_at=task[6],
        )

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks from the database."""
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        return [
            Task(
                task_id=task[0],
                title=task[1],
                description=task[2],
                status=task[3],
                priority=task[4],
                created_at=task[5],
                updated_at=task[6],
            )
            for task in tasks
        ]

    def update_task(self, task_id: int, updated_task: UpdateTask) -> Task:
        """Update a task in the database."""
        update_values = []
        for attr in updated_task.model_fields_set | {"updated_at"}:
            value = getattr(updated_task, attr)
            if isinstance(value, Enum):
                value = value.value

            update_values.append(f'{attr} = "{value}"')

        if update_values:
            update_query = (
                "UPDATE tasks SET " + ", ".join(update_values) + f" WHERE id={task_id}"
            )
            self.cursor.execute(update_query)
            self.conn.commit()

        return self.get_task(task_id)

    def delete_task(self, task_id: int) -> None:
        """Delete a task from the database."""
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def find_tasks_by_description(
        self, subtitle: str | None = None, subdesc: str | None = None
    ) -> list[Task]:
        """Find tasks by substring of description."""
        self.cursor.execute(
            "SELECT * FROM tasks WHERE title LIKE ? AND description LIKE ?",
            (f"%{subtitle or ''}%", f"%{subdesc or ''}%"),
        )
        tasks = self.cursor.fetchall()
        return [
            Task(
                task_id=task[0],
                title=task[1],
                description=task[2],
                status=task[3],
                priority=task[4],
                created_at=task[5],
                updated_at=task[6],
            )
            for task in tasks
        ]


def get_db() -> Generator[TasksDatabase, Any, None]:
    """Get a TasksDatabase instance."""
    db = TasksDatabase("tasks.db")
    try:
        yield db
    finally:
        db.conn.close()
