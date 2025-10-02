import tkinter as tk
from tkinter import messagebox
from editors import PointEditor, LineEditor, RectEditor, EllipseEditor

class DrawingApp:
   
    MAX_SHAPES = 128
    
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторна робота 2. Хубеджева Єлизавета")
        self.root.geometry("950x600")
        
        self.shapes = [None] * self.MAX_SHAPES
        self.shape_count = 0
        
        self.current_editor = None
        self.current_tool = None
        
        self.create_menu()
        self.create_canvas()
        self.create_status_bar()
        
        self.editors = {
            'point': PointEditor(self.canvas),
            'line': LineEditor(self.canvas),
            'rect': RectEditor(self.canvas),
            'ellipse': EllipseEditor(self.canvas)
        }
        
        self.select_tool('point')
        
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Очистити", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        
        self.objects_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Об'єкти", menu=self.objects_menu)
        self.tool_var = tk.StringVar(value='point')
        self.objects_menu.add_radiobutton(
            label="Точка", 
            variable=self.tool_var,
            value='point',
            command=lambda: self.select_tool('point')
        )
        self.objects_menu.add_radiobutton(
            label="Лінія", 
            variable=self.tool_var,
            value='line',
            command=lambda: self.select_tool('line')
        )
        self.objects_menu.add_radiobutton(
            label="Прямокутник", 
            variable=self.tool_var,
            value='rect',
            command=lambda: self.select_tool('rect')
        )
        self.objects_menu.add_radiobutton(
            label="Еліпс", 
            variable=self.tool_var,
            value='ellipse',
            command=lambda: self.select_tool('ellipse')
        )
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self.show_about)
    
    def create_canvas(self):
        self.canvas = tk.Canvas(
            self.root, 
            bg="white", 
            cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        self.status_bar = tk.Label(
            self.root, 
            text="Вибрано: Точка | Об'єктів: 0/128",
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def select_tool(self, tool):
        self.current_tool = tool
        self.current_editor = self.editors[tool]
        self.tool_var.set(tool)
        self.update_status()
    
    def on_mouse_down(self, event):
        if self.current_editor and self.shape_count < self.MAX_SHAPES:
            self.current_editor.on_mouse_down(event)
    
    def on_mouse_move(self, event):
        if self.current_editor:
            self.current_editor.on_mouse_move(event)
    
    def on_mouse_up(self, event):
        if self.current_editor and self.shape_count < self.MAX_SHAPES:
            shape = self.current_editor.on_mouse_up(event)
            if shape:
                self.add_shape(shape)
    
    def add_shape(self, shape):
        if self.shape_count < self.MAX_SHAPES:
            self.shapes[self.shape_count] = shape
            self.shape_count += 1
            shape.show(self.canvas)
            self.update_status()
        else:
            messagebox.showwarning(
                "Увага", 
                "Досягнуто максимальну кількість об'єктів (128)"
            )
    
    def clear_canvas(self):
        if self.shape_count > 0:
            result = messagebox.askyesno(
                "Підтвердження", 
                "Ви впевнені, що хочете очистити полотно?"
            )
            if result:
                self.canvas.delete("all")
                self.shapes = [None] * self.MAX_SHAPES
                self.shape_count = 0
                self.update_status()
    
    def update_status(self):
        tool_names = {
            'point': 'Точка',
            'line': 'Лінія',
            'rect': 'Прямокутник',
            'ellipse': 'Еліпс'
        }
        current_tool_name = tool_names.get(self.current_tool, "Невідомо")
        self.status_bar.config(
            text=f"Вибрано: {current_tool_name} | Об'єктів: {self.shape_count}/{self.MAX_SHAPES}"
        )
    
    def show_about(self):
        messagebox.showinfo(
            "Про програму",
            "Програма для малювання геометричних фігур\n\n"
            "Автор: Хубеджева Єлизавета\n\n"
            "Підтримувані фігури:\n"
            "• Точка\n"
            "• Лінія\n"
            "• Прямокутник\n"
            "• Еліпс\n\n"
            "Максимальна кількість об'єктів: 128"
        )
    
    def run(self):
        self.root.mainloop()