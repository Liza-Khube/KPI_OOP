import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import json
import time

proc_obj2 = None
proc_obj3 = None
script_dir = os.path.dirname(os.path.abspath(__file__))
PARAMS_FILE = "params.json"
COMMAND_FILE = "command.txt"

def ensure_files_exist():
    if not os.path.exists(PARAMS_FILE):
        with open(PARAMS_FILE, "w") as f: f.write("{}")
    if not os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE, "w") as f: f.write("IDLE")

def is_running(proc):
    if proc is None:
        return False
    if proc.poll() is not None:
        return False
    return True

def start_automation(n_val, min_val, max_val):
    global proc_obj2
    
    print(f"--- Початок роботи: n={n_val}, range=[{min_val}, {max_val}] ---")

    data = {"n": n_val, "min": min_val, "max": max_val}

    if not is_running(proc_obj2):
        print("Запуск Object2...")
        proc_obj2 = subprocess.Popen([sys.executable, os.path.join(script_dir, 'Object2.py')])
        time.sleep(1) 
    else:
        print("Object2 вже активний.")

    try:
        with open(PARAMS_FILE, "w") as f:
            json.dump(data, f)
        
        with open(COMMAND_FILE, "w") as f:
            f.write("START_OBJ2")
        
        print("Команду START_OBJ2 надіслано.")
        
        root.after(500, check_obj2_finished)
        
    except Exception as e:
        messagebox.showerror("Помилка", f"Файлова помилка: {e}")

def check_obj2_finished():
    try:
        with open(COMMAND_FILE, "r") as f:
            status = f.read().strip()
            
        if status == "DONE_OBJ2":
            print("Object2 завершив генерацію.")
            run_object3_scenario() 
        else:
            root.after(500, check_obj2_finished)
    except:
        root.after(500, check_obj2_finished)

def run_object3_scenario():
    global proc_obj3
    
    if not is_running(proc_obj3):
        print("Запуск Object3...")
        proc_obj3 = subprocess.Popen([sys.executable, os.path.join(script_dir, 'Object3.py')])
        time.sleep(1)
    else:
        print("Object3 вже активний.")

    with open(COMMAND_FILE, "w") as f:
        f.write("START_OBJ3")
    
    print("Команду START_OBJ3 надіслано.")
    root.after(500, check_obj3_finished)

def check_obj3_finished():
    try:
        with open(COMMAND_FILE, "r") as f:
            status = f.read().strip()
            
        if status == "DONE_OBJ3":
            print("Object3 завершив роботу.")
            with open(COMMAND_FILE, "w") as f: f.write("IDLE")
        else:
            root.after(500, check_obj3_finished)
    except:
        pass

def open_input_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Введення параметрів")
    dialog.geometry("300x200")
    dialog.grab_set() 

    tk.Label(dialog, text="Введіть параметри:", font=("Arial", 10, "bold")).pack(pady=10)

    frame_d = tk.Frame(dialog)
    frame_d.pack(pady=5)

    tk.Label(frame_d, text="n:").grid(row=0, column=0, padx=5, pady=5)
    d_entry_n = tk.Entry(frame_d, width=10)
    d_entry_n.grid(row=0, column=1)
    d_entry_n.insert(0, "10")

    tk.Label(frame_d, text="Min:").grid(row=1, column=0, padx=5, pady=5)
    d_entry_min = tk.Entry(frame_d, width=10)
    d_entry_min.grid(row=1, column=1)
    d_entry_min.insert(0, "1.0")

    tk.Label(frame_d, text="Max:").grid(row=2, column=0, padx=5, pady=5)
    d_entry_max = tk.Entry(frame_d, width=10)
    d_entry_max.grid(row=2, column=1)
    d_entry_max.insert(0, "100.0")

    def on_submit():
        try:
            n = int(d_entry_n.get())
            mn = float(d_entry_min.get())
            mx = float(d_entry_max.get())
            dialog.destroy()
            start_automation(n, mn, mx)
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні числа!")

    tk.Button(dialog, text="Виконати", command=on_submit, bg="lightblue", width=15).pack(pady=15)

def on_closing():
    global proc_obj2, proc_obj3
    if is_running(proc_obj2): proc_obj2.terminate()
    if is_running(proc_obj3): proc_obj3.terminate()
    root.destroy()


ensure_files_exist()
root = tk.Tk()
root.title("Lab6")
root.geometry("500x300+50+50")

main_menu = tk.Menu(root)
root.config(menu=main_menu)

file_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Вихід", command=on_closing)

main_menu.add_command(label="Вектор чисел", command=open_input_dialog)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()