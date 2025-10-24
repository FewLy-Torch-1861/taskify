import io
import argparse


def main():
    paser = argparse.ArgumentParser(description="CLI To-Do list that just work.")
    paser.add_argument("-a", "--add", type=str, help="Add a new task.")
    paser.add_argument("-c", "--complete", type=int, help="Mark task as completed.")
    paser.add_argument("-d", "--discard", type=int, help="Discard a task.")
    paser.add_argument(
        "-C", "--clean", help="Clean To-Do list by remove completed and discarded task."
    )

    args = paser.parse_args()


if __name__ == "__main__":
    main()
