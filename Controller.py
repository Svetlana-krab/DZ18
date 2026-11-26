from tkinter import messagebox
import matplotlib.pyplot as plt

class PatientController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.view.btn_add.config(command=self.add_patient)
        self.view.btn_edit.config(command=self.edit_patient)
        self.view.btn_stats.config(command=self.show_stats)
        
        self.view.update_table(self.model.get_all())

    def add_patient(self):
        data = self.view.get_inputs()
        # Проверка на заполненность (отчество может быть пустым, поэтому проверяем отдельно)
        if not data["surname"] or not data["name"] or not data["age"] or not data["gender"] or not data["height"] or not data["weight"]:
            messagebox.showerror("Ошибка", "Заполните обязательные поля (Фамилия, Имя, Возраст, Пол, Рост, Вес)!")
            return

        try:
            age = int(data["age"])
            height = float(data["height"])
            weight = float(data["weight"])
            bmi = self.model.calculate_bmi(weight, height)
        except ValueError:
            messagebox.showerror("Ошибка", "Возраст, рост и вес должны быть числами!")
            return

        patient = {
            "surname": data["surname"], 
            "name": data["name"], 
            "patronymic": data["patronymic"],
            "age": age, 
            "gender": data["gender"],
            "height": height, 
            "weight": weight, 
            "bmi": bmi
        }
        self.model.add(patient)
        self.view.update_table(self.model.get_all())
        self.view.clear_inputs()

    def edit_patient(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пациента!")
            return
        
        item_id = selected[0]
        idx = self.view.tree.index(item_id)
        p = self.model.get_all()[idx]

        self.view.set_inputs(p)
        
        self.model.remove_by_index(idx)
        self.view.tree.delete(item_id)

    def show_stats(self):
        patients = self.model.get_all()
        if not patients:
            messagebox.showwarning("Внимание", "Нет данных для статистики!")
            return

        males = [p for p in patients if p["gender"] == "М"]
        females = [p for p in patients if p["gender"] == "Ж"]
        undefined = [p for p in patients if p["gender"] == "Неопределенный"]
        
        ages = [p["age"] for p in patients]
        bmis = [p["bmi"] for p in patients]
        
        bmi_males = [p["bmi"] for p in males]
        bmi_females = [p["bmi"] for p in females]
        bmi_undefined = [p["bmi"] for p in undefined]

        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        fig.canvas.manager.set_window_title('Сводная статистика')

        # 1. Распределение по полу (теперь 3 категории)
        genders = ["М", "Ж", "Неопр."]
        counts = [len(males), len(females), len(undefined)]
        colors = ["#4a90e2", "#ff9999", "#cccccc"]
        axs[0, 0].bar(genders, counts, color=colors)
        axs[0, 0].set_title("Распределение по полу")

        # 2. Распределение по возрасту
        axs[0, 1].hist(ages, bins=10, color="#8ab6d6", edgecolor="black")
        axs[0, 1].set_title("Распределение по возрасту")

        # 3. Распределение ИМТ с учётом пола
        # Используем гистограммы наложения, чтобы было видно все 3 категории
        axs[1, 0].hist([bmi_males, bmi_females, bmi_undefined], bins=10, 
                       label=["М", "Ж", "Неопр."], color=colors, alpha=0.7)
        axs[1, 0].set_title("ИМТ с учётом пола")
        axs[1, 0].legend()

        # 4. Зависимость ИМТ от возраста
        axs[1, 1].scatter(ages, bmis, color="purple", alpha=0.6)
        axs[1, 1].set_title("Зависимость ИМТ от возраста")
        axs[1, 1].set_xlabel("Возраст")
        axs[1, 1].set_ylabel("ИМТ")

        plt.tight_layout()
        plt.show()