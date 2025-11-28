import tkinter as tk
import json

COMMAND_FILE = "command.txt"

def check_for_commands():
    try:
        with open(COMMAND_FILE, "r") as f:
            cmd = f.read().strip()
        
        if cmd == "START_OBJ3":
            perform_sort()
            
    except Exception:
        pass
    
    root.after(500, check_for_commands)

def perform_sort():
    try:
        content = root.clipboard_get()
        numbers = json.loads(content)

        numbers.sort()

        text_area.delete('1.0', tk.END)
        formatted_text = ""
        for i, num in enumerate(numbers):
            formatted_text += f"{num:^10}"
            if (i + 1) % 5 == 0:
                formatted_text += "\n"
        text_area.insert(tk.END, formatted_text)

        with open(COMMAND_FILE, "w") as f:
            f.write("DONE_OBJ3")
            
    except Exception as e:
        print(f"Object3 Error: {e}")

root = tk.Tk()
root.title("Object 3")
root.geometry("450x300+1020+50")

tk.Label(root, text="Object 3 (Sorter)", font=("Arial", 13)).pack()
text_area = tk.Text(root, height=10, width=60, font=("Consolas", 12))
text_area.pack(pady=10)

root.after(500, check_for_commands)
root.mainloop()