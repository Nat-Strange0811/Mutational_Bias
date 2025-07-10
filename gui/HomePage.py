import tkinter as tk
from gui.gui_utils import clear_window

from gui.search_menu_options import species_menu, mutations_menu, dna_sequences_menu
from gui import results_menu
from gui import analysis_menu
from gui import utils_menu



def create_home_page(main_window):
    '''Clears the main window and sets up the home page with buttons for different functionalities.'''

    #Clear the main window using the utility function
    clear_window(main_window)
    main_window.unbind("<Button-3>")

    # Set up the main window
    main_window.title("Home Page")
    main_window.geometry("1000x700")
    main_window.configure(background="#e7e7e7")
    
    search_menu = tk.Menu(main_window,tearoff=0)
    analysis_menu = tk.Menu(main_window, tearoff=0)
    utils_menu = tk.Menu(main_window, tearoff=0)

    search_menu.add_command(label = "Species", command = lambda: create_search_menu(main_window, "Species"))
    search_menu.add_command(label = "Mutations", command = lambda: create_search_menu(main_window, "Mutations"))
    search_menu.add_command(label = "DNA Sequences", command = lambda: create_search_menu(main_window, "DNA Sequences"))
    analysis_menu.add_command(label = "Results", command = lambda: create_search_menu(main_window, "Results"))
    analysis_menu.add_command(label = "Analysis", command = lambda: create_search_menu(main_window, "Analysis"))
    utils_menu.add_command(label = "Utility Functions", command = lambda: create_search_menu(main_window, "Utility Functions"))  

    # Create a heading label
    heading = tk.Label(main_window,
                       text = "Main Menu",
                       font = ("Arial", 24, "bold"),
                       bg = 'black',
                       fg = 'white',
                       relief = 'raised',
                       bd = 10,
                       padx = 20,
                       pady = 20)
    heading.pack()

    description = tk.Label(main_window,
                            text = "Welcome to the Mutational Bias Analysis Tool!\n\n"
                                     '''Use the menu above to navigate through the application.\n'''
                                     '''Search for details on species, mutations, DNA sequences, and results.\n'''
                                     '''You can also add, delete, or edit entries as needed.\n'''
                                     '''To run analysis, or produce a report, select the analysis menu.\n'''
                                     '''Utility functions, designed to help with data extraction are also available.\n''',
                            font = ("Arial", 14),
                            bg = '#e7e7e7',
                            fg = 'black',
                            padx = 20,
                            pady = 20)
    description.pack()


    main_menu = tk.Menu(main_window)
    main_menu.add_cascade(label = "Search/Edit Database", menu = search_menu)
    main_menu.add_cascade(label = "Run Analysis", menu = analysis_menu)
    main_menu.add_cascade(label = "Utility Functions", menu = utils_menu)
    main_window.config(menu=main_menu)
    
def create_search_menu(main_window, table_name):
    """
    Creates the search menu for the main window.
    
    Args:
        main_window (tk.Tk): The main application window.
        table_name (str): The name of the table to search in.
    """
    menu_lookup = {
        "Species": species_menu.launch_species_menu,
        "Mutations": mutations_menu.launch_mutations_menu,
        "DNA Sequences": dna_sequences_menu.launch_dna_sequences_menu,
        "Results": results_menu.launch_results_menu,
        "Analysis": analysis_menu.launch_analysis_menu,
        "Utility Functions" : utils_menu.launch_utility_functions_menu
    }

    clear_window(main_window)

    menu_lookup[table_name](main_window)
    