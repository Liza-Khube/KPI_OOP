import tkinter as tk

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self._show_tip)
        self.widget.bind("<Leave>", self._hide_tip)

    def _show_tip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip_window, text=self.text, justify='left',
            background="#ffffe0", relief='solid', borderwidth=1,
        )
        label.pack(ipadx=1)

    def _hide_tip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

class Toolbar:
    def __init__(self, root, select_tool_callback):
        self.frame = tk.Frame(root, bd=1, relief=tk.RAISED)
        self.select_tool_callback = select_tool_callback
        self.button_images = {}
        self.buttons = {}

        buttons_data = {
            'point': ("./icons/point.png", "Створити точку"),
            'line': ("./icons/line.png", "Намалювати лінію"),
            'rect': ("./icons/rect.png", "Намалювати прямокутник"),
            'ellipse': ("./icons/ellipse.png", "Намалювати еліпс"),
            'line_oo': ("./icons/line_oo.png", "Намалювати лінію з кружечками"),
            'cube': ("./icons/cube.png", "Намалювати каркас кубу"),
        }

        img_scale = 22

        for tool, (img_file, tooltip_text) in buttons_data.items():
            try:
                original_img = tk.PhotoImage(file=img_file)
                resized_img = original_img.subsample(img_scale, img_scale)
                self.button_images[tool] = resized_img
                
                button = tk.Button(
                    self.frame,
                    image=resized_img,
                    command=lambda t=tool: self.select_tool_callback(t),
                    relief=tk.RAISED
                )
                button.pack(side=tk.LEFT, padx=2, pady=2)
                Tooltip(button, tooltip_text)
                self.buttons[tool] = button
            except tk.TclError:
                print(f"Помилка: Файл зображення '{img_file}' не знайдено.")

        self.frame.pack(side=tk.TOP, fill=tk.X)
    
    def set_active_tool(self, active_tool):
        for tool, button in self.buttons.items():
            if tool == active_tool:
                button.config(relief=tk.SUNKEN)
            else:
                button.config(relief=tk.RAISED)