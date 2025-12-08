import tkinter as tk
from tkinter import filedialog, messagebox
import os
from analysis import ProjectAnalyzer
from viewer import HierarchyViewer

class CppHierarchyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Візуалізатор #include-ієрархії C++")
        self.root.geometry("1000x800")
        
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_folder = tk.Button(toolbar, text="📂 Вибрати папку", command=self.open_folder_dialog)
        btn_folder.pack(side=tk.LEFT, padx=5, pady=2)
        
        btn_file = tk.Button(toolbar, text="📄 Вибрати файл", command=self.open_file_dialog)
        btn_file.pack(side=tk.LEFT, padx=5, pady=2)
        
        tk.Label(toolbar, text="  |  Масштаб: ").pack(side=tk.LEFT)
        
        tk.Button(toolbar, text=" + ", command=self.on_zoom_in).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text=" - ", command=self.on_zoom_out).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text=" 100% ", command=self.on_zoom_reset).pack(side=tk.LEFT, padx=2)
        
        self.analyzer = ProjectAnalyzer()
        self.viewer = HierarchyViewer(self.root)

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Відкрити папку проекту...", command=self.open_folder_dialog)
        file_menu.add_command(label="Відкрити головний файл...", command=self.open_file_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Збільшити (+)", command=self.on_zoom_in)
        view_menu.add_command(label="Зменшити (-)", command=self.on_zoom_out)
        view_menu.add_command(label="Скинути (100%)", command=self.on_zoom_reset)

        menubar.add_cascade(label="Файл", menu=file_menu)
        menubar.add_cascade(label="Вигляд", menu=view_menu)
        self.root.config(menu=menubar)
        
        self.root.bind("<Configure>", self.on_resize)

    def open_folder_dialog(self):
        folder_selected = filedialog.askdirectory(title="Виберіть папку проекту")
        if folder_selected:
            self.load_project(folder_selected)

    def open_file_dialog(self):
        file_selected = filedialog.askopenfilename(
            title="Виберіть головний файл проекту (.cpp, .h)",
            filetypes=[
                ("C++ Files", "*.cpp *.h *.c *.hpp *.rc"),
                ("All Files", "*.*")
            ]
        )
        if file_selected:
            self.load_project(file_selected)

    def load_project(self, path):
        if os.path.isfile(path):
            folder_path = os.path.dirname(path)
            display_name = f"File: {os.path.basename(path)}"
        else:
            folder_path = path
            display_name = "Folder Mode"
            
        self.root.title(f"Візуалізатор - {folder_path} ({display_name})")
        
        self.analyzer.scan_directory(path)
        
        levels, dependencies = self.analyzer.get_hierarchy_data()
        
        if not levels:
            messagebox.showinfo("Інфо", "Файлів проекту не знайдено або вони не мають залежностей.")
            return
        
        self.viewer.set_data(levels, dependencies)

    def on_zoom_in(self):
        self.viewer.zoom_in()

    def on_zoom_out(self):
        self.viewer.zoom_out()

    def on_zoom_reset(self):
        self.viewer.reset_zoom()

    def on_resize(self, event):
        if event.widget == self.root:
            self.viewer.redraw()

if __name__ == "__main__":
    root = tk.Tk()
    app = CppHierarchyApp(root)
    root.mainloop()