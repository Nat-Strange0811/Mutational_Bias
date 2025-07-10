import tkinter as tk
from gui.gui_utils import *
from tkinter import messagebox
import re


def add_entry(main_window, table_name):
    """
    Placeholder function for adding an entry to the specified table.
    
    Args:
        main_window (tk.Tk): The main application window.
        table_name (str): The name of the table to add an entry to.
    """
    def insert_row(heading=False, row_count=0):
        headings = column_lookup_entry[table_name]
        rows = []

        for col, heading_text in enumerate(headings):
            if heading:
                widget = tk.Label(frame, text=heading_text, font=("Arial", 14, "bold"), width=30, anchor="w")
            else:
                widget = tk.Entry(frame, width=30, font=("Arial", 14))
                rows.append(widget)
            widget.grid(row=row_count, column=col, sticky="ew", padx=2, pady=2)
            frame.grid_columnconfigure(col, weight=1)

        return rows, row_count + 1
    
    def on_canvas_resize(event):
        canvas.itemconfig("inner_frame", width=event.width)

    def add_cancel():
        from gui.search_menu_options import species_menu, mutations_menu, dna_sequences_menu
        menu_lookup = {
            "Species" : species_menu.launch_species_menu,
            "Mutations" : mutations_menu.launch_mutations_menu,
            "DNA_Sequences" : dna_sequences_menu.launch_dna_sequences_menu
        }
        clear_window(add_window)
        menu_lookup[table_name](add_window)

    def add_clear():
        clear_window(add_window)
        add_entry(add_window, table_name)

    def add_save():

        column_lookup = {
            "Species": ["Class", "Scientific_Name", "Common_Name", "Domesticated"],
            "Mutations": ["Species_ID", "DNA_Sequence_ID","Gene", "Nucleotide_Change", "Amino_Acid_Change", "CpG_Associated", "Gain_of_Function", "URL"],
            "DNA_Sequences": ["Species_ID", "Gene", "DNA_Sequence", "Splice_Site"]
            }
        
        for j, row in enumerate(rows):
            entry_data = conditions_check(j, row, table_name)

            query = f'''INSERT INTO
                            {table_name}
                            ({', '.join(column_lookup[table_name])})
                        VALUES
                            ({', '.join(['?'] * len(column_lookup[table_name]))})'''
            
            
            
            if entry_data == None:
                continue
            elif type(entry_data) != str:
                error = add_row(query, entry_data)
                if table_name == "DNA_Sequences":
                    check_mutations(entry_data[0], entry_data[1])
                for widget in row:
                    widget.delete(0, tk.END)
                if error:
                    messagebox.showerror("Error", f"An error occurred while adding the entry: {error}, please contact Nat")
            else:
                messagebox.showerror("Error", entry_data)

        


    def configure_window(add_window):
        
        clear_window(add_window)
        #configure window
        add_window.title(f"Add Entry to {table_name}")
        add_window.geometry("800x600")

        #add title label and description label
        heading = tk.Label(add_window,
                        text = "Add Entry to " + table_name,
                        font = ("Arial", 24, "bold"),
                        bg = 'black',
                        fg = 'white',
                        relief = 'raised',
                        bd = 10,
                        padx = 20,
                        pady = 20)
        heading.pack(pady=10)

        if table_name == "DNA_Sequences":
            instructions_text = "Please input splice site information as (including both () and []): \n\n([location one, location two], [location three, location four]etc.) or leave blank"
        else:
            instructions_text = ""

        instructions = tk.Label(add_window,
                                text = "Please fill in the details below to add a new entry.\n"
                                        "Once you have filled in the details, click 'Save' to add the entry(ies).\n"
                                        "To cancel and return to the previous menu, click 'Back'.\n" \
                                        "Please note, all fields are required unless specified.\n\n" + instructions_text,
                                font = ("Arial", 12),
                                justify='left')
        instructions.pack(pady=10)


        #add menu items
        add_menu = tk.Menu(add_window, tearoff=0)
        add_menu.add_command(label="Save", command=lambda: add_save())
        add_menu.add_command(label="Clear", command=lambda: add_clear())
        add_menu.add_command(label="Back", command=lambda: add_cancel())

        main_menu = tk.Menu(add_window)
        main_menu.add_cascade(label="Options", menu=add_menu)
        add_window.config(menu=main_menu)

        #create structure to add entires, we create a tale like structure, using canvas, frame, scrollbar and entry widgets, enabling retrieval
        #of input data.
        canvas = tk.Canvas(add_window)
        frame = tk.Frame(canvas)
        scrollbar = tk.Scrollbar(add_window, orient="vertical", command=canvas.yview)

        canvas.create_window((0, 0), window=frame, anchor="nw", tags="inner_frame")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        return add_window, frame, canvas, scrollbar

    rows = []

    column_lookup_entry = {
        "Species": ["Class", "Scientific Name", "Common Name", "Domesticated"],
        "Mutations": ["Scientific Name", "Gene", "Nucleotide Change", "Amino Acid Change", "CpG Associated", "Gain of Function", "URL"],
        "DNA_Sequences": ["Scientific Name", "Gene", "DNA Sequence", "Splice Site"]
        }

    row_count = 1
    add_window, frame, canvas, scrollbar = configure_window(main_window)
    canvas.bind("<Configure>", on_canvas_resize)

    insert_row(True)

    for i in range(20):
        row, row_count = insert_row(False, row_count)
        rows.append(row)