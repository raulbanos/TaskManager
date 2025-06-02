# gui.py
"""
Graphical User Interface (GUI) for the Task Manager application.
Built with Tkinter, this module provides a visual way to manage tasks,
including adding, editing, deleting, and sorting tasks by priority or due date.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from taskOperations import addTask, editTask, deleteTask, validateDate
from fileOperations import saveTasks
from displayUtils import Colors, sortTasks

class TaskManagerGUI:
    def __init__(self, root, tasks):
        self.root = root
        self.tasks = tasks
        self.root.title("Task Manager")
        self.root.geometry("800x600")

        # Configure style for a modern look
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10), padding=10)
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("Treeview", font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        # Main container
        self.mainContainer = ttk.Frame(self.root, padding="20")
        self.mainContainer.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        titleLabel = ttk.Label(self.mainContainer, text="Task Manager", font=("Helvetica", 16, "bold"))
        titleLabel.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Task list
        self.taskList = ttk.Treeview(self.mainContainer, columns=("Title", "Priority", "Due Date", "Completed"), show="headings", height=15)
        self.taskList.heading("Title", text="Title")
        self.taskList.heading("Priority", text="Priority")
        self.taskList.heading("Due Date", text="Due Date")
        self.taskList.heading("Completed", text="Completed")
        self.taskList.column("Title", width=300)
        self.taskList.column("Priority", width=100)
        self.taskList.column("Due Date", width=120)
        self.taskList.column("Completed", width=100)
        self.taskList.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar for task list
        scrollbar = ttk.Scrollbar(self.mainContainer, orient=tk.VERTICAL, command=self.taskList.yview)
        self.taskList.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))

        # Button frame
        buttonFrame = ttk.Frame(self.mainContainer, padding="10")
        buttonFrame.grid(row=2, column=0, columnspan=2, pady=20)

        # Buttons
        ttk.Button(buttonFrame, text="Add Task", command=self.openAddTaskWindow).grid(row=0, column=0, padx=5)
        ttk.Button(buttonFrame, text="Edit Task", command=self.openEditTaskWindow).grid(row=0, column=1, padx=5)
        ttk.Button(buttonFrame, text="Delete Task", command=self.deleteTask).grid(row=0, column=2, padx=5)
        ttk.Button(buttonFrame, text="Sort by Priority", command=lambda: self.sortTasks("priority")).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(buttonFrame, text="Sort by Due Date", command=lambda: self.sortTasks("dueDate")).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(buttonFrame, text="Exit", command=self.exit).grid(row=1, column=2, padx=5, pady=5)

        # Initial task display
        self.refreshTaskList()

    def refreshTaskList(self, sortBy=None):
        """Refresh the task list display."""
        for item in self.taskList.get_children():
            self.taskList.delete(item)

        tasksToDisplay = sortTasks(self.tasks.copy(), sortBy)

        today = datetime.now().date()
        for task in tasksToDisplay:
            dueDate = datetime.strptime(task["dueDate"], "%d-%m-%Y").date()
            daysRemaining = (dueDate - today).days
            alert = " (!)" if daysRemaining <= 1 and not task["completed"] else ""
            
            if task["priority"] == "high":
                tag = "high"
            elif task["priority"] == "medium":
                tag = "medium"
            else:
                tag = "low"
            
            self.taskList.insert("", tk.END, values=(
                task["title"] + alert,
                task["priority"],
                task["dueDate"],
                "✔" if task["completed"] else "✘"
            ), tags=(tag,))

        self.taskList.tag_configure("high", foreground="red")
        self.taskList.tag_configure("medium", foreground="orange")
        self.taskList.tag_configure("low", foreground="green")

    def openAddTaskWindow(self):
        """Open a window to add a new task."""
        self.taskWindow = tk.Toplevel(self.root)
        self.taskWindow.title("Add Task")
        self.taskWindow.geometry("400x350")

        formFrame = ttk.Frame(self.taskWindow, padding="20")
        formFrame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(formFrame, text="Add New Task", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Label(formFrame, text="Title:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.titleEntry = ttk.Entry(formFrame, width=30)
        self.titleEntry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formFrame, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.descEntry = ttk.Entry(formFrame, width=30)
        self.descEntry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(formFrame, text="Priority:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.priorityCombo = ttk.Combobox(formFrame, values=["high", "medium", "low"], width=27)
        self.priorityCombo.grid(row=3, column=1, padx=5, pady=5)
        self.priorityCombo.set("medium")

        ttk.Label(formFrame, text="Due Date (DD-MM-YYYY):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.dueDateEntry = ttk.Entry(formFrame, width=30)
        self.dueDateEntry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(formFrame, text="Add", command=self.addTask).grid(row=5, column=0, columnspan=2, pady=20)

    def addTask(self):
        """Add a new task from the GUI."""
        title = self.titleEntry.get()
        description = self.descEntry.get()
        priority = self.priorityCombo.get().lower()
        dueDate = self.dueDateEntry.get()

        if not title:
            messagebox.showerror("Error", "Title cannot be empty.")
            return
        if not validateDate(dueDate):
            messagebox.showerror("Error", "Invalid date format or value. Please use DD-MM-YYYY (e.g., 25-02-2025).")
            return

        task = {
            "title": title,
            "description": description,
            "priority": priority,
            "dueDate": dueDate,
            "completed": False
        }
        self.tasks.append(task)
        self.refreshTaskList()
        self.taskWindow.destroy()
        messagebox.showinfo("Success", "Task added successfully!")

    def openEditTaskWindow(self):
        """Open a window to edit the selected task."""
        selected = self.taskList.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task to edit.")
            return

        selectedIndex = self.taskList.index(selected[0])
        task = self.tasks[selectedIndex]

        self.editWindow = tk.Toplevel(self.root)
        self.editWindow.title("Edit Task")
        self.editWindow.geometry("400x350")

        formFrame = ttk.Frame(self.editWindow, padding="20")
        formFrame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(formFrame, text="Edit Task", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Label(formFrame, text="Title:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.titleEntry = ttk.Entry(formFrame, width=30)
        self.titleEntry.insert(0, task["title"])
        self.titleEntry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formFrame, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.descEntry = ttk.Entry(formFrame, width=30)
        self.descEntry.insert(0, task["description"])
        self.descEntry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(formFrame, text="Priority:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.priorityCombo = ttk.Combobox(formFrame, values=["high", "medium", "low"], width=27)
        self.priorityCombo.set(task["priority"])
        self.priorityCombo.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(formFrame, text="Due Date (DD-MM-YYYY):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.dueDateEntry = ttk.Entry(formFrame, width=30)
        self.dueDateEntry.insert(0, task["dueDate"])
        self.dueDateEntry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(formFrame, text="Completed:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.completedVar = tk.StringVar(value="yes" if task["completed"] else "no")
        ttk.Combobox(formFrame, textvariable=self.completedVar, values=["yes", "no"], width=27).grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(formFrame, text="Update", command=lambda: self.updateTask(selectedIndex)).grid(row=6, column=0, columnspan=2, pady=20)

    def updateTask(self, taskIndex):
        """Update the selected task."""
        title = self.titleEntry.get()
        description = self.descEntry.get()
        priority = self.priorityCombo.get().lower()
        dueDate = self.dueDateEntry.get()
        completed = self.completedVar.get() == "yes"

        if not title:
            messagebox.showerror("Error", "Title cannot be empty.")
            return
        if not validateDate(dueDate):
            messagebox.showerror("Error", "Invalid date format or value. Please use DD-MM-YYYY (e.g., 25-02-2025).")
            return

        self.tasks[taskIndex] = {
            "title": title,
            "description": description,
            "priority": priority,
            "dueDate": dueDate,
            "completed": completed
        }
        self.refreshTaskList()
        self.editWindow.destroy()
        messagebox.showinfo("Success", "Task updated successfully!")

    def deleteTask(self):
        """Delete the selected task."""
        selected = self.taskList.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task to delete.")
            return

        selectedIndex = self.taskList.index(selected[0])
        deletedTask = self.tasks.pop(selectedIndex)
        self.refreshTaskList()
        messagebox.showinfo("Success", f"Task '{deletedTask['title']}' deleted successfully!")

    def sortTasks(self, sortBy):
        """Sort tasks and refresh the display."""
        self.refreshTaskList(sortBy=sortBy)

    def exit(self):
        """Save tasks and exit the application."""
        saveTasks(self.tasks)
        self.root.destroy()

def runGUI(tasks):
    """Run the GUI application."""
    root = tk.Tk()
    app = TaskManagerGUI(root, tasks)
    root.mainloop()