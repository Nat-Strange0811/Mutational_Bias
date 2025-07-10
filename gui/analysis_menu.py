import tkinter as tk
from gui.gui_utils import *
from utils import *

def launch_analysis_menu(main_window):
    home_menu = tk.Menu(main_window, tearoff=0)


    from gui.HomePage import create_home_page
    home_menu.add_command(label="Home", command=lambda: create_home_page(main_window))

    main_menu = tk.Menu(main_window)
    main_menu.add_cascade(label="Home", menu=home_menu)
    main_window.config(menu=main_menu)