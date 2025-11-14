import tkinter as tk
from tkinter import messagebox
from toolbar import Toolbar 
from my_editor import MyEditor
from my_table import MyTable

class DrawingApp:

    def __init__(self, root):
        self.root = root
        self.base_title = "Лабораторна робота 5. Хубеджева Єлизавета"
        self.root.title(self.base_title)
        self.root.geometry("950x600")

        self.current_tool = 'point'
        
        self.table_window = None

        self.create_menu()
        self.create_toolbar() 
        self.create_canvas()
        
        self.my_editor = MyEditor(
            self.canvas, 
            self.update_status,
            self.on_shape_update
        )
        
        self.create_status_bar()
        
        self.select_tool('point')
     
        self.canvas.bind("<Button-1>", self.my_editor.on_mouse_down) 
        self.canvas.bind("<B1-Motion>", self.my_editor.on_mouse_move) 
        self.canvas.bind("<ButtonRelease-1>", self.my_editor.on_mouse_up) 

        self.root.protocol("WM_DELETE_WINDOW", self.on_program_exit)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar) 
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Очистити", command=self.clear_canvas) 
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.on_program_exit)

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
     
        table_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Таблиця", menu=table_menu)
        table_menu.add_command(label="Показати / Сховати", command=self.toggle_table_window)
        
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
        self.my_editor.unhighlight_all()

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
            "Максимальна кількість об'єктів: 126"
        )
    

    def _get_table_window(self):
        if self.table_window is None or not self.table_window.window.winfo_exists():
            self.table_window = MyTable(
                self.root,
                on_row_select_callback=self.on_table_row_select,
                on_row_double_click_callback=self.on_table_row_double_click
            )
            
            self.on_shape_update(None)
        return self.table_window

    def toggle_table_window(self):
        table = self._get_table_window()
        if table.window.winfo_viewable():
            table.hide()
            self.my_editor.unhighlight_all()
        else:
            table.show()

    def on_shape_update(self, shape):
        if self.table_window is None or not self.table_window.window.winfo_exists():
            return

        if shape:
            self.table_window.add_row(
                shape.__class__.__name__, 
                shape.x1, shape.y1, shape.x2, shape.y2
            )
        else:
            self.table_window.clear_table()
            if self.my_editor.shapes:
                for i in range(self.my_editor.shape_count):
                    s = self.my_editor.shapes[i]
                    self.table_window.add_row(
                        s.__class__.__name__, 
                        s.x1, s.y1, s.x2, s.y2
                    )

    def on_table_row_select(self, index):
        self.my_editor.highlight_shape_at(index)

    def on_table_row_double_click(self, index):
        if messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити цей об'єкт?"):
            self.my_editor.delete_shape_at(index)

    def on_program_exit(self):
        if self.table_window and self.table_window.window.winfo_exists():
            self.table_window.destroy_window()
        self.root.quit()

    def run(self):
        self.root.mainloop()