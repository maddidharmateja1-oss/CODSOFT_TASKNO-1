import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog


class TodoApp:

    def __init__(self, root):
        self.root = root
        self.root.title("CodSoft - To-Do List")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.config(bg="#f4f4f4")

        self.filename = "tasks.json"
        self.tasks = self.load_tasks()

        # Title Label
        self.title_label = tk.Label(
            self.root,
            text="My To-Do List",
            font=("Arial", 18, "bold"),
            bg="#f4f4f4",
        )
        self.title_label.pack(pady=10)

        # Task Entry
        self.entry_task = tk.Entry(
            self.root, font=("Arial", 12), width=30, bd=2
        )
        self.entry_task.pack(pady=5)
        self.entry_task.bind("<Return>", lambda event: self.add_task())

        # Add Task Button
        self.btn_add = tk.Button(
            self.root,
            text="Add Task",
            font=("Arial", 10, "bold"),
            bg="#0d6efd",
            fg="white",
            width=20,
            command=self.add_task,
        )
        self.btn_add.pack(pady=5)

        # Listbox Frame & Scrollbar
        self.frame_list = tk.Frame(self.root)
        self.frame_list.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.frame_list)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_tasks = tk.Listbox(
            self.frame_list,
            font=("Arial", 12),
            width=32,
            height=10,
            yscrollcommand=self.scrollbar.set,
            exportselection=False,
            selectmode=tk.SINGLE,
        )
        self.listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.listbox_tasks.yview)

        # Button Frame
        self.frame_buttons = tk.Frame(self.root, bg="#f4f4f4")
        self.frame_buttons.pack(pady=10)

        self.btn_toggle = tk.Button(
            self.frame_buttons,
            text="✔ Toggle Done",
            font=("Arial", 10, "bold"),
            bg="#4caf50",
            fg="white",
            width=14,
            command=self.toggle_done,
        )
        self.btn_toggle.grid(row=0, column=0, padx=5, pady=5)

        self.btn_edit = tk.Button(
            self.frame_buttons,
            text="✏ Edit Task",
            font=("Arial", 10, "bold"),
            bg="#ffc107",
            fg="black",
            width=14,
            command=self.edit_task,
        )
        self.btn_edit.grid(row=0, column=1, padx=5, pady=5)

        self.btn_delete = tk.Button(
            self.frame_buttons,
            text="✖ Delete Task",
            font=("Arial", 10, "bold"),
            bg="#f44336",
            fg="white",
            width=14,
            command=self.delete_task,
        )
        self.btn_delete.grid(row=1, column=0, padx=5, pady=5)

        self.btn_clear = tk.Button(
            self.frame_buttons,
            text="Clear All",
            font=("Arial", 10, "bold"),
            bg="#607d8b",
            fg="white",
            width=14,
            command=self.clear_all,
        )
        self.btn_clear.grid(row=1, column=1, padx=5, pady=5)

        self.refresh_listbox()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    return json.load(file)
            except Exception:
                return []
        return []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        task_text = self.entry_task.get().strip()
        if task_text:
            self.tasks.append({"title": task_text, "done": False})
            self.save_tasks()
            self.refresh_listbox()
            self.entry_task.delete(0, tk.END)
        else:
            messagebox.showwarning(
                "Input Error", "Please enter a task description."
            )

    def toggle_done(self):
        try:
            index = self.listbox_tasks.curselection()[0]
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            self.save_tasks()
            self.refresh_listbox()
            self.listbox_tasks.selection_set(index)
        except IndexError:
            messagebox.showwarning(
                "Selection Error", "Please select a task to toggle."
            )

    def edit_task(self):
        try:
            index = self.listbox_tasks.curselection()[0]
            current_title = self.tasks[index]["title"]
            new_title = simpledialog.askstring(
                "Edit Task",
                "Update task description:",
                initialvalue=current_title,
            )
            if new_title and new_title.strip():
                self.tasks[index]["title"] = new_title.strip()
                self.save_tasks()
                self.refresh_listbox()
                self.listbox_tasks.selection_set(index)
        except IndexError:
            messagebox.showwarning(
                "Selection Error", "Please select a task to update."
            )

    def delete_task(self):
        try:
            index = self.listbox_tasks.curselection()[0]
            del self.tasks[index]
            self.save_tasks()
            self.refresh_listbox()
        except IndexError:
            messagebox.showwarning(
                "Selection Error", "Please select a task to delete."
            )

    def clear_all(self):
        if self.tasks:
            if messagebox.askyesno(
                "Confirm", "Are you sure you want to delete all tasks?"
            ):
                self.tasks = []
                self.save_tasks()
                self.refresh_listbox()
        else:
            messagebox.showinfo("Empty List", "There are no tasks to clear.")

    def refresh_listbox(self):
        self.listbox_tasks.delete(0, tk.END)
        for task in self.tasks:
            status = "[✓] " if task["done"] else "[ ] "
            self.listbox_tasks.insert(tk.END, f"{status}{task['title']}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()