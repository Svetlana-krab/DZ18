import tkinter as tk
import math
import re   # защита точки от двойного ввода и подсчёт процентов

#Работа с главным окном root
root = tk.Tk()
root.title("Калькулятор")
root.configure(bg="#e6f2f8")
root.geometry("320x500")
root.resizable(False, False)    #запрет на растяжение окна

#Ввод и валидация
is_error_state = False  

def validate_input(char):
    return char in "0123456789.+-*/()^%"

vcmd = (root.register(validate_input), '%S')

entry = tk.Entry(root, font=("Arial", 20), justify="right", bd=4, relief="ridge", 
                 bg="#ffffff", fg="#2c3e50", validate="key", validatecommand=vcmd)
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
#Для размера шрифта
def adjust_font(event=None):
    text_len = len(entry.get())
    if text_len <= 12:
        size = 20
    elif text_len <= 16:
        size = 16
    elif text_len <= 20:
        size = 12
    else:
        size = 9
    entry.config(font=("Arial", size))

def format_result(val):
    if isinstance(val, float):
        val = round(val, 6)
        if val.is_integer():
            return str(int(val))
        else:
            res_str = f"{val:.6f}".rstrip('0').rstrip('.')
            return res_str
    return str(val)
#Ввод данных и обработка ошибок
def press(s):
    global is_error_state
    if is_error_state:
        entry.config(validate="none")
        entry.delete(0, tk.END)
        entry.config(validate="key")
        is_error_state = False
    
    if s == ".":
        current = entry.get()
        last_num = re.split(r'[+\-*/()^%]', current)[-1]
        if "." in last_num:
            return

    # Временно отключаем валидацию для вставки sqrt
    entry.config(validate="none")
    entry.insert(tk.END, s)
    entry.config(validate="key")
    
    adjust_font()

def show_error(msg):
    global is_error_state
    entry.config(validate="none")
    entry.delete(0, tk.END)
    entry.insert(0, msg)
    entry.config(validate="key")
    is_error_state = True
    adjust_font()

def clear(event=None):
    global is_error_state
    entry.config(validate="none")
    entry.delete(0, tk.END)
    entry.config(validate="key")
    is_error_state = False
    adjust_font()

def backspace(event=None):
    global is_error_state
    if is_error_state:
        clear()
        return "break"
    pos = entry.index(tk.INSERT)
    if pos > 0:
        entry.delete(pos - 1, pos)
    adjust_font()
    return "break"

def calculate(event=None):
    global is_error_state
    if is_error_state:
        clear()
        return "break"
    try:
        expr = entry.get().strip()
        if not expr:
            return "break"
            
        expr = expr.replace('%', '/100')
        
        if "sqrt(" in expr:
            open_brackets = 0
            for char in expr:
                if char == '(':
                    open_brackets += 1
                elif char == ')':
                    open_brackets -= 1
            if open_brackets > 0:
                expr += ")" * open_brackets
        
        expr = expr.replace('^', '**')
        result = eval(expr, {"__builtins__": None}, {"math": math, "sqrt": math.sqrt})
        
        entry.config(validate="none")
        entry.delete(0, tk.END)
        entry.insert(0, format_result(result))
        entry.config(validate="key")
        adjust_font()
    except ZeroDivisionError:
        show_error("Деление на 0!")
    except ValueError:
        show_error("Ошибка (например, корень < 0)")
    except Exception:
        show_error("Ошибка ввода")
    return "break"

def percent_action():
    global is_error_state
    if is_error_state: 
        clear()
        return
    expr = entry.get().strip()
    if not expr: 
        return
    numbers = re.findall(r'\d+\.?\d*', expr)
    if not numbers:
        show_error("Нет числа")
        return
    last_num_str = numbers[-1]
    try:
        last_num = float(last_num_str)
    except:
        return

    if '+' in expr or '-' in expr:
        parts = re.split(r'([+-])', expr)
        if len(parts) >= 3:
            try:
                base_num = float(parts[0])
                perc_val = (base_num * last_num) / 100
                parts[-1] = format_result(perc_val)
                new_expr = "".join(parts)
                entry.config(validate="none")
                entry.delete(0, tk.END)
                entry.insert(0, new_expr)
                entry.config(validate="key")
                adjust_font()
                return
            except:
                pass
    try:
        val = float(eval(expr))
        res = val / 100
        entry.config(validate="none")
        entry.delete(0, tk.END)
        entry.insert(0, format_result(res))
        entry.config(validate="key")
        adjust_font()
    except:
        show_error("Ошибка %")

