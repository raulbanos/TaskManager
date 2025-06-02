# taskOperations.py
"""
Module for task operations in the Task Manager application.
Provides functions to add, edit, and delete tasks, including validation for dates.
"""
from datetime import datetime

def validateDate(dateString):
    """Validate if the date string is in DD-MM-YYYY format and is a valid date."""
    try:
        datetime.strptime(dateString, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def addTask(tasks):
    """Add a new task to the list with validated input."""
    title = input("Task title: ")
    description = input("Description: ")
    priority = input("Priority (high/medium/low): ").lower()
    
    while True:
        dueDate = input("Due date (DD-MM-YYYY): ")
        if validateDate(dueDate):
            break
        print("Invalid date format or value. Please use DD-MM-YYYY (e.g., 25-02-2025).")
    
    task = {
        "title": title,
        "description": description,
        "priority": priority,
        "dueDate": dueDate,
        "completed": False
    }
    tasks.append(task)
    print("Task added successfully!")

def editTask(tasks):
    """Edit an existing task."""
    from displayUtils import showTasks
    
    if not tasks:
        print("No tasks available to edit.")
        return
    
    numTasks = showTasks(tasks)
    while True:
        try:
            taskIndex = int(input(f"Enter the task number to edit (1-{numTasks}): ")) - 1
            if 0 <= taskIndex < len(tasks):
                break
            print(f"Please enter a number between 1 and {numTasks}.")
        except ValueError:
            print("Please enter a valid number.")
    
    task = tasks[taskIndex]
    print(f"\nEditing task: {task['title']}")
    print("Leave blank to keep current value.")
    
    newTitle = input(f"New title [{task['title']}]: ") or task['title']
    newDescription = input(f"New description [{task['description']}]: ") or task['description']
    newPriority = input(f"New priority (high/medium/low) [{task['priority']}]: ").lower() or task['priority']
    
    while True:
        newDueDate = input(f"New due date (DD-MM-YYYY) [{task['dueDate']}]: ") or task['dueDate']
        if validateDate(newDueDate):
            break
        print("Invalid date format or value. Please use DD-MM-YYYY (e.g., 25-02-2025).")
    
    newCompleted = input(f"Completed? (yes/no) [{'yes' if task['completed'] else 'no'}]: ").lower()
    newCompleted = True if newCompleted == "yes" else False if newCompleted == "no" else task['completed']
    
    tasks[taskIndex] = {
        "title": newTitle,
        "description": newDescription,
        "priority": newPriority,
        "dueDate": newDueDate,
        "completed": newCompleted
    }
    print("Task updated successfully!")

def deleteTask(tasks):
    """Delete an existing task."""
    from displayUtils import showTasks
    
    if not tasks:
        print("No tasks available to delete.")
        return
    
    numTasks = showTasks(tasks)
    while True:
        try:
            taskIndex = int(input(f"Enter the task number to delete (1-{numTasks}): ")) - 1
            if 0 <= taskIndex < len(tasks):
                break
            print(f"Please enter a number between 1 and {numTasks}.")
        except ValueError:
            print("Please enter a valid number.")
    
    deletedTask = tasks.pop(taskIndex)
    print(f"Task '{deletedTask['title']}' deleted successfully!")