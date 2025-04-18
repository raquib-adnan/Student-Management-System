import tkinter as tk
from tkinter import ttk, messagebox
from db import Database
import re

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")
        self.db = Database()

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create search frame
        self.search_frame = ttk.LabelFrame(self.main_frame, text="Search", padding="5")
        self.search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_students)
        ttk.Entry(self.search_frame, textvariable=self.search_var, width=40).grid(row=0, column=0, padx=5)
        ttk.Button(self.search_frame, text="Clear", command=self.clear_search).grid(row=0, column=1, padx=5)

        # Create student form frame
        self.form_frame = ttk.LabelFrame(self.main_frame, text="Student Details", padding="5")
        self.form_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Form fields
        ttk.Label(self.form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(self.form_frame, text="Roll No:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.roll_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.roll_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(self.form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.email_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.email_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(self.form_frame, text="Course:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.course_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.course_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)

        # Buttons
        self.button_frame = ttk.Frame(self.form_frame)
        self.button_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(self.button_frame, text="Add", command=self.add_student).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Update", command=self.update_student).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="Delete", command=self.delete_student).grid(row=0, column=2, padx=5)
        ttk.Button(self.button_frame, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=5)

        # Create Treeview
        self.tree_frame = ttk.LabelFrame(self.main_frame, text="Students List", padding="5")
        self.tree_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Name", "Roll No", "Email", "Course"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Roll No", text="Roll No")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Course", text="Course")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Roll No", width=100)
        self.tree.column("Email", width=200)
        self.tree.column("Course", width=150)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Load initial data
        self.load_students()

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_form(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Name is required")
            return False
        if not self.roll_var.get().strip():
            messagebox.showerror("Error", "Roll number is required")
            return False
        if not self.email_var.get().strip():
            messagebox.showerror("Error", "Email is required")
            return False
        if not self.validate_email(self.email_var.get()):
            messagebox.showerror("Error", "Invalid email format")
            return False
        if not self.course_var.get().strip():
            messagebox.showerror("Error", "Course is required")
            return False
        return True

    def add_student(self):
        if not self.validate_form():
            return
        
        if self.db.add_student(
            self.name_var.get().strip(),
            self.roll_var.get().strip(),
            self.email_var.get().strip(),
            self.course_var.get().strip()
        ):
            messagebox.showinfo("Success", "Student added successfully")
            self.clear_form()
            self.load_students()
        else:
            messagebox.showerror("Error", "Roll number or email already exists")

    def update_student(self):
        if not self.validate_form():
            return
        
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to update")
            return

        student_id = self.tree.item(selected_item[0])['values'][0]
        if self.db.update_student(
            student_id,
            self.name_var.get().strip(),
            self.roll_var.get().strip(),
            self.email_var.get().strip(),
            self.course_var.get().strip()
        ):
            messagebox.showinfo("Success", "Student updated successfully")
            self.clear_form()
            self.load_students()
        else:
            messagebox.showerror("Error", "Roll number or email already exists")

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            student_id = self.tree.item(selected_item[0])['values'][0]
            if self.db.delete_student(student_id):
                messagebox.showinfo("Success", "Student deleted successfully")
                self.clear_form()
                self.load_students()
            else:
                messagebox.showerror("Error", "Failed to delete student")

    def load_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        students = self.db.get_all_students()
        for student in students:
            self.tree.insert('', 'end', values=student)

    def search_students(self, *args):
        query = self.search_var.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        students = self.db.search_students(query)
        for student in students:
            self.tree.insert('', 'end', values=student)

    def clear_search(self):
        self.search_var.set("")
        self.load_students()

    def clear_form(self):
        self.name_var.set("")
        self.roll_var.set("")
        self.email_var.set("")
        self.course_var.set("")

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])['values']
            self.name_var.set(values[1])
            self.roll_var.set(values[2])
            self.email_var.set(values[3])
            self.course_var.set(values[4])

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop() 