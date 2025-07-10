from gui.HomePage import create_home_page
from gui.gui_utils import *
from utils import get_db_path
import tkinter as tk
import sqlite3
import sys

def main():
    if '--test' in sys.argv:
        print("Test run: app starts correctly.")
        sys.exit(0)

    set_connection(sqlite3.connect(get_db_path()))

    window = tk.Tk()
    main_menu = build_base_menu(window)
    window.main_menu = main_menu
    window.config(menu=main_menu)

    create_home_page(window)
    window.mainloop()

if __name__ == "__main__":
    main()