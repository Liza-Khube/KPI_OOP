import tkinter as tk
from app import DrawingApp


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    app.run()


if __name__ == "__main__":
    main()