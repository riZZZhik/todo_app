"""This module defines the routes for the tasks API."""

from fastapi import APIRouter, Depends, status

from ...database import TasksDatabase, get_db
from ...models import Task, UpdateTask

router = APIRouter()


@router.post(
    "",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    name="tasks:create_task",
)
def create_task(task: Task, db: TasksDatabase = Depends(get_db)) -> Task:
    """Create a new task.

    Args:
        task: The task object containing the task details.
        db: The database dependency.

    Returns:
        The created task object.
    """
    return db.create_task(task)


@router.get("/{task_id}", response_model=Task, name="tasks:get_task")
def get_task(task_id: int, db: TasksDatabase = Depends(get_db)) -> Task:
    """Retrieve a task by ID.

    Args:
        task_id: The ID of the task to retrieve.
        db: The database dependency.

    Returns:
        The task with the given ID.
    """
    return db.get_task(task_id)


@router.get("", response_model=list[Task], name="tasks:get_tasks")
def get_tasks(
    sort_by: str | None = None,
    top_n: int | None = None,
    db: TasksDatabase = Depends(get_db),
) -> list[Task]:
    """Retrieve a list of tasks.

    Args:
        sort_by: The field to sort the tasks by. Can be "title", "status", or "created_at".
            Defaults to None.
        top_n: The number of top tasks to retrieve. Defaults to None.
        db: The database dependency.

    Returns:
        A list of tasks.
    """
    tasks = db.get_all_tasks()

    tasks = sorted(tasks, key=lambda task: task.priority, reverse=True)
    if top_n:
        tasks = tasks[:top_n]

    match sort_by:
        case "title":
            tasks.sort(key=lambda task: task.title)
        case "status":
            tasks.sort(key=lambda task: task.status, reverse=True)
        case "created_at":
            tasks.sort(key=lambda task: task.created_at)
        case "updated_at":
            tasks.sort(key=lambda task: task.updated_at)
        case "priority":
            pass
        case _:
            tasks.sort(key=lambda task: task.task_id, reverse=True)

    return tasks


@router.get("/find", response_model=list[Task], name="tasks:find_task")
def find_tasks(
    subtitle: str | None = None,
    subdesc: str | None = None,
    db: TasksDatabase = Depends(get_db),
) -> list[Task]:
    """Find tasks by substring in their description.

    Args:
        subtitle: The substring to search for in the task title.
        subdesc: The substring to search for in the task description.
        db: The database dependency.

    Returns:
        A list of tasks that match the given substring.
    """
    return db.find_tasks_by_description(subtitle, subdesc)


@router.put(
    "/{task_id}",
    response_model=Task,
    status_code=status.HTTP_202_ACCEPTED,
    name="tasks:update_task",
)
def update_task(
    task_id: int, updated_task: UpdateTask, db: TasksDatabase = Depends(get_db)
) -> Task:
    """Update task with the given task_id in the database.

    Args:
        task_id: The ID of the task to be updated.
        updated_task: The updated task data.

    Returns:
        The updated task.
    """
    return db.update_task(task_id, updated_task)


@router.delete("/{task_id}", name="tasks:delete_task")
def delete_task(task_id: int, db: TasksDatabase = Depends(get_db)) -> dict[str, str]:
    """Delete task by ID.

    Parameters:
        task_id: The ID of the task to be deleted.
        db: The database dependency.

    Returns:
        A dictionary with a message indicating the task has been deleted.
    """
    db.delete_task(task_id)
    return {"message": f"Task {task_id} deleted"}
