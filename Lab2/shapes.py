from abc import ABC, abstractmethod

class Shape(ABC):
    
    def __init__(self, x1, y1, x2, y2, color="black", width=2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.width = width
    
    @abstractmethod
    def show(self, canvas):
        pass

class PointShape(Shape): 
    def show(self, canvas):
        radius = 3
        canvas.create_oval(
            self.x1 - radius, self.y1 - radius,
            self.x1 + radius, self.y1 + radius,
            fill=self.color, outline=self.color
        )


class LineShape(Shape):    
    def show(self, canvas):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2,
            fill=self.color, width=self.width
        )

class RectShape(Shape):   
    def show(self, canvas):
        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            fill=None, outline=self.color, width=self.width
        )

class EllipseShape(Shape):    
    def show(self, canvas):
        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            fill="pink", outline=self.color, width=self.width
        )