import tkinter as tk
from tkinter import ttk

class PatientView:
    def __init__(self, root):
        self.root = root
        self.root.title("Пациенты (MVC)")
        # Расширили окно, чтобы кнопки влезли в один ряд
        self.root.geometry("1300x650")

        label_font = ("Arial", 12, "bold")
        entry_font = ("Arial", 12)
        btn_font = ("Arial", 12)

        frame_input = tk.Frame(root, pady=15)
        frame_input.pack(fill="x", padx=10)

        # --- Поля ввода ---
        tk.Label(frame_input, text="Фамилия:", font=label_font).grid(row=0, column=0, padx=2, sticky="e")
        self.entry_surname = tk.Entry(frame_input, width=18, font=entry_font)
        self.entry_surname.grid(row=0, column=1, padx=2)

        tk.Label(frame_input, text="Имя:", font=label_font).grid(row=0, column=2, padx=2, sticky="e")
        self.entry_name = tk.Entry(frame_input, width=15, font=entry_font)
        self.entry_name.grid(row=0, column=3, padx=2)

        tk.Label(frame_input, text="Отчество:", font=label_font).grid(row=0, column=4, padx=2, sticky="e")
        self.entry_patronymic = tk.Entry(frame_input, width=18, font=entry_font)
        self.entry_patronymic.grid(row=0, column=5, padx=2)

        tk.Label(frame_input, text="Возраст:", font=label_font).grid(row=1, column=0, padx=2, pady=10, sticky="e")
        self.entry_age = tk.Entry(frame_input, width=8, font=entry_font)
        self.entry_age.grid(row=1, column=1, padx=2, pady=10)

        tk.Label(frame_input, text="Пол:", font=label_font).grid(row=1, column=2, padx=2, pady=10, sticky="e")
        self.combo_gender = ttk.Combobox(frame_input, values=["М", "Ж", "Неопределенный"], width=14, state="readonly", font=entry_font)
        self.combo_gender.grid(row=1, column=3, padx=2, pady=10)

        tk.Label(frame_input, text="Рост (см):", font=label_font).grid(row=1, column=4, padx=2, pady=10, sticky="e")
        self.entry_height = tk.Entry(frame_input, width=8, font=entry_font)
        self.entry_height.grid(row=1, column=5, padx=2, pady=10)

        tk.Label(frame_input, text="Вес (кг):", font=label_font).grid(row=1, column=6, padx=2, pady=10, sticky="e")
        self.entry_weight = tk.Entry(frame_input, width=8, font=entry_font)
        self.entry_weight.grid(row=1, column=7, padx=2, pady=10)

        # --- Кнопки ---
        frame_btns = tk.Frame(root, pady=10)
        frame_btns.pack()

        # Увеличили width до 22, теперь текст точно поместится
        self.btn_add = tk.Button(frame_btns, text="Добавить", bg="#a0c4ff", font=btn_font, width=22)
        self.btn_add.pack(side="left", padx=10)
        
        self.btn_edit = tk.Button(frame_btns, text="Редактировать", bg="#cceeff", font=btn_font, width=22)
        self.btn_edit.pack(side="left", padx=10)

        self.btn_delete = tk.Button(frame_btns, text="Удалить", bg="#ff9999", font=btn_font, width=22)
        self.btn_delete.pack(side="left", padx=10)
        
        self.btn_stats = tk.Button(frame_btns, text="Статистика", bg="#b3d9ff", font=btn_font, width=22)
        self.btn_stats.pack(side="left", padx=10)

        # --- Таблица ---
        columns = ("Фамилия", "Имя", "Отчество", "Возраст", "Пол", "Рост", "Вес", "ИМТ")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Arial", 11))

        widths = [150, 120, 150, 80, 120, 80, 80, 80]
        for col, w in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def get_inputs(self):
        return {
            "surname": self.entry_surname.get().strip(),
            "name": self.entry_name.get().strip(),
            "patronymic": self.entry_patronymic.get().strip(),
            "age": self.entry_age.get().strip(),
            "gender": self.combo_gender.get(),
            "height": self.entry_height.get().strip(),
            "weight": self.entry_weight.get().strip()
        }

    def clear_inputs(self):
        self.entry_surname.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_patronymic.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_height.delete(0, tk.END)
        self.entry_weight.delete(0, tk.END)

    def set_inputs(self, p):
        self.clear_inputs()
        self.entry_surname.insert(0, p["surname"])
        self.entry_name.insert(0, p["name"])
        self.entry_patronymic.insert(0, p["patronymic"])
        self.entry_age.insert(0, p["age"])
        self.combo_gender.set(p["gender"])
        self.entry_height.insert(0, p["height"])
        self.entry_weight.insert(0, p["weight"])

    def update_table(self, patients):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in patients:
            self.tree.insert("", "end", values=(
                p["surname"], p["name"], p["patronymic"], 
                p["age"], p["gender"], p["height"], p["weight"], p["bmi"]
            ))