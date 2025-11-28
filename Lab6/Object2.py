import tkinter as tk
import random
import json
import time

PARAMS_FILE = "params.json"
COMMAND_FILE = "command.txt"

def check_for_commands():
    try:
        with open(COMMAND_FILE, "r") as f:
            cmd = f.read().strip()
        
        if cmd == "START_OBJ2":
            perform_task()
            
    except Exception:
        pass
    
    root.after(500, check_for_commands)

def perform_task():
    try:
        with open(PARAMS_FILE, "r") as f:
            data = json.load(f)
        
        n = data['n']
        min_val = data['min']
        max_val = data['max']
        
        numbers = [round(random.uniform(min_val, max_val), 2) for _ in range(n)]
        
        text_area.delete('1.0', tk.END)
        formatted_text = ""
        for i, num in enumerate(numbers):
            formatted_text += f"{num:^10}"
            if (i + 1) % 5 == 0:
                formatted_text += "\n"
        text_area.insert(tk.END, formatted_text)
        
        root.clipboard_clear()
        root.clipboard_append(json.dumps(numbers))
        root.update()
        
        with open(COMMAND_FILE, "w") as f:
            f.write("DONE_OBJ2")
            
    except Exception as e:
        print(f"Object2 Error: {e}")

root = tk.Tk()
root.title("Object 2")
root.geometry("450x300+560+50")

tk.Label(root, text="Object 2 (Generator)", font=("Arial", 13)).pack()
text_area = tk.Text(root, height=10, width=60, font=("Consolas", 12)) 
text_area.pack(pady=10)

root.after(500, check_for_commands)
root.mainloop()