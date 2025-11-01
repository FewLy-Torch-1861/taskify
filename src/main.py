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


def add(tasks_data: List[Task], taskName: str):
    new_task = Task(id=0, name=taskName, status="pending")

    tasks_data.append(new_task)

    new_id = len(tasks_data)
    print(f"✅ Task #{new_id}: '{taskName}' has been added.")


def complete(tasks_data: List[Task], taskId: int):
    task_index = taskId - 1

    if 0 <= task_index < len(tasks_data):
        task = tasks_data[task_index]

        if task["status"] == "complete":
            print(f"⚠️ Task #{taskId} is already completed.")
            return

        task["status"] = "complete"
        print(f"🎉 Task #{taskId}: '{task['name']}' marked as COMPLETE.")

    else:
        print(f"❌ Error: Task ID {taskId} not found.")


def discard(tasks_data: List[Task], taskId: int):
    task_index = taskId - 1

    if 0 <= task_index < len(tasks_data):
        task = tasks_data[task_index]

        if task["status"] == "discard":
            print(f"⚠️ Task #{taskId} is already discarded.")
            return

        task["status"] = "discard"
        print(f"🎉 Task #{taskId}: '{task['name']}' marked as DISCARD.")

    else:
        print(f"❌ Error: Task ID {taskId} not found.")


def edit(tasks_data: List[Task], taskId: int, newName: str):
    task_index = taskId - 1

    if 0 <= task_index < len(tasks_data):
        task = tasks_data[task_index]
        old_name = task["name"]
        task["name"] = newName
        print(f"✅ Task #{taskId} has been updated from '{old_name}' to '{newName}'.")

    else:
        print(f"❌ Error: Task ID {taskId} not found.")


def clean(tasks_data: List[Task], taskType: str):
    if taskType == "complete" or taskType == "discard":
        initial_count = len(tasks_data)

        tasks_to_keep = [task for task in tasks_data if task["status"] != taskType]
        tasks_data[:] = tasks_to_keep

        removed_count = initial_count - len(tasks_data)

        if removed_count > 0:
            print(f"🎉 Cleared {removed_count} tasks with status '{taskType}'.")
        else:
            print(f"🧹 No tasks with status '{taskType}' found to clear.")

    else:
        print(
            f"❌ Error: Task Status '{taskType}' is invalid. Please use 'discard' or 'complete'."
        )


def listTasks(tasks_data: List[Task]):
    if not tasks_data:
        print("\n🎉 Your to-do list is sparkling clean! Nothing to see here. 🎉")
        return

    print("\n📦 To-Do List:")
    print("—" * 40)

    for i, task in enumerate(tasks_data):
        task_id = i + 1
        task_name = task["name"]
        status = task["status"]

        if status == "complete":
            prefix = "  [✅] "
            display_name = f"\033[90m{task_name}\033[0m"
        elif status == "discard":
            prefix = "  [❌] "
            display_name = f"\033[31m{task_name}\033[0m"
        else:
            prefix = "  [⏳] "
            display_name = task_name

        print(f"{prefix} {task_id:<3} | {display_name}")

    print("—" * 40)
    print(f"Total tasks: {len(tasks_data)}")


def loadTask(taskFile: Path) -> List[Task]:
    try:
        with open(taskFile, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("Tasks file not found. Starting with an empty list.")
        return []
    except Exception as e:
        print(f"[ERROR]: {e}")
        return []


def saveTask(taskFile, tasks_data: list):
    with open(taskFile, "w", encoding="utf-8") as f:
        json.dump(tasks_data, f, indent=4, ensure_ascii=False)


def reindex_tasks(tasks_data: List[Task]):
    for i, task in enumerate(tasks_data):
        task["id"] = i + 1


def main():
    TASK_FILE = get_task_file_path()
    current_tasks = loadTask(TASK_FILE)

    paser = argparse.ArgumentParser(description="CLI To-Do list that just work.")
    paser.add_argument(
        "-a", "--add", type=str, metavar="taskName", help="Add a new task."
    )
    paser.add_argument(
        "-c", "--complete", type=int, metavar="taskId", help="Mark task as completed."
    )
    paser.add_argument(
        "-d", "--discard", type=int, metavar="taskId", help="Mark task as discarded."
    )
    paser.add_argument(
        "-e",
        "--edit",
        nargs=2,
        metavar=("taskId", "newName"),
        help="Edit an existing task.",
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
        case a if a.edit is not None:
            edit(current_tasks, int(a.edit[0]), a.edit[1])
        case a if a.complete is not None:
            complete(current_tasks, a.complete)
        case a if a.clean is not None:
            clean(current_tasks, a.clean)
        case a if a.list is True:
            listTasks(current_tasks)
        case _:
            listTasks(current_tasks)

    reindex_tasks(current_tasks)
    saveTask(TASK_FILE, current_tasks)


if __name__ == "__main__":
    main()
