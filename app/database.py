"""This module contains the TasksDatabase, which is used to interact with the SQLite database."""

import sqlite3
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
                            created_at TEXT,
                            priority INTEGER
                        )"""
        )
        self.conn.commit()

    def _generate_id(self) -> int:
        """Generate a unique ID for a task."""
        self.cursor.execute("SELECT MAX(id) FROM tasks")
        result = self.cursor.fetchone()
        max_id = result[0] if len(result) else -1
        return max_id + 1

    def create_task(self, task: Task) -> Task:
        """Insert a task into the database."""
        task.task_id = self._generate_id()
        self.cursor.execute(
            """INSERT INTO tasks (id, title, description, status, created_at, priority)
                          VALUES (?, ?, ?, ?, ?, ?)""",
            (
                task.task_id,
                task.title,
                task.description,
                task.status,
                task.created_at,
                task.priority,
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
            created_at=task[4],
            priority=task[5],
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
                created_at=task[4],
                priority=task[5],
            )
            for task in tasks
        ]

    def update_task(self, task_id: int, updated_task: UpdateTask) -> Task:
        """Update a task in the database."""
        update_values = []
        if updated_task.title is not None:
            update_values.append(f"title='{updated_task.title}'")
        if updated_task.description is not None:
            update_values.append(f"description='{updated_task.description}'")
        if updated_task.status is not None:
            update_values.append(f"status='{updated_task.status}'")
        if updated_task.priority is not None:
            update_values.append(f"priority={updated_task.priority.value}")

        if update_values:
            update_query = "UPDATE tasks SET " + ", ".join(update_values) + f" WHERE id={task_id}"
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
                created_at=task[4],
                priority=task[5],
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
