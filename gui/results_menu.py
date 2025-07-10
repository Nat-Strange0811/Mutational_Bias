import tkinter as tk
from gui.gui_utils import *

def launch_results_menu(main_window):
    '''
    Creates the analysis menu for the main window.
    Args:
        main_window (tk.Tk): The main application window.
    '''

    main_window.title("Species Search Menu")
    widgets = []
    frame = tk.Frame(main_window)
    frame.grid(row=0, column=0, sticky='nsew')

    main_window.rowconfigure(0, weight=1)
    main_window.columnconfigure(0, weight=1)

    home_menu = tk.Menu(main_window, tearoff=0)
    model_menu = tk.Menu(main_window, tearoff=0)
    filter_menu = tk.Menu(main_window, tearoff=0)
    
    from gui.HomePage import create_home_page
    home_menu.add_command(label="Home", command=lambda: create_home_page(main_window))
    filter_menu.add_command(label = "Search", command = lambda: filter_table(frame, initial_query, 4, 1, 7, widgets, filterable_column_names, table_name = "Results"))
    filter_menu.add_command(label = "Clear", command = lambda: create_table(frame, initial_query, 4, 1, 7, widgets = widgets, table_name = "Results"))
    model_menu.add_command(label = "Run Model 1", command = lambda: run_model(main_window, ["Model_1"], frame, initial_query, 4, 1, 7, widgets, filterable_column_names))
    model_menu.add_command(label = "Run Model 2", command = lambda: run_model(main_window, ["Model_2"], frame, initial_query, 4, 1, 7, widgets, filterable_column_names))
    model_menu.add_command(label = "Run Model 3", command = lambda: run_model(main_window, ["Model_3"], frame, initial_query, 4, 1, 7, widgets, filterable_column_names))
    model_menu.add_command(label = "Run All Models", command = lambda: run_model(main_window, ["Model_1", "Model_2", "Model_3"], frame, initial_query, 4, 1, 7, widgets, filterable_column_names))
    rows = 11
    columns = 9
    for i in range(rows):
        frame.rowconfigure(i, weight=1)
    for j in range(columns):
        frame.columnconfigure(j, weight=1)


    heading = tk.Label(frame,
                       text = "Search Stored Results",
                       font = ("Arial", 24, "bold"),
                       bg = 'black',
                       fg = 'white',
                       relief = 'raised',
                       bd = 10,
                       padx = 20,
                       pady = 20)
    heading.grid(row=0, column=1, columnspan=7, pady=10)

    instructions = tk.Label(frame,
                            text =  "Below is a table of results for all DNA Sequences stored within the database\n"

                                    "Select or type the filters you want to apply and click 'Search'.\n"
                                    "To clear the filters and view all results, click 'Clear'.\n" \
                                    "The filters will automatically apply to the average percentage displayed\n"
                                    "To return to the home page, click 'Home'.\n\n" \
                                    
                                    "You can run models by selecting the options in the menu bar, note the filters will apply to the models.\n"
                                    "Alternatively, you can select the rows you want to run using ctrl + left click. Note, row select is stronger than the filters\n" \
                                    "To view results of binomial tests, generate graphs and reports, select the Analysis menu.\n\n" \
                                    "Double click on a row to view the full details",
                            font = ("Arial", 10),
                            justify='left')
    instructions.grid(row=1, column=1, columnspan=7, pady=10)

    initial_query = '''SELECT
                            Species.Scientific_Name as [Scientific Name],
                            DNA_Sequences.Gene as [Gene],
                            Results.Model_1 as [Model 1],
                            Results.Model_2 as [Model 2],
                            Results.Model_3 as [Model 3]
                        FROM
                            DNA_Sequences
                        LEFT JOIN
                            Species
                        ON
                            DNA_Sequences.Species_ID = Species.Species_ID
                        LEFT JOIN
                            Results
                        ON
                            Results.DNA_Sequence_ID = DNA_Sequences.DNA_Sequence_ID
                        WHERE
                            1 = 1
                    '''

    filterable_column_names = ['Species.Scientific_Name', 'DNA_Sequences.Gene', 'Results.Model_1', 'Results.Model_2', 'Results.Model_3']

    scientific_name_heading = tk.Label(frame,
                                    text = "Scientific Name",
                                    font = ("Arial", 14, "bold"),
                                    width= 30)
    scientific_name_heading.grid(row=2, column=2)

    gene_heading = tk.Label(frame,
                            text = "Gene",
                            font = ("Arial", 14, "bold"),
                            width= 30)
    gene_heading.grid(row=2, column=4)

    results_heading = tk.Label(frame,
                                text = "No Results",
                                font = ("Arial", 14, "bold"),
                                width= 30)
    results_heading.grid(row=2, column=6, sticky='ew')

    scientific_name_entry = tk.Entry(frame, 
                                    width=30, 
                                    font=("Arial", 14))
    scientific_name_entry.grid(row=3, column=2)
    widgets.append(scientific_name_entry)

    gene_options = extract_options('DNA_Sequences', 'Gene')
    gene_listbox_entry = tk.Listbox(frame,
                                    width=30,
                                    font=("Arial", 14),
                                    height=3,
                                    exportselection=False,
                                    selectmode='multiple')
    for option in gene_options:
        gene_listbox_entry.insert(tk.END, option)
    gene_listbox_entry.grid(row=3, column=4)
    widgets.append(gene_listbox_entry)

    sub_frame = tk.Frame(frame)
    var1 = tk.BooleanVar()
    sub_frame.grid(row=3, column=6, sticky='')
    results_1_checkbox = tk.Checkbutton(sub_frame,
                                        text="Model 1",
                                        font=("Arial", 10),
                                        variable=var1,
                                        onvalue=1,
                                        offvalue=0)
    results_1_checkbox.grid(row=0, column=0, sticky='')
    results_1_checkbox.var = var1
    widgets.append(results_1_checkbox)
    
    var2 = tk.BooleanVar()
    results_2_checkbox = tk.Checkbutton(sub_frame,
                                        text="Model 2",
                                        font=("Arial", 10),
                                        variable=var2,
                                        onvalue=1,
                                        offvalue=0)
    results_2_checkbox.grid(row=0, column=1, sticky='')
    results_2_checkbox.var = var2
    widgets.append(results_2_checkbox)

    var3 = tk.BooleanVar()
    results_3_checkbox = tk.Checkbutton(sub_frame,
                                        text="Model 3",
                                        font=("Arial", 10),
                                        variable=var3,
                                        onvalue=1,
                                        offvalue=0)
    results_3_checkbox.grid(row=0, column=2, sticky='')
    results_3_checkbox.var = var3
    widgets.append(results_3_checkbox)


    main_menu = main_window.main_menu
    main_menu.add_cascade(label="Home", menu=home_menu)
    main_menu.add_cascade(label="Model Options", menu=model_menu)
    main_menu.add_cascade(label="Filter Options", menu=filter_menu)

    create_table(frame, initial_query, 4, 1, 7, widgets = widgets, table_name = "Results")
    



