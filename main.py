from gui.HomePage import create_home_page
from gui.gui_utils import set_connection
from utils import get_db_path
import tkinter as tk
import sqlite3

def main():

    set_connection(sqlite3.connect(get_db_path()))

    window = tk.Tk()
    create_home_page(window)
    window.mainloop()

if __name__ == "__main__":
    main()