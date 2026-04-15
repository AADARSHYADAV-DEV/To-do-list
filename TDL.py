import argparse
import json
import os
import sys
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def format_task(index, task):
    status = '✓' if task.get('done') else ' '
    created = task.get('created', '')
    return f"[{status}] {index}. {task['title']} (created: {created})"


def list_tasks(tasks):
    if not tasks:
        print('No tasks found. Add one with: python TDL.py add "Buy milk"')
        return
    print('To Do List:')
    for idx, task in enumerate(tasks, start=1):
        print(format_task(idx, task))


def add_task(tasks, title):
    task = {
        'title': title.strip(),
        'done': False,
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Added: "{title.strip()}"')


def mark_done(tasks, index):
    if index < 1 or index > len(tasks):
        print('Invalid task number.')
        return
    tasks[index - 1]['done'] = True
    save_tasks(tasks)
    print(f'Marked done: {tasks[index - 1]["title"]}')


def remove_task(tasks, index):
    if index < 1 or index > len(tasks):
        print('Invalid task number.')
        return
    removed = tasks.pop(index - 1)
    save_tasks(tasks)
    print(f'Removed: {removed["title"]}')


def clear_tasks():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    print('All tasks cleared.')


def print_help(parser):
    parser.print_help()
    print('\nExamples:')
    print('  python TDL.py list')
    print('  python TDL.py add "Buy groceries"')
    print('  python TDL.py done 1')
    print('  python TDL.py remove 1')
    print('  python TDL.py clear')


def interactive_menu(tasks):
    while True:
        print('\n=== To Do List ===')
        list_tasks(tasks)
        print('\nCommands: add, done, remove, clear, quit')
        command = input('> ').strip().lower()
        if command == 'quit' or command == 'exit':
            break
        if command.startswith('add '):
            add_task(tasks, command[4:])
        elif command == 'add':
            title = input('Task title: ').strip()
            if title:
                add_task(tasks, title)
        elif command.startswith('done '):
            try:
                mark_done(tasks, int(command.split()[1]))
            except (ValueError, IndexError):
                print('Usage: done <task number>')
        elif command.startswith('remove '):
            try:
                remove_task(tasks, int(command.split()[1]))
            except (ValueError, IndexError):
                print('Usage: remove <task number>')
        elif command == 'clear':
            confirm = input('Clear all tasks? (y/N): ').strip().lower()
            if confirm == 'y':
                tasks.clear()
                clear_tasks()
        else:
            print('Unknown command. Use add, done, remove, clear, or quit.')


def main():
    parser = argparse.ArgumentParser(description='Simple command-line To Do list app')
    parser.add_argument('command', nargs='?', help='Command to run: add, list, done, remove, clear')
    parser.add_argument('value', nargs='*', help='Task title or task number')
    args = parser.parse_args()

    tasks = load_tasks()

    if not args.command:
        interactive_menu(tasks)
        return

    command = args.command.lower()
    if command == 'list':
        list_tasks(tasks)
    elif command == 'add':
        title = ' '.join(args.value).strip()
        if not title:
            print('Please provide a task title.')
            return
        add_task(tasks, title)
    elif command == 'done':
        if not args.value:
            print('Please provide a task number.')
            return
        try:
            mark_done(tasks, int(args.value[0]))
        except ValueError:
            print('Task number must be a number.')
    elif command == 'remove':
        if not args.value:
            print('Please provide a task number.')
            return
        try:
            remove_task(tasks, int(args.value[0]))
        except ValueError:
            print('Task number must be a number.')
    elif command == 'clear':
        confirm = input('Clear all tasks? (y/N): ').strip().lower()
        if confirm == 'y':
            tasks.clear()
            clear_tasks()
    else:
        print('Unknown command:', command)
        print_help(parser)


if __name__ == '__main__':
    main()
    pi