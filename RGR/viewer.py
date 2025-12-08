import tkinter as tk
from tkinter import ttk

class HierarchyViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self, bg="white")
        self.v_scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.h_scroll = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.BASE_BOX_WIDTH = 220
        self.BASE_BOX_HEIGHT = 100
        self.BASE_H_GAP = 100
        self.BASE_V_GAP = 150
        
        self.scale_factor = 1.0
        
        self.current_levels = None
        self.current_deps = None
        
        self.node_info = {}

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_linux_scroll_up)
        self.canvas.bind_all("<Button-5>", self._on_linux_scroll_down)

    def set_data(self, levels_data, dependencies):
        self.current_levels = levels_data
        self.current_deps = dependencies
        self.redraw()

    def zoom_in(self):
        self.scale_factor += 0.1
        self.redraw()

    def zoom_out(self):
        if self.scale_factor > 0.2:
            self.scale_factor -= 0.1
            self.redraw()

    def reset_zoom(self):
        self.scale_factor = 1.0
        self.redraw()

    def redraw(self):
        if self.current_levels and self.current_deps:
            self._draw_scene_scaled()

    def _draw_scene_scaled(self):
        self.canvas.delete("all")
        self.node_info = {}
        
        box_w = self.BASE_BOX_WIDTH * self.scale_factor
        box_h = self.BASE_BOX_HEIGHT * self.scale_factor
        h_gap = self.BASE_H_GAP * self.scale_factor
        v_gap = self.BASE_V_GAP * self.scale_factor
        
        font_title_size = int(9 * self.scale_factor)
        font_content_size = int(8 * self.scale_factor)
        font_arrow_size = int(7 * self.scale_factor)
        
        if font_title_size < 4: font_title_size = 4
        if font_content_size < 3: font_content_size = 3
        
        sorted_levels = sorted(self.current_levels.keys())
        max_width = 0
        current_y = 50 * self.scale_factor

        for level in sorted_levels:
            files = self.current_levels[level]
            total_level_width = len(files) * (box_w + h_gap) - h_gap
            
            canvas_w = self.winfo_width()
            start_x = max(50, (canvas_w - total_level_width) // 2)
            if start_x < 50: start_x = 50
            
            current_x = start_x
            
            for filename in files:
                self.node_info[filename] = {
                    'x': current_x,
                    'y': current_y,
                    'w': box_w,
                    'h': box_h
                }
                current_x += box_w + h_gap
                if current_x > max_width: max_width = current_x
            
            current_y += box_h + v_gap

        shadow_offset = 4 * self.scale_factor
        for filename, coords in self.node_info.items():
            x, y, w, h = coords['x'], coords['y'], coords['w'], coords['h']
            self.canvas.create_rectangle(
                x + shadow_offset, y + shadow_offset, 
                x + w + shadow_offset, y + h + shadow_offset, 
                fill="#C0C0C0", outline=""
            )

        parents_of = {f: [] for f in self.node_info}
        children_of = {f: [] for f in self.node_info}

        for parent, includes in self.current_deps.items():
            if parent not in self.node_info: continue
            for child in includes:
                if child in self.node_info:
                    parents_of[child].append(parent)
                    children_of[parent].append(child)

        for f in self.node_info:
            parents_of[f].sort(key=lambda p: self.node_info[p]['x'])
            children_of[f].sort(key=lambda c: self.node_info[c]['x'])

        for child, parents in parents_of.items():
            if not parents: continue
            child_info = self.node_info[child]
            step_out = child_info['w'] / (len(parents) + 1)
            
            for i, parent in enumerate(parents):
                parent_info = self.node_info[parent]
                try:
                    child_index = children_of[parent].index(child)
                    total_children = len(children_of[parent])
                except ValueError: continue

                step_in = parent_info['w'] / (total_children + 1)

                start_x = child_info['x'] + step_out * (i + 1)
                start_y = child_info['y']
                end_x = parent_info['x'] + step_in * (child_index + 1)
                end_y = parent_info['y'] + parent_info['h']

                self.canvas.create_line(
                    start_x, start_y, end_x, end_y,
                    arrow=tk.LAST, fill="#444444", width=1.5 * self.scale_factor
                )
                
                ratio = 0.40 if (i % 2 == 0) else 0.60
                text_x = start_x + (end_x - start_x) * ratio
                text_y = start_y + (end_y - start_y) * ratio
                
                text_w = 45 * self.scale_factor
                text_h = 14 * self.scale_factor
                
                self.canvas.create_rectangle(
                    text_x - text_w/2, text_y - text_h/2,
                    text_x + text_w/2, text_y + text_h/2,
                    fill="white", outline=""
                )
                self.canvas.create_text(
                    text_x, text_y, text="#include", 
                    fill="#0000AA", font=("Arial", font_arrow_size, "italic")
                )

        for filename, coords in self.node_info.items():
            self._draw_node_body(coords, filename, self.current_deps.get(filename, []), font_title_size, font_content_size)

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _draw_node_body(self, coords, title, includes, f_title, f_content):
        x, y, w, h = coords['x'], coords['y'], coords['w'], coords['h']
        
        bg_color = "#E0FFFF" if title.endswith('.h') else "#FFFFE0" 
        if title.endswith('.rc'): bg_color = "#E0E0E0"

        self.canvas.create_rectangle(x, y, x+w, y+h, fill=bg_color, outline="black")
        
        header_h = 25 * self.scale_factor
        self.canvas.create_line(x, y + header_h, x + w, y + header_h, fill="black")
        self.canvas.create_text(x + w/2, y + header_h/2, text=title, font=("Arial", f_title, "bold"))
        
        content_text = ""
        if includes:
            for inc in includes[:5]:
                content_text += f"#include \"{inc}\"\n"
            if len(includes) > 5:
                content_text += "..."
        else:
            content_text = "(base)"
            
        self.canvas.create_text(x + 5*self.scale_factor, y + header_h + 5*self.scale_factor, 
                                text=content_text, anchor="nw", font=("Consolas", f_content), fill="#555555")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_shift_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
    def _on_linux_scroll_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def _on_linux_scroll_down(self, event):
        self.canvas.yview_scroll(1, "units")