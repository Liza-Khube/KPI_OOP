import tkinter as tk
import json
import socket
import threading

HOST = '127.0.0.1'
PORT = 65433

def server_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    cmd = conn.recv(1024).decode('utf-8')
                    
                    if cmd == "EXIT":
                        print("Отримано команду EXIT. Завершення роботи.")
                        root.after(0, root.destroy)
                        break

                    if cmd == "START":
                        done_event = threading.Event()
                        root.after(0, lambda: perform_sorting(done_event))
                        done_event.wait()
                        conn.sendall(b"DONE")
                        
            except Exception as e:
                print(f"Server Error: {e}")
                break

def perform_sorting(event):
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
        
        print("Object3: Відсортовано.")
    except Exception as e:
        print(f"Error in sort: {e}")
    finally:
        event.set()

root = tk.Tk()
root.title("Object 3")
root.geometry("450x300+1000+50")

tk.Label(root, text="Object 3 (Sorter)", font=("Arial", 13, "bold")).pack(pady=5)
text_area = tk.Text(root, height=12, width=60, font=("Consolas", 10))
text_area.pack(pady=5, padx=10)

t = threading.Thread(target=server_listener, daemon=True)
t.start()

root.mainloop()