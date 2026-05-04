import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import string
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных паролей")
        self.root.geometry("600x500")
        
        # Переменные
        self.length_var = tk.IntVar(value=12)
        self.digits_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.history_file = "password_history.json"
        self.history = self.load_history()
        
        self.setup_ui()
        self.update_history_table()
    
    def setup_ui(self):
        # Фрейм настроек
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Ползунок длины
        ttk.Label(settings_frame, text="Длина:").grid(row=0, column=0, sticky="w")
        self.length_scale = ttk.Scale(settings_frame, from_=4, to=50, variable=self.length_var, orient="horizontal")
        self.length_scale.grid(row=0, column=1, sticky="ew", padx=5)
        self.length_label = ttk.Label(settings_frame, text="12")
        self.length_label.grid(row=0, column=2)
        self.length_scale.config(command=self.update_length_label)
        
        # Чекбоксы
        ttk.Checkbutton(settings_frame, text="Цифры", variable=self.digits_var).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(settings_frame, text="Заглавные буквы", variable=self.upper_var).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(settings_frame, text="Строчные буквы", variable=self.lower_var).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(settings_frame, text="Спецсимволы", variable=self.symbols_var).grid(row=2, column=1, sticky="w")
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Поле пароля и кнопки
        password_frame = ttk.Frame(self.root)
        password_frame.pack(fill="x", padx=10, pady=5)
        
        self.password_entry = ttk.Entry(password_frame, font=("Courier", 12), justify="center")
        self.password_entry.pack(side="left", fill="x", expand=True)
        
        ttk.Button(password_frame, text="Генерировать", command=self.generate_password).pack(side="right", padx=5)
        ttk.Button(password_frame, text="Копировать", command=self.copy_password).pack(side="right")
        
        # История
        history_frame = ttk.LabelFrame(self.root, text="История паролей", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Таблица
        columns = ("Длина", "Пароль", "Дата")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)
        
        ttk.Button(history_frame, text="Очистить историю", command=self.clear_history).pack(pady=5)
    
    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))
    
    def get_charset(self):
        charset = ""
        if self.digits_var.get():
            charset += string.digits
        if self.upper_var.get():
            charset += string.ascii_uppercase
        if self.lower_var.get():
            charset += string.ascii_lowercase
        if self.symbols_var.get():
            charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not charset:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return ""
        return charset
    
    def generate_password(self):
        length = self.length_var.get()
        if length < 4 or length > 50:
            messagebox.showerror("Ошибка", "Длина должна быть от 4 до 50 символов!")
            return
        
        charset = self.get_charset()
        if not charset:
            return
        
        password = ''.join(random.choice(charset) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        
        # Сохранить в историю
        entry = {
            "length": length,
            "password": password,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.history.insert(0, entry)
        if len(self.history) > 100:  # Лимит 100 записей
            self.history = self.history[:100]
        self.save_history()
        self.update_history_table()
    
    def copy_password(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.password_entry.get())
        messagebox.showinfo("Копировано", "Пароль скопирован в буфер обмена!")
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def update_history_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.history[-20:]:  # Последние 20
            self.tree.insert("", "end", values=(entry["length"], entry["password"][:20] + "..." if len(entry["password"]) > 20 else entry["password"], entry["timestamp"]))
    
    def clear_history(self):
        self.history = []
        self.save_history()
        self.update_history_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
