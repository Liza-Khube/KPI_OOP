from abc import ABC, abstractmethod

class Shape(ABC):
    
    def __init__(self, x1, y1, x2, y2, color="black", fill_color="pink", width=2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.fill_color = fill_color
        self.width = width
        self.canvas_id = None
    
    @abstractmethod
    def show(self, canvas):
        pass
    
    @abstractmethod
    def get_name(self):
        pass

class PointShape(Shape):
    def show(self, canvas):
        radius = 3
        self.canvas_id = canvas.create_oval(
            self.x1 - radius, self.y1 - radius,
            self.x1 + radius, self.y1 + radius,
            fill=self.color, outline=self.color
        )
    
    def get_name(self):
        return "Точка"


class LineShape(Shape):    
    def show(self, canvas):
        self.canvas_id = canvas.create_line(
            self.x1, self.y1, self.x2, self.y2,
            fill=self.color, width=self.width
        )
    
    def get_name(self):
        return "Лінія"


class RectShape(Shape):   
    def show(self, canvas):
        self.canvas_id = canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            fill=None, outline=self.color, width=self.width
        )
    
    def get_name(self):
        return "Прямокутник"


class EllipseShape(Shape):    
    def show(self, canvas):
        self.canvas_id = canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            fill=self.fill_color, outline=self.color, width=self.width
        )
    
    def get_name(self):
        return "Еліпс"