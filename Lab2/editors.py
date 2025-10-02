import tkinter as tk
from abc import ABC, abstractmethod
from shapes import Shape, PointShape, LineShape, RectShape, EllipseShape

class Editor(ABC):
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.start_x = 0
        self.start_y = 0
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
    
    def on_mouse_down(self, event) -> None:
        self.start_x = event.x
        self.start_y = event.y
        self.is_drawing = True
    
    def on_mouse_move(self, event) -> None:
        if self.is_drawing:
            if self.temp_id:
                self.canvas.delete(self.temp_id)
            self.temp_id = self.create_preview(event)
    
    def on_mouse_up(self, event) -> Shape:
        if self.is_drawing:
            if self.temp_id:
                self.canvas.delete(self.temp_id)
                self.temp_id = None
            self.is_drawing = False
            return self.create_shape(event)
        return None
    
    def create_preview(self, event):
        return None
    
    @abstractmethod
    def create_shape(self, event) -> Shape:
        pass


class PointEditor(ShapeEditor):    
    def create_shape(self, event) -> Shape:
        return PointShape(self.start_x, self.start_y, self.start_x, self.start_y)


class LineEditor(ShapeEditor):    
    def create_preview(self, event):
        return self.canvas.create_line(
            self.start_x, self.start_y, event.x, event.y,
            fill="black"
        )
    
    def create_shape(self, event) -> Shape:
        return LineShape(self.start_x, self.start_y, event.x, event.y)


class RectEditor(ShapeEditor):    
    def create_preview(self, event):
        return self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            fill=None, outline="black"
        )
    
    def create_shape(self, event) -> Shape:
        return RectShape(self.start_x, self.start_y, event.x, event.y)


class EllipseEditor(ShapeEditor):
    def create_preview(self, event):
        x1, y1, x2, y2 = self.calculate_bounds(event)
        return self.canvas.create_oval(
            x1, y1, x2, y2,
            fill="pink", outline="black"
        )
    
    def create_shape(self, event) -> Shape:
        x1, y1, x2, y2 = self.calculate_bounds(event)
        return EllipseShape(x1, y1, x2, y2)
    
    def calculate_bounds(self, event):
        dx = abs(event.x - self.start_x)
        dy = abs(event.y - self.start_y)
        
        x1 = self.start_x - dx
        y1 = self.start_y - dy
        x2 = self.start_x + dx
        y2 = self.start_y + dy
        
        return x1, y1, x2, y2