import tkinter as tk
from tkinter import messagebox
from toolbar import Toolbar 
from my_editor import MyEditor

class DrawingApp:

    def __init__(self, root):
        self.root = root
        self.base_title = "Лабораторна робота 4. Хубеджева Єлизавета"
        self.root.title(self.base_title)
        self.root.geometry("950x600")

        self.current_tool = 'point'

        self.create_menu()
        self.create_toolbar() 
        self.create_canvas()
        
        self.my_editor = MyEditor(self.canvas, self.update_status)
        
        self.create_status_bar()
        
        self.select_tool('point')
     
        self.canvas.bind("<Button-1>", self.my_editor.on_mouse_down) 
        self.canvas.bind("<B1-Motion>", self.my_editor.on_mouse_move) 
        self.canvas.bind("<ButtonRelease-1>", self.my_editor.on_mouse_up) 

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
        
        menu_items = {
            "Точка": "point",
            "Лінія": "line",
            "Прямокутник": "rect",
            "Еліпс": "ellipse",
            "Лінія з кружечками": "line_oo",
            "Куб": "cube"
        }
        
        for label, tool in menu_items.items():
            self.objects_menu.add_command(
                label=label,
                command=lambda t=tool: self.select_tool(t)
            )
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self.show_about)

    def create_toolbar(self):
        self.toolbar = Toolbar(self.root, self.select_tool)

    def create_canvas(self):
        self.canvas = tk.Canvas(
            self.root, 
            bg="white", 
            cursor="crosshair"
        ) 
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        shape_count = self.my_editor.get_shape_count()
        self.status_bar = tk.Label(
            self.root, 
            text=f"Об'єктів: {shape_count}/{MyEditor.MAX_SHAPES}",
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def select_tool(self, tool):
        self.current_tool = tool
        self.my_editor.select_tool(tool)
        self.toolbar.set_active_tool(tool)
        self.update_status() 

    def clear_canvas(self):
        if self.my_editor.get_shape_count() > 0:
            if messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете очистити полотно?"):
                self.my_editor.clear()
    
    def update_status(self):
        shape_count = self.my_editor.get_shape_count()
        self.status_bar.config(
            text=f"Об'єктів: {shape_count}/{MyEditor.MAX_SHAPES}"
        )
        
        tool_names = {
            'point': 'Точка',
            'line': 'Лінія',
            'rect': 'Прямокутник', 
            'ellipse': 'Еліпс',
            'line_oo': 'Лінія з кружечками',
            'cube': 'Куб'
        }
        current_tool_name = tool_names.get(self.current_tool, "Невідомо")
        self.root.title(f"{self.base_title} - [{current_tool_name}]")
    
    def show_about(self):
        messagebox.showinfo(
            "Про програму",
            "Програма для малювання геометричних фігур\n\n"
            "Автор: Хубеджева Єлизавета\n\n"
            "Підтримувані фігури:\n"
            "• Точка\n"
            "• Лінія\n"
            "• Прямокутник\n"
            "• Еліпс\n"
            "• Лінія з кружечками\n"
            "• Каркас кубу\n\n"
            "Максимальна кількість об'єктів: 128"
        )
    
    def run(self):
        self.root.mainloop()