def create_square_btn(parent, text, cmd, bg_color, fg_color="#2c3e50", font_size=16):
    w, h = 60, 60 
    canvas = tk.Canvas(parent, width=w, height=h, bg="#e6f2f8", highlightthickness=0, cursor="hand2")
    rect = canvas.create_rectangle(0, 0, w, h, fill=bg_color, outline=bg_color)
    if text == "√":
        cx, cy = w/2, h/2
        points_line = [cx-10, cy+2, cx-5, cy+8, cx+2, cy-8, cx+12, cy-8]
        canvas.create_line(points_line, fill=fg_color, width=3, capstyle=tk.ROUND, joinstyle=tk.ROUND)
        canvas.create_line(cx+2, cy-8, cx+4, cy-11, fill=fg_color, width=3, capstyle=tk.ROUND)
    else:
        canvas.create_text(w/2, h/2, text=text, font=("Arial", font_size, "bold"), fill=fg_color)
    
    hover_color = "#cce4ff" if bg_color == "#b3d9ff" else ("#5d9bbd" if bg_color == "#4a90e2" else "#7a9bb5")
    
    def on_enter(e): canvas.itemconfig(rect, fill=hover_color, outline=hover_color)
    def on_leave(e): canvas.itemconfig(rect, fill=bg_color, outline=bg_color)
    def on_click(e):
        cmd()
        entry.focus_set()
        
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)
    return canvas

# Кнопки
square_cmd = lambda: press("^2")
sqrt_cmd = lambda: press("sqrt(")

row1 = [("(", lambda: press("("), "#b3d9ff"), (")", lambda: press(")"), "#b3d9ff"), ("C", clear, "#4a90e2", "white"), ("Del", backspace, "#a0c4ff")]
row2 = [("x²", square_cmd, "#b3d9ff"), ("√", sqrt_cmd, "#b3d9ff"), ("x^y", lambda: press("^"), "#b3d9ff"), ("/", lambda: press("/"), "#4a90e2", "white")]
row3 = [("7", lambda: press("7"), "#b3d9ff"), ("8", lambda: press("8"), "#b3d9ff"), ("9", lambda: press("9"), "#b3d9ff"), ("*", lambda: press("*"), "#4a90e2", "white")]
row4 = [("4", lambda: press("4"), "#b3d9ff"), ("5", lambda: press("5"), "#b3d9ff"), ("6", lambda: press("6"), "#b3d9ff"), ("-", lambda: press("-"), "#4a90e2", "white")]
row5 = [("1", lambda: press("1"), "#b3d9ff"), ("2", lambda: press("2"), "#b3d9ff"), ("3", lambda: press("3"), "#b3d9ff"), ("+", lambda: press("+"), "#4a90e2", "white")]
row6 = [("0", lambda: press("0"), "#b3d9ff"), ("%", percent_action, "#b3d9ff"), (".", lambda: press("."), "#b3d9ff"), ("=", calculate, "#3a7bd5", "white")]

grid_data = [row1, row2, row3, row4, row5, row6]
#Цикл для азмещения кнопок в цикл
for r, row in enumerate(grid_data):
    for c, btn_data in enumerate(row):
        if len(btn_data) == 4:
            text, cmd, color, fg_color = btn_data
        else:
            text, cmd, color = btn_data
            fg_color = "#2c3e50"
        f_size = 20 if text == "√" else 16
        btn = create_square_btn(root, text, cmd, color, fg_color, f_size)
        btn.grid(row=r+1, column=c, padx=2, pady=2)

root.grid_rowconfigure(0, weight=1)
for i in range(1, 7): root.grid_rowconfigure(i, weight=0)
for i in range(4): root.grid_columnconfigure(i, weight=1)
#Для привязки клавиатуры
entry.focus_set()

root.bind("<Button-1>", lambda e: root.focus_set() if e.widget == root else None)
root.bind("<FocusIn>", lambda e: entry.focus_set())

entry.bind("<Return>", calculate)
entry.bind("<KP_Enter>", calculate)
entry.bind("<Escape>", clear)
entry.bind("<BackSpace>", backspace)
entry.bind("<Delete>", clear)

root.mainloop()