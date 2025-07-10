import tkinter as tk
from gui.gui_utils import *
from utils import *

def launch_utility_functions_menu(main_window):
    
    main_window.title("Species Search Menu")
    frame = tk.Frame(main_window)
    frame.grid(row=0, column=0, sticky='nsew')

    main_window.rowconfigure(0, weight=1)
    main_window.columnconfigure(0, weight=1)

    home_menu = tk.Menu(main_window, tearoff=0)
    add_data_menu = tk.Menu(main_window, tearoff=0)
    manage_database_menu = tk.Menu(main_window, tearoff=0)
    from gui.HomePage import create_home_page
    home_menu.add_command(label="Home", command=lambda: create_home_page(main_window))
    add_data_menu.add_command(label = "Add Data from CSV", command = lambda: add_data_from_csv(main_window))
    add_data_menu.add_command(label = "Add DNA Sequences from GenBank", command = lambda: add_dna_sequences_from_genbank(main_window))
    manage_database_menu.add_command(label = "Import Database", command = lambda: import_database(main_window))
    manage_database_menu.add_command(label = "Export Database", command = lambda: export_database(main_window))

    main_menu = build_base_menu(main_window)
    main_menu.add_cascade(label="Home", menu=home_menu)
    main_menu.add_cascade(label="Add Data from CSV/Genbank", menu=add_data_menu)
    main_menu.add_cascade(label="Import/Export Database", menu=manage_database_menu)
    main_window.config(menu=main_menu)

    rows = 11
    columns = 9
    for i in range(rows):
        frame.rowconfigure(i, weight=1)
    for j in range(columns):
        frame.columnconfigure(j, weight=1)

    heading = tk.Label(frame,
                       text = "Utility Functions",
                       font = ("Arial", 24, "bold"),
                       bg = 'black',
                       fg = 'white',
                       relief = 'raised',
                       bd = 10,
                       padx = 20,
                       pady = 20)
    heading.grid(row=0, column=1, columnspan=7, pady=10)

    instructions = tk.Label(frame,
                            text =  "This page contains utility functions to help with data extraction and management.\n\n" \
                                    "1. Add Data from CSV: Extracts data from a CSV file and adds it to the database.\n" \
                                    "2. Add DNA Sequences from GenBank: Extracts DNA sequences from a GenBank accession ID,\n adding both the sequence and the species to the database\n" \
                                    "3. Import Database: Imports a database from a file, allowing you to work with existing data.\n" \
                                    "4. Export Database: Exports the database to a file, enabling you to save your work.\n\n" \
                                    
                                    "Please note, extracting data from a CSV file requires the CSV to be formatted correctly.\n" \
                                    "The CSV should contain columns with headers that match the database structure.\n For the tables, mutations, species and DNA Sequences, this is given below\n"\
                                    "This function acts the same way as the 'Add' functions in the other menus, so note you\n may recieve errors if you try to add mutations/dna sequences for species not in the database.\n" \
                                    "Additionally, importing data from GenBank may occasionally leave 'gaps' in the data,\n this can be because the GenBank link does not contain all pertinent information, please double check.\n\n"\
                                     
                                    "Database structure:\n\n"
                                    "Brackets indicate what sort of values should be in the column\n" \
                                    "Species: Class, Scientific Name, Common Name, Domesticated (yes/no)\n"\
                                    "Mutations: Scientific Name, Gene, Nucleotide Change, Amino Acid Change, CpG Associated (yes/no), Gain of Function (yes/no), URL\n"\
                                    "DNA Sequences: Scientific Name, Gene, DNA Sequence, Splice Site (check DNA Sequences tab for format description)",
                                    
                            font = ("Arial", 12),
                            justify='center')
                            
    instructions.grid(row=1, column=1, columnspan=7, pady=10)