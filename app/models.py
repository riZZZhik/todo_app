"""Defines the models used in the application."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    """Represents the status of a task."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class PriorityEnum(int, Enum):
    """Represents the priority levels for tasks."""

    LOW = 0
    MEDIUM = 1
    HIGH = 2
    URGENT = 3


class Task(BaseModel):
    """Represents a task."""

    task_id: int = -1
    title: str
    description: str
    status: StatusEnum = StatusEnum.TODO
    priority: PriorityEnum = PriorityEnum.LOW
    created_at: str = Field(default_factory=lambda: str(datetime.now()))


class UpdateTask(BaseModel):
    """Represents an update to a task."""

    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: PriorityEnum | None = None
