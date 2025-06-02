# fileOperations.py
"""
Module for handling file operations in the Task Manager application.
Provides functions to load and save tasks to a JSON file for persistent storage.
"""
import json
import os

def loadTasks(filePath='tasks.json'):
    """Load tasks from the JSON file."""
    try:
        with open(filePath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def saveTasks(tasks, filePath='tasks.json'):
    """Save tasks to the JSON file."""
    with open(filePath, 'w') as file:
        json.dump(tasks, file, indent=4)
    print(f"Tasks saved to: {os.path.abspath(filePath)}")