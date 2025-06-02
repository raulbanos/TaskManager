# main.py
"""
Main entry point for the Task Manager application.
Allows the user to choose between a console interface and a graphical interface (GUI)
to manage tasks, including adding, editing, deleting, and sorting tasks.
"""
import os
from fileOperations import loadTasks, saveTasks
from taskOperations import addTask, editTask, deleteTask
from displayUtils import showTasks
from gui import runGUI

# Main program
tasks = loadTasks()

print("Welcome to Task Manager!")
print("1. Use Console Interface\n2. Use Graphical Interface (GUI)")
interfaceChoice = input("Choose an interface: ")

if interfaceChoice == "1":
    # Console interface
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n1. Add task\n2. Show all tasks\n3. Show today's tasks\n4. Edit task\n5. Delete task\n6. Sort and show tasks\n7. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            addTask(tasks)
        elif choice == "2":
            showTasks(tasks)
        elif choice == "3":
            showTasks(tasks, filterToday=True)
        elif choice == "4":
            editTask(tasks)
        elif choice == "5":
            deleteTask(tasks)
        elif choice == "6":
            print("\nSort by:\n1. Priority\n2. Due date\n3. No sorting")
            sortChoice = input("Choose a sorting option: ")
            sortBy = None
            if sortChoice == "1":
                sortBy = "priority"
            elif sortChoice == "2":
                sortBy = "dueDate"
            showTasks(tasks, sortBy=sortBy)
        elif choice == "7":
            saveTasks(tasks)
            break
        input("\nPress Enter to continue...")
elif interfaceChoice == "2":
    # Graphical interface
    runGUI(tasks)
else:
    print("Invalid choice. Exiting...")
    saveTasks(tasks)