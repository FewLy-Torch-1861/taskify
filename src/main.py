import json
import argparse
from os import environ
from pathlib import Path
from typing import List, TypedDict, Union, Any

APP_NAME = "taskify"


class Task(TypedDict):
    id: int
    name: str
    status: Union[str, Any]


def get_task_file_path() -> Path:
    xdg_data = environ.get("XDG_DATA_HOME")

    if xdg_data:
        base_dir = Path(xdg_data)
    else:
        base_dir = Path.home() / ".local" / "share"

    app_dir = base_dir / APP_NAME
    app_dir.mkdir(parents=True, exist_ok=True)

    return app_dir / "tasks.json"


TASK_FILE = get_task_file_path()


def add(tasks_data: List[Task], taskName: str):
    if not tasks_data:
        new_id = 1
    else:
        new_id = max(task["id"] for task in tasks_data) + 1

    new_task = Task(id=new_id, name=taskName, status="pending")

    tasks_data.append(new_task)

    print(f"✅ Task #{new_id}: '{taskName}' added.")


def complete(tasks_data: List[Task], taskId: int):
    print(f"Completing Task: {taskId}...")


def discard(tasks_data: List[Task], taskId: int):
    print(f"Discarding Task: {taskId}...")


def clean(tasks_data: List[Task], taskType: str):
    print(f"Cleaning {taskType} task...")


def listTasks(tasks_data: List[Task]):
    print("WIP")


def loadTask() -> List[Task]:
    try:
        with open(TASK_FILE, "r", encoding="urf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("Tasks file not found. Starting with an empty list.")
        return []
    except Exception as e:
        print(f"[ERROR]: {e}")
        return []


def saveTask(tasks_data: list):
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks_data, f, indent=4, ensure_ascii=False)
    print("Tasks saved successfully!")


def main():
    current_tasks = loadTask()

    paser = argparse.ArgumentParser(description="CLI To-Do list that just work.")
    paser.add_argument(
        "-a", "--add", type=str, metavar="taskName", help="Add a new task."
    )
    paser.add_argument(
        "-c", "--complete", type=int, metavar="taskId", help="Mark task as completed."
    )
    paser.add_argument(
        "-d", "--discard", type=int, metavar="taskId", help="Discard a task."
    )
    paser.add_argument(
        "-C",
        "--clean",
        type=str,
        metavar="discard|complete",
        help="Clean To-Do list by remove completed or discarded task.",
    )
    paser.add_argument("-l", "--list", action="store_true", help="List all task.")

    args = paser.parse_args()

    match args:
        case a if a.add is not None:
            add(current_tasks, a.add)
        case a if a.discard is not None:
            discard(current_tasks, a.discard)
        case a if a.complete is not None:
            complete(current_tasks, a.complete)
        case a if a.clean is not None:
            clean(current_tasks, a.clean)
        case a if a.list is True:
            listTasks(current_tasks)
        case _:
            listTasks(current_tasks)
    
    saveTask(current_tasks)


if __name__ == "__main__":
    main()
