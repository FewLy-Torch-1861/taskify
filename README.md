# taskify

> A simple CLI To-Do list that just works.

`taskify` is a lightweight, command-line task manager written in Python. It helps you manage your to-do list directly from your terminal, storing tasks in a simple JSON file.

## Features

- **Add Tasks**: Quickly add new tasks to your list.
- **Update Status**: Mark tasks as `complete` or `discard`.
- **List View**: View all your tasks with color-coded statuses.
- **Clean Up**: Remove all `complete` or `discarded` tasks.
- **Persistent Storage**: Tasks are saved to `tasks.json`, following the XDG Base Directory Specification.

## Installation

There are two ways to use `taskify`.

### From a Pre-built Binary (Recommended)

You can download a pre-built binary for your operating system from the [latest release page](https://github.com/FewLy-Torch-1861/taskify/releases/latest). This is the easiest method and does not require Python to be installed.

After downloading, you may need to make it executable (on Linux/macOS):

```bash
chmod +x ./taskify
./taskify --help
```

### From Source

If you have Python 3 installed, you can run the script directly from the source code.

```bash
git clone https://github.com/FewLy-Torch-1861/taskify.git
cd taskify
python src/main.py --help
```

## Usage

If you've downloaded the binary, you can run all commands directly. If you're running from source, replace `./taskify` with `python src/main.py` in the examples below.

### List All Tasks

To see your current to-do list, run the script without any arguments or with the `--list` flag.

**Command:**

```bash
./taskify
```

**Example Output:**

```
📦 To-Do List:
————————————————————————————————————————
  [⏳]  1   | Buy groceries
  [✅]  2   | Finish the project report
  [❌]  3   | Old idea I will not pursue
————————————————————————————————————————
Total tasks: 3
```

### Add a New Task

Use the `-a` or `--add` flag followed by the task name in quotes.

**Command:**

```bash
./taskify --add "Read a new book"
```

**Output:**

```
✅ Task #4: 'Read a new book' has been added.
```

### Complete a Task

Use the `-c` or `--complete` flag followed by the Task ID.

**Command:**

```bash
./taskify --complete 1
```

**Output:**

```
🎉 Task #1: 'Buy groceries' marked as COMPLETE.
```

### Discard a Task

Use the `-d` or `--discard` flag followed by the Task ID.

**Command:**

```bash
./taskify --discard 3
```

### Edit a Task

Use the `-e` or `--edit` flag followed by the Task ID and the new task name in quotes.

**Command:**

```bash
./taskify --edit 1 "Buy milk and eggs"
```

**Output:**

```
✅ Task #1 has been updated from 'Buy groceries' to 'Buy milk and eggs'.
```

### Clean the Task List

Remove all tasks with a specific status (`complete` or `discard`) using the `-C` or `--clean` flag.

**Command:**

```bash
./taskify --clean complete
```

## Data Storage

Your tasks are stored in a `tasks.json` file located in the application's data directory. The script respects the `XDG_DATA_HOME` environment variable. If it's not set, the default path is `~/.local/share/taskify/tasks.json`.

## Tips and Tricks

You can copy/move the downloaded binary to `~/.local/bin` (or any directory in your `PATH`) to run it from anywhere.
