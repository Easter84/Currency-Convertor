"""
This module is the main file for the application and is used to launch it.
Created by Timothy Easter
"""
from models import ExchangeForm
import tkinter as tk


def main():
    """
    This is the function that starts the GUI loop and triggers the program to start.
    :return:
    """
    root = tk.Tk()
    app = ExchangeForm(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()
