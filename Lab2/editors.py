import tkinter as tk
from abc import ABC, abstractmethod
from shapes import Shape, PointShape, LineShape, RectShape, EllipseShape

class Editor(ABC):
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.start_x = 0
        self.start_y = 0
        self.current_shape = None
        self.is_drawing = False
    
    @abstractmethod
    def on_mouse_down(self, event):
        pass
    
    @abstractmethod
    def on_mouse_move(self, event):
        pass
    
    @abstractmethod
    def on_mouse_up(self, event):
        pass

class ShapeEditor(Editor):    
    def __init__(self, canvas: tk.Canvas):
        super().__init__(canvas)
        self.temp_id = None


class PointEditor(ShapeEditor):    
    def __init__(self, canvas: tk.Canvas):
        super().__init__(canvas, PointShape)
    
    def on_mouse_down(self, event) -> None:
        self.start_x = event.x
        self.start_y = event.y
        self.is_drawing = True
    
    def on_mouse_move(self, event) -> None:
        pass
    
    def on_mouse_up(self, event) -> Shape:
        if self.is_drawing:
            self.is_drawing = False
            return PointShape(self.start_x, self.start_y, self.start_x, self.start_y)
        return None


class LineEditor(ShapeEditor):    
    def __init__(self, canvas: tk.Canvas):
        super().__init__(canvas, LineShape)
    
    def on_mouse_down(self, event) -> None:
        self.start_x = event.x
        self.start_y = event.y
        self.is_drawing = True
    
    def on_mouse_move(self, event) -> None:
        if self.is_drawing:
            if self.temp_id:
                self.canvas.delete(self.temp_id)
            self.temp_id = self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill="black"
            )
    
    def on_mouse_up(self, event) -> Shape:
        if self.is_drawing:
            if self.temp_id:
                self.canvas.delete(self.temp_id)
                self.temp_id = None
            self.is_drawing = False
            return LineShape(self.start_x, self.start_y, event.x, event.y)
        return None


class RectEditor(ShapeEditor):    
    def __init__(self, canvas: tk.Canvas):
        super().__init__(canvas, RectShape)
    
    def on_mouse_down(self, event) -> None:
        self.start_x = event.x
        self.start_y = event.y
        self.is_drawing = True
    
    def on_mouse_move(self, event) -> None:
        if self.is_drawing:
            if self.temp_id:
                self.canvas.delete(self.temp_id)
            self.temp_id = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline="black"
            )
    
    def on_mouse_up(self, event) -> Shape:
        if self.is_drawing:
            if self.temp_id:
                self.canvas.delete(self.temp_id)
                self.temp_id = None
            self.is_drawing = False
            return RectShape(self.start_x, self.start_y, event.x, event.y)
        return None


class EllipseEditor(ShapeEditor):
    def __init__(self, canvas):
        super().__init__(canvas, EllipseShape)
    
    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.is_drawing = True
    
    def on_mouse_move(self, event):
        if self.is_drawing:
            if self.temp_id:
                self.canvas.delete(self.temp_id)
            
            dx = abs(event.x - self.start_x)
            dy = abs(event.y - self.start_y)
            
            x1 = self.start_x - dx
            y1 = self.start_y - dy
            x2 = self.start_x + dx
            y2 = self.start_y + dy
            
            self.temp_id = self.canvas.create_oval(
                x1, y1, x2, y2,
                outline="black"
            )
    
    def on_mouse_up(self, event):
        if self.is_drawing:
            if self.temp_id:
                self.canvas.delete(self.temp_id)
                self.temp_id = None
            self.is_drawing = False
            
            dx = abs(event.x - self.start_x)
            dy = abs(event.y - self.start_y)
            
            x1 = self.start_x - dx
            y1 = self.start_y - dy
            x2 = self.start_x + dx
            y2 = self.start_y + dy
            
            return EllipseShape(x1, y1, x2, y2)
        return None