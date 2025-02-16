import tkinter as tk
from tkinter import messagebox, simpledialog


class GradingApp:
    def __init__(self, root):  
        self.root = root
        self.root.title("Grading System")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f8ff")

        self.template = {}  
        self.students = {} 

        self.create_template_ui()

    
    def create_template_ui(self):
        self.clear_frame()
        self.create_template_frame = tk.Frame(self.root, bg="#e6f7ff", bd=2, relief="groove")
        self.create_template_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(
            self.create_template_frame,
            text="Create Grading Template",
            font=("Helvetica", 18, "bold"),
            bg="#e6f7ff",
            fg="#004d99",
        ).pack(pady=15)

        self.num_criteria_var = tk.StringVar()
        tk.Label(
            self.create_template_frame,
            text="Enter the number of grading criteria:",
            font=("Arial", 12),
            bg="#e6f7ff",
        ).pack(pady=5)
        tk.Entry(self.create_template_frame, textvariable=self.num_criteria_var, font=("Arial", 12), width=10).pack(pady=5)

        tk.Button(
            self.create_template_frame,
            text="Next",
            font=("Arial", 12),
            bg="#004d99",
            fg="white",
            command=self.add_criteria_ui,
        ).pack(pady=15)

    def add_criteria_ui(self):
        try:
            self.num_criteria = int(self.num_criteria_var.get())
            if self.num_criteria <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")
            return

        self.clear_frame()
        self.create_template_frame = tk.Frame(self.root, bg="#e6f7ff", bd=2, relief="groove")
        self.create_template_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(
            self.create_template_frame,
            text="Define Grading Criteria",
            font=("Helvetica", 18, "bold"),
            bg="#e6f7ff",
            fg="#004d99",
        ).pack(pady=15)

        self.criteria_entries = []
        self.weightage_entries = []

        for i in range(self.num_criteria):
            tk.Label(
                self.create_template_frame,
                text=f"Criterion {i + 1}:",
                font=("Arial", 12),
                bg="#e6f7ff",
            ).pack(anchor="w", padx=20)
            criterion_entry = tk.Entry(self.create_template_frame, font=("Arial", 12), width=20)
            criterion_entry.pack(pady=5, padx=20)
            self.criteria_entries.append(criterion_entry)

            tk.Label(
                self.create_template_frame,
                text=f"Weightage (%) for Criterion {i + 1}:",
                font=("Arial", 12),
                bg="#e6f7ff",
            ).pack(anchor="w", padx=20)
            weightage_entry = tk.Entry(self.create_template_frame, font=("Arial", 12), width=20)
            weightage_entry.pack(pady=5, padx=20)
            self.weightage_entries.append(weightage_entry)

        tk.Button(
            self.create_template_frame,
            text="Submit",
            font=("Arial", 12),
            bg="#004d99",
            fg="white",
            command=self.save_template,
        ).pack(pady=15)

    def save_template(self):
        self.template = {}
        total_weight = 0
        try:
            for criterion_entry, weightage_entry in zip(self.criteria_entries, self.weightage_entries):
                criterion = criterion_entry.get().strip()
                if not criterion:
                    raise ValueError("Criteria names cannot be empty.")
                weightage = weightage_entry.get().strip()
                weightage = float(weightage)  # Convert to float
                if weightage < 0 or weightage > 100:
                    raise ValueError("Weightages must be between 0 and 100.")
                self.template[criterion] = weightage / 100
                total_weight += weightage
            if total_weight != 100:
                raise ValueError("Total weightage must add up to 100%.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Success", "Grading template created successfully!")
        self.grade_students_ui()


    def grade_students_ui(self):
        self.clear_frame()
        self.grade_students_frame = tk.Frame(self.root, bg="#e6f7ff", bd=2, relief="groove")
        self.grade_students_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(
            self.grade_students_frame,
            text="Grade Students",
            font=("Helvetica", 18, "bold"),
            bg="#e6f7ff",
            fg="#004d99",
        ).pack(pady=15)

        self.num_students_var = tk.StringVar()
        tk.Label(
            self.grade_students_frame,
            text="Enter the number of students:",
            font=("Arial", 12),
            bg="#e6f7ff",
        ).pack(pady=5)
        tk.Entry(self.grade_students_frame, textvariable=self.num_students_var, font=("Arial", 12), width=10).pack(pady=5)

        tk.Button(
            self.grade_students_frame,
            text="Next",
            font=("Arial", 12),
            bg="#004d99",
            fg="white",
            command=self.add_student_scores_ui,
        ).pack(pady=15)

    def add_student_scores_ui(self):
        try:
            self.num_students = int(self.num_students_var.get())
            if self.num_students <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")
            return

        self.students = {}
        for _ in range(self.num_students):
            name = simpledialog.askstring("Student Name", "Enter the student's name:")
            if not name:
                messagebox.showerror("Error", "Student name cannot be empty.")
                return

            scores = {}
            for criterion in self.template:
                while True:
                    try:
                        score = float(simpledialog.askstring("Score", f"Enter the score for '{criterion}' (out of 10):"))
                        if 0 <= score <= 10:
                            scores[criterion] = score
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid score between 0 and 10.")

            total_grade = sum(scores[criterion] * self.template[criterion] for criterion in self.template)
            scores['Total Grade'] = round(total_grade, 2)
            self.students[name] = scores

        messagebox.showinfo("Success", "All student scores recorded successfully!")
        self.display_grades_ui()

    def display_grades_ui(self):
        self.clear_frame()
        self.display_frame = tk.Frame(self.root, bg="#e6f7ff", bd=2, relief="groove")
        self.display_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(self.display_frame, text="Final Grades", font=("Helvetica", 18, "bold"), bg="#e6f7ff", fg="#004d99").pack(pady=15)

        for name, scores in self.students.items():
            tk.Label(self.display_frame, text=f"Student: {name}", font=("Arial", 12, "bold"), bg="#e6f7ff").pack(anchor="w", padx=20)
            for criterion, score in scores.items():
                tk.Label(self.display_frame, text=f"  {criterion}: {score}", font=("Arial", 10), bg="#e6f7ff").pack(anchor="w", padx=40)

        tk.Button(self.display_frame, text="Restart", font=("Arial", 12), bg="#004d99", fg="white", command=self.create_template_ui).pack(pady=15)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GradingApp(root)
    root.mainloop()