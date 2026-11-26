import tkinter as tk
from tkinter import filedialog, messagebox
from fastq_module import FastqReader  # Импортируем наш модуль

class FastQCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Урезанный FastQC")
        self.root.geometry("600x350")
        self.root.configure(bg="#f0f4f8")

        # Заголовок
        tk.Label(root, text="Анализ FASTQ файлов", font=("Arial", 18, "bold"), bg="#f0f4f8").pack(pady=20)
        
        # Кнопка выбора файла
        self.btn_open = tk.Button(root, text="Выбрать FASTQ файл", font=("Arial", 14), 
                                  bg="#a0c4ff", cursor="hand2", command=self.open_file)
        self.btn_open.pack(pady=10)
        
        # Метка для отображения имени выбранного файла
        self.lbl_file = tk.Label(root, text="Файл не выбран", font=("Arial", 12), bg="#f0f4f8")
        self.lbl_file.pack(pady=10)
        
        # Инструкция
        tk.Label(root, text="(Поддерживаются файлы .fastq, .fq и архивы .gz)", fg="gray", bg="#f0f4f8").pack()

    def open_file(self):
        # Диалог выбора файла с фильтром по форматам (как требует задание)
        filename = filedialog.askopenfilename(
            title="Выберите FASTQ файл",
            filetypes=[
                ("FASTQ files", "*.fastq *.fq"), 
                ("Compressed FASTQ", "*.fastq.gz *.fq.gz"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.lbl_file.config(text=f"Загрузка: {filename.split('/')[-1]}...", fg="black")
            self.root.update() # Обновляем интерфейс, чтобы текст появился сразу
            
            try:
                # Создаем ридер из твоего модуля
                reader = FastqReader(filename)
                
                # Вызываем метод, который считает статистику и показывает графики matplotlib
                reader.plot_all()
                
                self.lbl_file.config(text=f"Готово: {filename.split('/')[-1]}", fg="green")
                
            except Exception as e:
                self.lbl_file.config(text="Ошибка чтения файла", fg="red")
                messagebox.showerror("Ошибка", f"Не удалось обработать файл:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FastQCApp(root)
    root.mainloop()