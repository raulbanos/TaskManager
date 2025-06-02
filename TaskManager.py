import json
from datetime import datetime, timedelta
import os

# Colors for console output
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

def loadTasks():
    """Load tasks from the JSON file."""
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def saveTasks(tasks):
    """Save tasks to the JSON file."""
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

def validateDate(dateString): 
    """Validate if the date string is in DD-MM-YY format and is a valid date"""
    try: 
        #Try to parse the date
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
            break #Exit loop if date is valid
        print("Invalid date format or value. Please use DD-MM-YY (e.g, 25-02-2025)")
    task = {
        "title": title,
        "description": description,
        "priority": priority,
        "dueDate": dueDate,
        "completed": False
    }
    tasks.append(task)
    print ("Task appended successfully")

def showTasks(tasks, filterToday=False):
    """Display tasks with optional filter for today."""
    today = datetime.now().date()
    hasAlerts = False
    for i, task in enumerate(tasks, 1):
        # Parse due date in DD-MM-YYYY format
        dueDate = datetime.strptime(task["dueDate"], "%d-%m-%Y").date()
        if filterToday and dueDate != today:
            continue  # Skip tasks not due today if filter is active
        
        # Set color based on priority
        if task["priority"] == "high":
            color = Colors.RED
        elif task["priority"] == "medium":
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
        
        # Alert if task is close to due date (within 1 day)
        daysRemaining = (dueDate - today).days
        alert = " (!)" if daysRemaining <= 1 and not task["completed"] else ""
        if alert:
            hasAlerts = True
        
        status = "✔" if task["completed"] else "✘"
        print(f"{color}{i}. {task['title']} - {task['priority']} - {task['dueDate']} [{status}]{alert}{Colors.RESET}")
    
    if hasAlerts:
        print(f"{Colors.RED}Warning! Some tasks are close to their due date.{Colors.RESET}")
    return len(tasks) #Return number of tasks for validation

def editTasks(tasks): 
    """Edit an existing task"""
    if not tasks: 
        print("No tasks available to edit.")
        return 
    numTasks= showTasks(tasks)
    while True: 
        try: 
            taskIndex= int(input(f"Enter the task number you wish to edit (1-{numTasks}): "))-1
            if 0 <= taskIndex < len(tasks): 
                break
            print(f"Please enter a number between 1 and {numTasks}.")
        except ValueError: 
            print("Please enter a valid number.")
    task=tasks[taskIndex]
    print(f"\nEditing task: {task['title']}")
    print("Leave blank to keep current value.")

    newTitle=input(f"New title [{task['title']}]: ") or task['title']
    newDescription=input(f"New description [{task['description']}]: ") or task['description']
    newPriority=input(f"New priority [{task['priority']}]: ") or task['priority']

    while  True: 
        newDueDate= input(f"New due date (DD-MM-YY) [{task['dueDate']}]") or task['dueDate']
        if validateDate(newDueDate): 
            break
        print("Invalid date format or value. Please use DD-MM-YY (e.g 1-01-1999)")
    newCompleted= input (f"Completed? (yes/no) [{'yes' if task['completed']else 'no'}]: ").lower()
    newCompleted=True if newCompleted=="yes" else False if newCompleted=="no" else task ['completed']

    tasks [taskIndex]={
        "title": newTitle,
        "description": newDescription,
        "priority": newPriority,
        "dueDate": newDueDate,
        "completed": newCompleted
    }
    print ("Task updated successfully")

def deleteTask(tasks): 
    """Delete an existing task."""
    if not tasks: 
        print("No tasks available to delete")
        return 
    numTasks=showTasks(tasks)
    while True: 
        try: 
            taskIndex= int (input(f"Enter the task number you wish to delete (1-{numTasks}): "))
            if 0<= taskIndex<len(tasks): 
                break
            print(f"Please enter a number between 1 and {numTasks}")
        except ValueError: 
            print ("Please enter a valid number.")
    deletedTask=tasks.pop(taskIndex)
    print(f"Task '{deletedTask['title']}' deleted successfully!")

# Main program
tasks = loadTasks()
while True:
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
    print("\n1. Add task\n2. Show all tasks\n3. Show today's tasks\n4. Edit task \n5. Delete task \n6. Exit Program")
    choice = input("Choose an option: ")
    if choice == "1":
        addTask(tasks)
    elif choice == "2":
        showTasks(tasks)
    elif choice == "3":
        showTasks(tasks, filterToday=True)
    elif choice == "4":
       editTasks(tasks)    
    elif choice == "5":
       deleteTask(tasks)
    elif choice == "6":
       saveTasks(tasks)
       break
    input("\nPress Enter to continue...")