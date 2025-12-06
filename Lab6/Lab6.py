import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import json
import time
import socket
import threading

HOST = '127.0.0.1'
PORT_OBJ2 = 65432
PORT_OBJ3 = 65433

proc_obj2 = None
proc_obj3 = None
script_dir = os.path.dirname(os.path.abspath(__file__))

def is_running(proc):
    if proc is None: return False
    if proc.poll() is not None: return False
    return True

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        result = s.connect_ex((HOST, port))
        return result == 0

def run_workflow_thread(n_val, min_val, max_val):
    global proc_obj2, proc_obj3
    
    print(f"--- Початок роботи: n={n_val}, range=[{min_val}, {max_val}] ---")

    if is_port_open(PORT_OBJ2):
        print("Manager: Object2 вже запущено")
    else:
        print("Manager: Запуск Object2")
        proc_obj2 = subprocess.Popen([sys.executable, os.path.join(script_dir, 'Object2.py')])
        time.sleep(0.5)

    if is_port_open(PORT_OBJ3):
        print("Manager: Object3 вже запущено ")
    else:
        print("Manager: Запуск Object3")
        proc_obj3 = subprocess.Popen([sys.executable, os.path.join(script_dir, 'Object3.py')])
        time.sleep(0.5)

    try:
        print(f"Manager: Надсилання параметрів до Object2")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT_OBJ2))
            
            msg_data = json.dumps({"n": n_val, "min": min_val, "max": max_val})
            s.sendall(msg_data.encode('utf-8'))
            
            response = s.recv(1024).decode('utf-8')
            
            if response == "DONE":
                print("Manager: Object2 повідомив про завершення.")
            else:
                print("Manager: Помилка від Object2.")
                return 
    except ConnectionRefusedError:
        messagebox.showerror("Помилка", "Object2 не відповідає (порт закритий).")
        return
    except Exception as e:
        print(f"Помилка комунікації з Object2: {e}")
        return

    try:
        print(f"Manager: Надсилання команди START до Object3")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT_OBJ3))
            
            s.sendall(b"START")
            
            response = s.recv(1024).decode('utf-8')
            
            if response == "DONE":
                print("Manager: Object3 повідомив про завершення.")
    except Exception as e:
        print(f"Помилка комунікації з Object3: {e}")

def open_input_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Введення параметрів")
    dialog.geometry("300x200")
    dialog.grab_set() 

    tk.Label(dialog, text="Введіть параметри:", font=("Arial", 10, "bold")).pack(pady=10)
    frame_d = tk.Frame(dialog)
    frame_d.pack(pady=5)

    tk.Label(frame_d, text="n:").grid(row=0, column=0, padx=5, pady=5)
    d_entry_n = tk.Entry(frame_d, width=10); d_entry_n.grid(row=0, column=1); d_entry_n.insert(0, "10")

    tk.Label(frame_d, text="Min:").grid(row=1, column=0, padx=5, pady=5)
    d_entry_min = tk.Entry(frame_d, width=10); d_entry_min.grid(row=1, column=1); d_entry_min.insert(0, "1.0")

    tk.Label(frame_d, text="Max:").grid(row=2, column=0, padx=5, pady=5)
    d_entry_max = tk.Entry(frame_d, width=10); d_entry_max.grid(row=2, column=1); d_entry_max.insert(0, "100.0")

    def on_submit():
        try:
            n = int(d_entry_n.get())
            mn = float(d_entry_min.get())
            mx = float(d_entry_max.get())
            dialog.destroy()
            threading.Thread(target=run_workflow_thread, args=(n, mn, mx), daemon=True).start()
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні числа")

    tk.Button(dialog, text="Виконати", command=on_submit, bg="lightblue", width=15).pack(pady=15)

def send_exit_command(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((HOST, port))
            s.sendall(b"EXIT")
            print(f"Manager: Надіслано EXIT на порт {port}")
    except (ConnectionRefusedError, socket.timeout):
        pass
    except Exception as e:
        print(f"Помилка при закритті порту {port}: {e}")

def on_closing():
    global proc_obj2, proc_obj3
    
    if is_running(proc_obj2): 
        proc_obj2.terminate()
    else:
        send_exit_command(PORT_OBJ2)

    if is_running(proc_obj3): 
        proc_obj3.terminate()
    else:
        send_exit_command(PORT_OBJ3)
    
    root.destroy()

root = tk.Tk()
root.title("Lab6 Manager")
root.geometry("450x300+50+50")

main_menu = tk.Menu(root)
root.config(menu=main_menu)
file_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Вихід", command=on_closing)
main_menu.add_command(label="Порахувати", command=open_input_dialog)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()