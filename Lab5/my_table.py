import tkinter as tk
from tkinter import ttk

class MyTable:

    def __init__(self, root, on_row_select_callback=None, on_row_double_click_callback=None):
        self.window = tk.Toplevel(root)
        self.window.title("Таблиця об'єктів")
        self.window.geometry("500x300")
        
        self.window.protocol("WM_DELETE_WINDOW", self.hide)
        
        self.on_row_select_callback = on_row_select_callback
        self.on_row_double_click_callback = on_row_double_click_callback

        frame = ttk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = ("name", "x1", "y1", "x2", "y2")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        self.tree.heading("name", text="Назва об'єкту")
        self.tree.heading("x1", text="X1")
        self.tree.heading("y1", text="Y1")
        self.tree.heading("x2", text="X2")
        self.tree.heading("y2", text="Y2")
        
        self.tree.column("name", width=120)
        for col in cols[1:]:
            self.tree.column(col, width=50, anchor=tk.E)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)
        self.tree.bind("<Double-1>", self._on_row_double_click)
        
        self.window.withdraw()

    def _get_selected_index(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return None
            
        selected_item = selected_items[0]
        return self.tree.index(selected_item)

    def _on_row_select(self, event):
        if not self.on_row_select_callback:
            return
            
        index = self._get_selected_index()
        if index is not None and index >= 0:
            self.on_row_select_callback(index)

    def _on_row_double_click(self, event):
        if not self.on_row_double_click_callback:
            return
        
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
            
        index = self._get_selected_index()
        if index is not None and index >= 0:
            self.on_row_double_click_callback(index)

    def add_row(self, *columns):
        self.tree.insert("", tk.END, values=columns)
        self.tree.see(self.tree.get_children()[-1])

    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def show(self):
        self.window.deiconify()
        self.window.lift()

    def hide(self):
        self.window.withdraw()

    def destroy_window(self):
        self.window.destroy()