import datetime
import os

from utilities import get_today

def manage_todo_list():
    try:
        today = get_today().split('T')[0]
        todofile = f"{today}.todo"

        todo_files = sorted([f for f in os.listdir() if f.endswith('.todo')])

        if not os.path.exists(todofile) and todo_files:
            most_recent_file = todo_files[-1]
            with open(most_recent_file, 'r') as file:
                tasks = file.readlines()
            uncompleted_tasks = [task for task in tasks if not task.startswith('~~')]
            with open(todofile, 'w') as file:
                file.writelines(uncompleted_tasks)
        elif not os.path.exists(todofile):
            with open(todofile, 'w') as file:
                pass

        with open(todofile, 'r') as file:
            tasks = file.readlines()

        while True:
            completed_tasks = [task for task in tasks if task.startswith('~~')]
            uncompleted_tasks = [task for task in tasks if not task.startswith('~~')]

            print("\nTo-do list:")
            for i, task in enumerate(uncompleted_tasks, 1):
                print(f"{i}. {task}", end="")
            print("\nCompleted tasks:")
            for i, task in enumerate(completed_tasks, 1):
                print(f"{i}. {task}", end="")
            print("\nm. Mark a task as completed\ns. Swap task positions\nq. Quit")
            action_or_task = input("Select an action or type in the task you would like to add: ")
            if action_or_task.lower() == 'q':
                break
            elif action_or_task.lower() == 'm':
                task_num = int(input("Enter a task number to mark as completed: ")) - 1
                assert 0 <= task_num < len(uncompleted_tasks), "Invalid task number."
                removed_task = f"~~{uncompleted_tasks[task_num].strip()}~~\n"
                uncompleted_tasks.remove(uncompleted_tasks[task_num])
                completed_tasks.append(removed_task)
            elif action_or_task.lower() == 's':
                pos1 = int(input("Enter the first task number to swap: ")) - 1
                pos2 = int(input("Enter the second task number to swap: ")) - 1
                assert 0 <= pos1 < len(uncompleted_tasks) and 0 <= pos2 < len(uncompleted_tasks), "Invalid task number."
                uncompleted_tasks[pos1], uncompleted_tasks[pos2] = uncompleted_tasks[pos2], uncompleted_tasks[pos1]
            else:  
                uncompleted_tasks.append(action_or_task + "\n")

            tasks = uncompleted_tasks + completed_tasks

        with open(todofile, 'w') as file:
            for task in tasks:
                file.write(task)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
