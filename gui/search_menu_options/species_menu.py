import tkinter as tk
from gui.gui_utils import *
from gui.edit_menu_options.add import add_entry


def launch_species_menu(main_window):
    """
    Creates the species menu for the main window.
    
    Args:
        main_window (tk.Tk): The main application window.
    """
    
    # Set new title
    main_window.title("Species Search Menu")
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
    edit_menu.add_command(label = "Add", command = lambda: add_entry(main_window, "Species"))
    edit_menu.add_command(label = "Delete", command = lambda: delete_selected_rows("Species"))
    edit_menu.add_command(label = "Edit", command = lambda: edit_selected_rows("Species", frame, initial_query, 4, 1, 7, widgets_hold, filterable_column_names))
    
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
                       text = "Search for Species",
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
                                    "You will be asked to confirm the deletion or edit.\n\n"
                                    "Double click on a row to view the full details",
                            font = ("Arial", 10),
                            justify='left')
    instructions.grid(row=1, column=1, columnspan=7, pady=10)

    #Initialise a query to fetch all of the species data
    initial_query = '''SELECT
                        Species.Class,
                        Species.Scientific_Name AS [Scientific Name], 
                        Species.Common_Name AS [Common Name], 
                        Species.Domesticated 
                    FROM 
                        Species
                    WHERE
                        1 = 1'''
    
    filterable_column_names = ["Species.Class", "Species.Scientific_Name", "Species.Common_Name", "Species.Domesticated"]
    

    #We want to be able to filter on class, domesticated status, scientific name, and common name. So we create headings for these options.
    class_heading = tk.Label(frame,
                            text = "Class",
                            font = ("Arial", 14, "bold"),
                            width = 30)
    class_heading.grid(row=2, column=1)

    scientific_name_heading = tk.Label(frame,
                                    text = "Scientific Name",
                                    font = ("Arial", 14, "bold"),
                                    width= 30)
    scientific_name_heading.grid(row=2, column=3)

    common_name_heading = tk.Label(frame,
                                    text = "Common Name",
                                    font = ("Arial", 14, "bold"),
                                    width= 30)
    common_name_heading.grid(row=2, column=5)

    domesticated_heading = tk.Label(frame,
                                    text = "Domesticated",
                                    font = ("Arial", 14, "bold"),
                                    width = 30)
    domesticated_heading.grid(row=2, column=7)

    #We want to be able to filter on class, so use the extract_options function to get a list of unique classes from the Species table.
    class_list = extract_options("Species", "Class")
    #We then create a listbox to display these classes
    class_list_box = tk.Listbox(frame, 
                                height=3, 
                                width=30,
                                selectmode="multiple",
                                exportselection=False)
    for item in class_list:
        class_list_box.insert(tk.END, item)
    class_list_box.grid(row=3, column=1)
    widgets_hold.append(class_list_box)

    #Create entries for scientific name and common name
    scientific_name_entry = tk.Entry(frame, 
                                        width=30, 
                                        font=("Arial", 14))
    scientific_name_entry.grid(row=3, column=3)
    widgets_hold.append(scientific_name_entry)

    common_name_entry = tk.Entry(frame, 
                                    width=30, 
                                    font=("Arial", 14))
    common_name_entry.grid(row=3, column=5)
    widgets_hold.append(common_name_entry)

    #Create a list of options for domesticated species
    domesticated_list_box = tk.Listbox(frame,
                                        height=3, 
                                        width=30,
                                        selectmode="multiple",
                                        exportselection=False)
    domesticated_list_box.insert(tk.END, "Yes")
    domesticated_list_box.insert(tk.END, "No")
    domesticated_list_box.grid(row=3, column=7)
    widgets_hold.append(domesticated_list_box)

    create_table(frame, initial_query, 4, 1, 7, widgets = widgets_hold)





