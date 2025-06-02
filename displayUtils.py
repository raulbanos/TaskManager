# displayUtils.py
"""
Utility module for displaying tasks in the Task Manager application.
Provides functions to sort and display tasks in the console or GUI,
with color-coded priorities and alerts for due dates.
"""
from datetime import datetime, timedelta

class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

def sortTasks(tasks, sortBy=None):
    """Sort tasks by priority or due date."""
    if not sortBy:
        return tasks
    
    priorityLevels = {"high": 3, "medium": 2, "low": 1}
    
    if sortBy == "priority":
        return sorted(tasks, key=lambda x: priorityLevels.get(x["priority"], 0), reverse=True)
    elif sortBy == "dueDate":
        return sorted(tasks, key=lambda x: datetime.strptime(x["dueDate"], "%d-%m-%Y"))
    return tasks

def showTasks(tasks, filterToday=False, sortBy=None):
    """Display tasks with optional filter for today and sorting."""
    tasksToDisplay = sortTasks(tasks.copy(), sortBy)
    
    today = datetime.now().date()
    hasAlerts = False
    for i, task in enumerate(tasksToDisplay, 1):
        dueDate = datetime.strptime(task["dueDate"], "%d-%m-%Y").date()
        if filterToday and dueDate != today:
            continue
        
        if task["priority"] == "high":
            color = Colors.RED
        elif task["priority"] == "medium":
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
        
        daysRemaining = (dueDate - today).days
        alert = " (!)" if daysRemaining <= 1 and not task["completed"] else ""
        if alert:
            hasAlerts = True
        
        status = "✔" if task["completed"] else "✘"
        print(f"{color}{i}. {task['title']} - {task['priority']} - {task['dueDate']} [{status}]{alert}{Colors.RESET}")
    
    if hasAlerts:
        print(f"{Colors.RED}Warning! Some tasks are close to their due date.{Colors.RESET}")
    return len(tasksToDisplay)