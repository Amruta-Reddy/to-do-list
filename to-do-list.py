# tkinter is a framework used to create GUI elements
from tkinter import *
import tkinter as tk

# messagebox module will display message boxes
from tkinter import messagebox
from datetime import date

# sqlite3 module for SQLite database operations
import sqlite3

# Create the database connection
conn = sqlite3.connect("todolist.db")
c = conn.cursor()                                        #  a cursor object to execute SQL statements on the database

# Create the tasks table if it doesn't exist
c.execute(
    #  the table columns: id (primary key), task_text (text), date_added (text).
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_text TEXT,
        date_added TEXT
    )
    """
)

# when a user adds a task
def add_task(event=None):
    task = entry.get("1.0", tk.END).strip()
    if task:
        # Insert the task into the database
        c.execute("INSERT INTO tasks (task_text, date_added) VALUES (?, ?)", (task, date.today().strftime("%Y-%m-%d")))
        conn.commit()

        listbox.insert(tk.END, task)
        entry.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

# when a user delets a task
def delete_task():
    try:
        index = listbox.curselection()
        selected_task = listbox.get(index)
        listbox.delete(index)

        # Delete the task from the database
        c.execute("DELETE FROM tasks WHERE task_text=?", (selected_task,))
        conn.commit()
    except:
        messagebox.showwarning("Warning", "Please select a task to delete.")

# when a user wants to clear all the tasks
def clear_tasks():
    listbox.delete(0, tk.END)

    # Clear all tasks from the database
    c.execute("DELETE FROM tasks")
    conn.commit()

# Create the main window
window = Tk()
window.geometry("400x500")
window.title("To Do List")

# Create and set custom font
font_family = "Arial"
font_size = 14
custom_font = (font_family, font_size)
window.option_add("*Font", custom_font)

# Get the current date
today = date.today().strftime("%B %d, %Y")

# Create the title label
titleLabel = Label(window, text=today, font=("Georgia", 30))
titleLabel.pack(pady=5)

# Create the listbox
listbox = tk.Listbox(
    window,
    width=25,
    font=custom_font,
    bg="#CDCCCD",
    selectbackground="#a6a6a6",
    selectforeground="black",
    relief=tk.FLAT
)
listbox.pack(pady=10)

# Populate the listbox with tasks from the database
c.execute("SELECT task_text FROM tasks")
tasks = c.fetchall()
for task in tasks:
    listbox.insert(tk.END, task[0])

# Create the entry field
entry = tk.Text(
    window,
    font=custom_font,
    height=4,
    width=25,
    relief=tk.FLAT,
    bg="#AB9AC6",
    bd=0
)
entry.pack(pady=5)

# Bind the <Return> key to the add_task function
entry.bind("<Return>", add_task)

# Create buttons
button_frame = tk.Frame(window, bg="#F3F3F3")
button_frame.pack(pady=10)

add_button = tk.Button(
    button_frame,
    text="Add Task",
    command=add_task,
    font=custom_font,
    bg="#81b29a",
    fg="#ffffff",
    relief=tk.FLAT,
    activebackground="green",
    activeforeground="#ffffff"
)
add_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(
    button_frame,
    text="Delete Task",
    command=delete_task,
    font=custom_font,
    bg="#db8b8b",
    fg="#ffffff",
    relief=tk.FLAT,
    activebackground="red",
    activeforeground="#ffffff"
)
delete_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(
    button_frame,
    text="Clear All",
    command=clear_tasks,
    font=custom_font,
    bg="yellow",
    fg="black",
    relief=tk.FLAT,
    activebackground="#b16d6d",
    activeforeground="#ffffff"
)
clear_button.grid(row=0, column=2, padx=5)

# Run the main window loop
window.mainloop()

# Close the database connection
conn.close()
