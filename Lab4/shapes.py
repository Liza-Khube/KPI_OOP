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
    def show(self, canvas, is_preview=False):
        pass
    
    def _get_style(self, is_preview, default_style):
        if is_preview:
            return {"outline": "black", "fill": None, "dash": (4, 2)}
        return default_style
    
    def _get_tags(self, is_preview):
        return "preview" if is_preview else "shape"


class PointShape(Shape):
    def show(self, canvas, is_preview=False):
        radius = 3
        
        style = self._get_style(is_preview, {
            "fill": self.color, 
            "outline": self.color
        })
        
        canvas.create_oval(
            self.x1 - radius, self.y1 - radius,
            self.x1 + radius, self.y1 + radius,
            **style,
            tags=self._get_tags(is_preview)
        )

class LineShape(Shape):
    def show(self, canvas, is_preview=False):
        style = self._get_style(is_preview, {
            "fill": self.color, 
            "width": self.width
        })

        if is_preview:
            if "outline" in style:
                style["fill"] = style.pop("outline")
            style["width"] = 1
        
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2,
            **style,
            tags=self._get_tags(is_preview)
        )

class RectShape(Shape):
    def show(self, canvas, is_preview=False):
        style = self._get_style(is_preview, {
            "fill": None, 
            "outline": self.color, 
            "width": self.width
        })
        
        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            **style,
            tags=self._get_tags(is_preview)
        )

class EllipseShape(Shape):
    def show(self, canvas, is_preview=False):
        style = self._get_style(is_preview, {
            "fill": "pink", 
            "outline": self.color, 
            "width": self.width
        })
        
        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            **style,
            tags=self._get_tags(is_preview)
        )

class LineOOShape(LineShape, EllipseShape):

    CIRCLE_RADIUS = 7

    def __init__(self, x1, y1, x2, y2):
        Shape.__init__(self, x1, y1, x2, y2)
        self.radius = self.CIRCLE_RADIUS
    
    def show(self, canvas, is_preview=False):
        LineShape.show(self, canvas, is_preview)
        orig_x1, orig_y1, orig_x2, orig_y2 = self.x1, self.y1, self.x2, self.y2
        
        self.x1, self.y1 = orig_x1 - self.radius, orig_y1 - self.radius
        self.x2, self.y2 = orig_x1 + self.radius, orig_y1 + self.radius
        EllipseShape.show(self, canvas, is_preview)
        
        self.x1, self.y1 = orig_x2 - self.radius, orig_y2 - self.radius
        self.x2, self.y2 = orig_x2 + self.radius, orig_y2 + self.radius
        EllipseShape.show(self, canvas, is_preview)
        
        self.x1, self.y1, self.x2, self.y2 = orig_x1, orig_y1, orig_x2, orig_y2

class CubeShape(RectShape, LineShape):

    PERSPECTIVE_RATIO = 0.4

    def __init__(self, x1, y1, x2, y2):
        Shape.__init__(self, x1, y1, x2, y2, color="purple")
    
    def show(self, canvas, is_preview=False):
        orig_x1, orig_y1 = self.x1, self.y1
        orig_x2, orig_y2 = self.x2, self.y2
        
        RectShape.show(self, canvas, is_preview)
        
        dx = (self.x2 - self.x1) * self.PERSPECTIVE_RATIO
        dy = (self.y2 - self.y1) * self.PERSPECTIVE_RATIO
        
        self.x1, self.y1 = orig_x1 + dx, orig_y1 - dy
        self.x2, self.y2 = orig_x2 + dx, orig_y2 - dy
        RectShape.show(self, canvas, is_preview)
        
        self.x1, self.y1 = orig_x1, orig_y1
        self.x2, self.y2 = orig_x1 + dx, orig_y1 - dy
        LineShape.show(self, canvas, is_preview)
        
        self.x1, self.y1 = orig_x2, orig_y1
        self.x2, self.y2 = orig_x2 + dx, orig_y1 - dy
        LineShape.show(self, canvas, is_preview)
        
        self.x1, self.y1 = orig_x1, orig_y2
        self.x2, self.y2 = orig_x1 + dx, orig_y2 - dy
        LineShape.show(self, canvas, is_preview)
        
        self.x1, self.y1 = orig_x2, orig_y2
        self.x2, self.y2 = orig_x2 + dx, orig_y2 - dy
        LineShape.show(self, canvas, is_preview)
        
        self.x1, self.y1 = orig_x1, orig_y1
        self.x2, self.y2 = orig_x2, orig_y2