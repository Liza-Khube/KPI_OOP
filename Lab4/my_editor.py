import tkinter as tk
from tkinter import messagebox
from shapes import Shape, PointShape, LineShape, RectShape, EllipseShape, LineOOShape, CubeShape

class MyEditor:
    MAX_SHAPES = 126
    
    def __init__(self, canvas, status_update_callback):
        self.canvas = canvas
        self.status_update_callback = status_update_callback
        
        self.shapes = None 
        self.shape_count = 0
        
        self.current_tool = 'point'
        self.is_drawing = False
        self.start_x = 0
        self.start_y = 0
        
        self.temp_shape = None

    def _ensure_array_exists(self):
        if self.shapes is None:
            self.shapes = [None] * self.MAX_SHAPES

    def __del__(self):
        del self.shapes

    def select_tool(self, tool):
        self.current_tool = tool

    def on_mouse_down(self, event):
        self._ensure_array_exists() 
        
        if self.shape_count >= self.MAX_SHAPES:
            messagebox.showwarning("Увага", "Досягнуто максимальну кількість об'єктів (126)")
            return
            
        self.is_drawing = True
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_move(self, event):
        if not self.is_drawing:
            return
            
        self.canvas.delete("preview")
        self.temp_shape = self._create_shape_instance(event)
        
        if self.temp_shape:
            self.temp_shape.show(self.canvas, is_preview=True)

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
            self.shapes[self.shape_count] = shape
            self.shape_count += 1
            shape.show(self.canvas)
            self.status_update_callback()
        
    def get_shape_count(self):
        if self.shapes is None:
            return 0
        return self.shape_count

    def clear(self):
        self.canvas.delete("shape")
        self.shapes = None 
        self.shape_count = 0
        self.status_update_callback()