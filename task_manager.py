import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority INTEGER,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

# Add a new task
def add_task():
    title = input("Enter task title: ").strip()
    description = input("Enter description (optional): ").strip()
    due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()
    priority = input("Enter priority (1=High, 2=Medium, 3=Low, default=3): ").strip()

    if priority not in ['1', '2', '3']:
        priority = '3'

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date, priority)
        VALUES (?, ?, ?, ?)
    ''', (title, description, due_date if due_date else None, int(priority)))
    conn.commit()
    conn.close()
    print("Task added successfully!")

# View all tasks
def view_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, due_date, priority, status FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n--- All Tasks ---")
    for task in tasks:
        id, title, due_date, priority, status = task
        print(f"[{id}] {title} | Due: {due_date or 'N/A'} | Priority: {priority} | Status: {status}")

# Mark a task as completed
def mark_task_completed():
    task_id = input("Enter the ID of the task to mark as completed: ").strip()
    if not task_id.isdigit():
        print("Invalid ID.")
        return

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("No task found with that ID.")
    else:
        print("Task marked as completed.")

    conn.close()

# Edit a task
def edit_task():
    task_id = input("Enter the ID of the task to edit: ").strip()
    if not task_id.isdigit():
        print("Invalid ID.")
        return

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        print("No task found with that ID.")
        conn.close()
        return

    print("\nLeave a field blank to keep it unchanged.")

    new_title = input(f"New title (current: {task[1]}): ").strip()
    new_description = input(f"New description (current: {task[2]}): ").strip()
    new_due_date = input(f"New due date (current: {task[3] or 'N/A'}): ").strip()
    new_priority = input(f"New priority (1=High, 2=Medium, 3=Low, current: {task[4]}): ").strip()

    updated_title = new_title if new_title else task[1]
    updated_description = new_description if new_description else task[2]
    updated_due_date = new_due_date if new_due_date else task[3]
    updated_priority = int(new_priority) if new_priority in ['1', '2', '3'] else task[4]

    cursor.execute('''
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, priority = ?
        WHERE id = ?
    ''', (updated_title, updated_description, updated_due_date, updated_priority, task_id))

    conn.commit()
    conn.close()
    print("Task updated successfully.")

# Change task status
def change_task_status():
    task_id = input("Enter the ID of the task to change status: ").strip()
    if not task_id.isdigit():
        print("Invalid ID.")
        return

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        print("No task found with that ID.")
        conn.close()
        return

    print(f"Current status: {task[0]}")
    print("Choose new status:")
    print("1. Pending")
    print("2. In Progress")
    print("3. Completed")

    choice = input("Enter option number: ").strip()

    status_map = {
        '1': 'Pending',
        '2': 'In Progress',
        '3': 'Completed'
    }

    new_status = status_map.get(choice)
    if not new_status:
        print("Invalid choice.")
        conn.close()
        return

    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()
    print(f"Status updated to '{new_status}'.")

# Delete a task
def delete_task():
    task_id = input("Enter the ID of the task to delete: ").strip()
    if not task_id.isdigit():
        print("Invalid ID.")
        return

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        print("No task found with that ID.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete task '{task[1]}'? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Deletion cancelled.")
        conn.close()
        return

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Task deleted successfully.")

# Main menu
def main():
    init_db()
    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task as Completed")
        print("4. Edit Task")
        print("5. Change Task Status")
        print("6. Delete Task")
        print("7. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            view_tasks()
            mark_task_completed()
        elif choice == '4':
            view_tasks()
            edit_task()
        elif choice == '5':
            view_tasks()
            change_task_status()
        elif choice == '6':
            view_tasks()
            delete_task()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()