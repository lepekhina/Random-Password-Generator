import json
import os
import random
import string
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


class PasswordGeneratorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("650x450")
        self.root.resizable(False, False)

        self.HISTORY_FILE = "passwords_history.json"

        # Настройка стилей
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Переменные интерфейса
        self.length_var = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_specials = tk.BooleanVar(value=True)

        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # Левая панель: Настройки
        left_frame = ttk.LabelFrame(self.root, text=" Настройки пароля ", padding=15)
        left_frame.place(x=15, y=15, width=280, height=420)

        # Ползунок длины
        ttk.Label(left_frame, text="Длина пароля:").pack(anchor="w", pady=2)
        self.length_label = ttk.Label(
            left_frame, text="12", font=("Arial", 10, "bold")
        )
        self.length_label.pack(anchor="w")

        self.slider = ttk.Scale(
            left_frame,
            from_=4,
            to=32,
            variable=self.length_var,
            orient="horizontal",
            command=self.update_length_label,
        )
        self.slider.pack(fill="x", pady=10)

        # Чекбоксы параметров
        ttk.Checkbutton(
            left_frame, text="Включить цифры (0-9)", variable=self.use_digits
        ).pack(anchor="w", pady=5)
        ttk.Checkbutton(
            left_frame, text="Включить буквы (a-Z)", variable=self.use_letters
        ).pack(anchor="w", pady=5)
        ttk.Checkbutton(
            left_frame, text="Спецсимволы (!@#$%)", variable=self.use_specials
        ).pack(anchor="w", pady=5)

        # Кнопка генерации
        generate_btn = ttk.Button(
            left_frame, text="Сгенерировать", command=self.generate_password
        )
        generate_btn.pack(fill="x", pady=20)

        # Поле вывода результата
        ttk.Label(left_frame, text="Созданный пароль:").pack(anchor="w")
        self.result_entry = ttk.Entry(
            left_frame, font=("Courier", 11, "bold"), justify="center"
        )
        self.result_entry.pack(fill="x", pady=5)

        # Кнопка копирования
        copy_btn = ttk.Button(
            left_frame, text="Копировать в буфер", command=self.copy_to_clipboard
        )
        copy_btn.pack(fill="x", pady=5)

        # Правая панель: История
        right_frame = ttk.LabelFrame(self.root, text=" История генераций ", padding=10)
        right_frame.place(x=310, y=15, width=325, height=420)

        # Таблица истории (Treeview)
        columns = ("date", "password")
        self.tree = ttk.Treeview(
            right_frame, columns=columns, show="headings", selectmode="browse"
        )
        self.tree.heading("date", text="Дата и время")
        self.tree.heading("password", text="Пароль")
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("password", width=180, anchor="w")

        # Скроллбар для таблицы
        scrollbar = ttk.Scrollbar(
            right_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_length_label(self, event=None):
        self.length_label.config(text=str(int(self.length_var.get())))

    def generate_password(self):
        length = int(self.length_var.get())

        # Валидация граничных значений длины
        if length < 4 or length > 32:
            messagebox.showerror(
                "Ошибка валидации", "Длина должна быть от 4 до 32 символов!"
            )
            return

        # Валидация выбора типов символов
        chars = ""
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_specials.get():
            chars += "!@#$%^&*()-_=+[]{};:,.<>?/"

        # Негативный сценарий: ни один чекбокс не выбран
        if not chars:
            messagebox.showwarning(
                "Предупреждение", "Выберите хотя бы один тип символов!"
            )
            return

        # Генерация пароля с помощью random
        password = "".join(random.choice(chars) for _ in range(length))

        # Вывод на экран
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)

        # Добавление в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_to_history(timestamp, password)

    def copy_to_clipboard(self):
        password = self.result_entry.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Внимание", "Сначала сгенерируйте пароль.")

    def save_to_history(self, timestamp, password):
        # Вставка на первое место в таблице интерфейса
        self.tree.insert("", 0, values=(timestamp, password))

        # Сохранение в JSON файл
        history_data = []
        if os.path.exists(self.HISTORY_FILE):
            try:
                with open(self.HISTORY_FILE, "r", encoding="utf-8") as f:
                    history_data = json.load(f)
            except json.JSONDecodeError:
                history_data = []

        # Добавляем новую запись в начало списка
        history_data.insert(0, {"date": timestamp, "password": password})

        # Ограничим историю 50 записями, чтобы не перегружать файл
        history_data = history_data[:50]

        with open(self.HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if not os.path.exists(self.HISTORY_FILE):
            return

        try:
            with open(self.HISTORY_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
                for item in reversed(history_data):
                    self.tree.insert(
                        "", 0, values=(item["date"], item["password"])
                    )
        except (json.JSONDecodeError, KeyError):
            pass  # Если файл поврежден, просто создаем чистую историю


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
