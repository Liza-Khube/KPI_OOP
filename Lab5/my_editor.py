import tkinter as tk
from tkinter import messagebox
from shapes import Shape, PointShape, LineShape, RectShape, EllipseShape, LineOOShape, CubeShape

class MyEditor:

    MAX_SHAPES = 126
    LOG_FILE = "shapes_log.txt"

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MyEditor, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, canvas=None, status_update_callback=None, shape_add_callback=None):
        if self._initialized:
            return

        self.canvas = canvas
        self.status_update_callback = status_update_callback
        self.shape_add_callback = shape_add_callback 
        
        self.shapes = None 
        self.shape_count = 0
        
        self.current_tool = 'point'
        self.is_drawing = False
        self.start_x = 0
        self.start_y = 0
        
        self.temp_shape = None
        self.highlighted_index = None

        self._initialized = True
        
        self._clear_log_file()

    def _ensure_array_exists(self):
        if self.shapes is None:
            self.shapes = [None] * self.MAX_SHAPES

    def select_tool(self, tool):
        self.current_tool = tool
        self.unhighlight_all()

    def on_mouse_down(self, event):
        self._ensure_array_exists() 
        
        if self.shape_count >= self.MAX_SHAPES:
            messagebox.showwarning("Увага", "Досягнуто максимальну кількість об'єктів (126)")
            return
            
        self.unhighlight_all()    
        self.is_drawing = True
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_move(self, event):
        if not self.is_drawing:
            return
            
        self.canvas.delete("preview")
        self.temp_shape = self._create_shape_instance(event)
        
        if self.temp_shape:
            self.temp_shape.show(self.canvas, is_preview=True, is_highlighted=False)

    def on_mouse_up(self, event):
        if not self.is_drawing:
            return
            
        self.is_drawing = False
        self.canvas.delete("preview")
        
        final_shape = self._create_shape_instance(event)
        
        if final_shape:
            self.add_shape(final_shape)
            
        self.temp_shape = None

    def _create_shape_instance(self, event):
        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y

        if self.current_tool == 'point':
            return PointShape(x1, y1, x1, y1)
        elif self.current_tool == 'line':
            return LineShape(x1, y1, x2, y2)
        elif self.current_tool == 'rect':
            return RectShape(x1, y1, x2, y2)
        elif self.current_tool == 'ellipse':
            return EllipseShape(x1, y1, x2, y2)
        elif self.current_tool == 'line_oo':
            return LineOOShape(x1, y1, x2, y2)
        elif self.current_tool == 'cube':
            return CubeShape(x1, y1, x2, y2)
        return None

    def add_shape(self, shape):
        self._ensure_array_exists() 
        
        if self.shape_count < self.MAX_SHAPES:
            self.highlighted_index = None
            self.shapes[self.shape_count] = shape
            self.shape_count += 1
            shape.show(self.canvas, is_preview=False, is_highlighted=False)
            
            self.status_update_callback()
            self._log_shape_to_file(shape)
            self.shape_add_callback(shape)
            
    def _log_shape_to_file(self, shape):

        shape_name = shape.__class__.__name__
        
        try:
            with open(self.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"{shape_name}\t{shape.x1}\t{shape.y1}\t{shape.x2}\t{shape.y2}\n")
        except IOError as e:
            print(f"Помилка запису у файл '{self.LOG_FILE}': {e}")

    def _clear_log_file(self):
        try:
            with open(self.LOG_FILE, "w", encoding="utf-8") as f:
                f.write("")
        except IOError as e:
            print(f"Помилка очищення файлу '{self.LOG_FILE}': {e}")

    def get_shape_count(self):
        if self.shapes is None:
            return 0
        return self.shape_count

    def clear(self):
        self.canvas.delete("shape")
        self.highlighted_index = None
        self.shapes = None 
        self.shape_count = 0
        

        self.status_update_callback()
        self._clear_log_file()
        self.shape_add_callback(None)

    def redraw_all_shapes(self):
        self.canvas.delete("shape")
        if self.shapes is None:
            return
            
        for i in range(self.shape_count):
            is_highlighted = (i == self.highlighted_index)
            self.shapes[i].show(self.canvas, is_preview=False, is_highlighted=is_highlighted)

    def highlight_shape_at(self, index):
        if not (0 <= index < self.shape_count):
            return
            
        if self.highlighted_index == index:
            return
            
        self.highlighted_index = index
        self.redraw_all_shapes()

    def unhighlight_all(self):
        if self.highlighted_index is None:
            return
            
        self.highlighted_index = None
        self.redraw_all_shapes()

    def delete_shape_at(self, index):
        if not (0 <= index < self.shape_count):
            return

        for i in range(index, self.shape_count - 1):
            self.shapes[i] = self.shapes[i+1]
        
        self.shapes[self.shape_count - 1] = None
        self.shape_count -= 1   
        self.highlighted_index = None
        self.redraw_all_shapes()
        self.status_update_callback()
        self._regenerate_log_file()
        self.shape_add_callback(None)

    def _regenerate_log_file(self):
        self._clear_log_file()
        if self.shapes is None:
            return
        for i in range(self.shape_count):
            self._log_shape_to_file(self.shapes[i])