import tkinter as tk
import random
import json
import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

def server_listener():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if not data: continue
                    
                    message = data.decode('utf-8')

                    if message == "EXIT":
                        print("Отримано команду EXIT. Завершення роботи.")
                        root.after(0, root.destroy)
                        break
                    
                    try:
                        params = json.loads(message)
                        done_event = threading.Event()
                        root.after(0, lambda: perform_generation(params, done_event))
                        done_event.wait()
                        conn.sendall(b"DONE")
                    except json.JSONDecodeError:
                        pass
                    
            except Exception as e:
                print(f"Server Error: {e}")
                break

def perform_generation(params, event):
    try:
        n = params['n']
        mn = params['min']
        mx = params['max']
        
        numbers = [round(random.uniform(mn, mx), 2) for _ in range(n)]
        
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
        
        print("Object2: Згенеровано і записано.")
    except Exception as e:
        print(f"Error in gen: {e}")
    finally:
        event.set()

root = tk.Tk()
root.title("Object 2")
root.geometry("450x300+530+50")

tk.Label(root, text="Object 2 (Generator)", font=("Arial", 13, "bold")).pack(pady=5)
text_area = tk.Text(root, height=12, width=60, font=("Consolas", 10)) 
text_area.pack(pady=5, padx=10)

t = threading.Thread(target=server_listener, daemon=True)
t.start()

root.mainloop()