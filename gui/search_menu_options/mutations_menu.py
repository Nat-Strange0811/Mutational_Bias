import tkinter as tk
from gui.gui_utils import *
from gui.edit_menu_options.add import add_entry


def launch_mutations_menu(main_window):
    """
    Creates the mutations menu for the main window.
    
    Args:
        main_window (tk.Tk): The main application window.
    """
    
    # Set new title
    main_window.title("Mutations Search Menu")
    widgets_hold = []

    #Establish a frame to hold the widgets
    frame = tk.Frame(main_window)
    frame.grid(row=0, column=0, sticky='nsew')

    #Configure the main window and frame to expand with the window size
    main_window.rowconfigure(0, weight=1)
    main_window.columnconfigure(0, weight=1)

    #Define the menu
    main_menu = tk.Menu(main_window)

    home_menu = tk.Menu(main_window, tearoff=0)
    filter_menu = tk.Menu(main_window, tearoff=0)
    edit_menu = tk.Menu(main_window, tearoff=0) 

    from gui.HomePage import create_home_page
    home_menu.add_command(label = "Home", command = lambda: create_home_page(main_window))
    filter_menu.add_command(label = "Search", command = lambda: filter_table(frame, initial_query, 4, 1, 7, widgets_hold, filterable_column_names))
    filter_menu.add_command(label = "Clear", command = lambda: create_table(frame, initial_query, 4, 1, 7, widgets = widgets_hold))
    edit_menu.add_command(label = "Add", command = lambda: add_entry(main_window, "Mutations"))
    edit_menu.add_command(label = "Delete", command = lambda: delete_selected_rows("Mutations"))
    edit_menu.add_command(label = "Edit", command = lambda: edit_selected_rows("Mutations", frame, initial_query, 4, 1, 7, widgets_hold, filterable_column_names))
    
    main_menu.add_cascade(label="Home", menu=home_menu)
    main_menu.add_cascade(label="Filter Options", menu=filter_menu)
    main_menu.add_cascade(label="Edit Options", menu=edit_menu)

    main_window.config(menu=main_menu)

    #Define the number of rows and columns in the frame and configure them to expand
    rows = 11
    columns = 9
    for i in range(rows):
        frame.rowconfigure(i, weight=1)
    for j in range(columns):
        frame.columnconfigure(j, weight=1)
    
    #Set heading
    heading = tk.Label(frame,
                       text = "Search for Mutations",
                       font = ("Arial", 24, "bold"),
                       bg = 'black',
                       fg = 'white',
                       relief = 'raised',
                       bd = 10,
                       padx = 20,
                       pady = 20)
    heading.grid(row=0, column=1, columnspan=7, pady=10)

    #Create a label to display the instructions
    instructions = tk.Label(frame,
                            text = "Select or type the filters you want to apply and click 'Search'.\n"
                                    "To clear the filters and view all species, click 'Clear'.\n"
                                    "To return to the home page, click 'Back'.\n" \
                                    "To add a new species, click 'Add'.\n"
                                    "To delete a species, select the row and click 'Delete'.\n" \
                                    "To edit a species, select the row and click 'Edit'.\n\n"

                                    "You can delete and edit multiple entries at once by holding ctrl and selecting multiple rows.\n"
                                    "You will be asked to confirm the deletion or edit.\n"

                                    "Double click on a row to view the full details",
                            font = ("Arial", 10),
                            justify='left')
    instructions.grid(row=1, column=1, columnspan=7, pady=10)

    #Initialise a query to fetch all of the species data
    initial_query = '''SELECT 
                        Species.Scientific_Name AS [Scientific Name],
                        Mutations.Gene,
                        Mutations.Nucleotide_Change AS [Nucleotide Change],
                        Mutations.Amino_Acid_Change AS [Amino Acid Change],
                        Mutations.CpG_Associated AS [CpG Associated],
                        Mutations.Gain_of_Function AS [Gain of Function],
                        Mutations.URL
                    FROM 
                        Mutations
                    LEFT JOIN
                        Species ON Mutations.Species_ID = Species.Species_ID
                    WHERE
                        1 = 1'''
    
    filterable_column_names = ["Species.Scientific_Name", "Mutations.Gene", "Mutations.CpG_Associated", "Mutations.Gain_of_Function"]
    

    #We want to be able to filter on class, domesticated status, scientific name, and scientific name. So we create headings for these options.
    scientific_name_heading = tk.Label(frame,
                                    text = "Scientific Name",
                                    font = ("Arial", 14, "bold"),
                                    width= 30)
    scientific_name_heading.grid(row=2, column=1)

    gene_heading = tk.Label(frame,
                            text = "Gene",
                            font = ("Arial", 14, "bold"),
                            width = 30)
    gene_heading.grid(row=2, column=3)

    CpG_associated_heading = tk.Label(frame,
                                        text = "CpG Associated",
                                        font = ("Arial", 14, "bold"),
                                        width = 30)
    CpG_associated_heading.grid(row=2, column=5)

    gain_of_function_heading = tk.Label(frame,
                                        text = "Gain of Function",
                                        font = ("Arial", 14, "bold"),
                                        width = 30)
    gain_of_function_heading.grid(row=2, column=7)

    #Create entries for scientific name

    scientific_name_entry = tk.Entry(frame, 
                                width=30, 
                                font=("Arial", 14))
    scientific_name_entry.grid(row=3, column=1)
    widgets_hold.append(scientific_name_entry)

    #Create a list of options for genes
    gene_options = extract_options("DNA_Sequences", "Gene")
    gene_list_box = tk.Listbox(frame,
                                height=3, 
                                width=30,
                                selectmode="multiple",
                                exportselection=False)
    gene_list_box.grid(row=3, column=3)
    for option in gene_options:
        gene_list_box.insert(tk.END, option)
    widgets_hold.append(gene_list_box)

    #Create a list of options for CpG associated
    CpG_list_box = tk.Listbox(frame,
                                height=3,
                                width=30,
                                selectmode="multiple",
                                exportselection=False)
    CpG_list_box.grid(row=3, column=5)
    CpG_options = ["Yes", "No"]
    for option in CpG_options:
        CpG_list_box.insert(tk.END, option)
    widgets_hold.append(CpG_list_box)

    #Create a list of options for gain of function
    gain_of_function_list_box = tk.Listbox(frame,
                                            height=3, 
                                            width=30,
                                            selectmode="multiple",
                                            exportselection=False)
    gain_of_function_list_box.grid(row=3, column=7)
    gain_of_function_options = ["Gain", "Loss"]
    for option in gain_of_function_options:
        gain_of_function_list_box.insert(tk.END, option)
    widgets_hold.append(gain_of_function_list_box)                              

    create_table(frame, initial_query, 4, 1, 7, widgets = widgets_hold)

    main_window.bind("<Button-3>", lambda event: copy_url_sequence(event, main_window))

def copy_url_sequence(event, main_window):
    """
    Copies the URL of the mutation to the clipboard when a row is clicked.
    Args:
        event (tk.Event): The event triggered by clicking on a row.
        main_window (tk.Tk): The main application window.
    """
    if not isinstance(event.widget, tk.ttk.Treeview):
        return
    
    table = event.widget
    item = table.identify_row(event.y)
    if not item:
        return
    values = table.item(item, 'values')
    try:
        url = values[6]
    except IndexError:
        url = "<No URL>"

    main_window.clipboard_clear()
    main_window.clipboard_append(url)
    main_window.update()  # Keep the clipboard content until the program exits
