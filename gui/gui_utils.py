import tkinter as tk
from tkinter import ttk
import sqlite3
import gui.table as store
from tkinter import messagebox
import re
from Models.model1 import Model1
from Models.model2 import Model2
from Models.model3 import Model3
import sys

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()
    if hasattr(window, 'main_menu'):
        window.main_menu.delete(0, 'end')  # Clear the menu bar if it exists

def set_connection(conn):
    global connection
    connection = conn

def create_table(window, query, xposition = 0, yposition = 0, span = 1, values = None, widgets = None, table_name = None):
    """
    Creates a table in the given window based on the provided query.
    
    Args:
        window (tk.Tk): The main application window.
        query (str): The SQL query to execute for fetching data.
    """
    average_1 = 0
    average_2 = 0
    average_3 = 0
    cursor = connection.cursor()

    if table_name == "Results":
        query += ''' ORDER BY
                            (Results.Model_1 IS NULL OR Results.Model_2 IS NULL OR Results.Model_3 IS NULL),
                            Species.Scientific_Name,
                            DNA_Sequences.Gene;'''
        


    cursor.execute(query, values if values else [])
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    table = ttk.Treeview(window, columns=columns, show='headings', selectmode='extended')
    table.bind("<Double-1>", lambda event: show_row_details(event))

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100)

    count_1 = 0
    count_2 = 0
    count_3 = 0

    for row in rows:
        table.insert('', tk.END, values=row)
        if table_name == "Results":
            if row[2]:
                average_1 += float(row[2])
                count_1 += 1
            if row[3]:
                average_2 += float(row[3])
                count_2 += 1
            if row[4]:
                average_3 += float(row[4])
                count_3 += 1
    
    if table_name == "Results":
        table.insert('', tk.END, values = ["************", "Average", average_1 / count_1, average_2 / count_2, average_3 / count_3])

    table.grid(row=xposition, column=yposition, pady = 10, sticky='nsew', columnspan= span)
    store.table = table
    if widgets:
        for widget in widgets:
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Listbox):
                widget.selection_clear(0, tk.END)

def check_and_get_foregin_key(table, value):
    if table == "Species":
        query = '''SELECT 
                    Species_ID 
                   FROM 
                    Species 
                   WHERE
                    Scientific_Name = ?'''
    elif table == "DNA_Sequences":
        query = '''SELECT 
                    DNA_Sequences.DNA_Sequence_ID 
                FROM
                    DNA_Sequences 
                LEFT JOIN 
                    Species on DNA_Sequences.Species_ID = Species.Species_ID 
                WHERE 
                    Species.Scientific_Name = ? 
                AND
                    DNA_Sequences.Gene = ?'''
    
    cursor = connection.cursor()
    if type(value) not in (tuple, list):
        value = (value,)
        
    cursor.execute(query, value)
    result = cursor.fetchone()

    return result[0] if result else None

def fetch_primary_key(row_data, table_name):
    row_data = list(row_data)

    primary_key_lookup = {
        "Species": "Species_ID",
        "Mutations": "Mutation_ID",
        "DNA_Sequences": "DNA_Sequence_ID",
        "Results": "Result_ID"
    }

    column_names_lookup = {
        "Species": ["Class", "Scientific_Name", "Common_Name", "Domesticated"],
        "Mutations": ["Species_ID", "Gene", "Nucleotide_Change", "Amino_Acid_Change", "CpG_Associated", "Gain_of_Function", "URL"],
        "DNA_Sequences": ["Species_ID", "Gene", "DNA_Sequence", "Splice_Site"],
        "Results": ["DNA_Sequence_ID", "Model_1", "Model_2", "Model_3"]
    }

    if table_name != "Species" and table_name != "Results":
        species_id = check_and_get_foregin_key("Species", row_data[0])
        values = [species_id] + row_data[1:]
    elif table_name == "Results":
        dna_sequence_id = check_and_get_foregin_key("DNA_Sequences", row_data[0:2])
        values = [dna_sequence_id] + row_data[2:]
    else:
        values = row_data

    conditions = []
    removals = []
    for i, value in enumerate(values):

        if value == 'None':
            conditions.append(f"{column_names_lookup[table_name][i]} is NULL")
            removals.append('None')
        else:
            conditions.append(f"{column_names_lookup[table_name][i]} = ?")

    for removal in removals:
        if removal in values:
            values.remove(removal)

    query = f'''SELECT 
                {primary_key_lookup[table_name]} 
            FROM 
                {table_name} 
            WHERE 
                1 = 1 AND
            '''
    query += ' AND '.join(conditions)

    cursor = connection.cursor()

    cursor.execute(query, values)
    result = cursor.fetchall()


    if len (result) > 1:
        messagebox.showerror("Error", f"Alert, there are duplicate entries in the {table_name} table, please check the data.")

    return result[0] if result else None

def delete_selected_rows(table_name):
    selected_rows = store.table.selection()

    if not selected_rows:
        return
    else:
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected entries?")
        if confirm:
            for row in selected_rows:
                row_data = store.table.item(row, 'values')
                primary_key = fetch_primary_key(row_data, table_name)
                delete_row(table_name, primary_key)
                store.table.delete(row)

def delete_row(table_name, primary_key):
    primary_key_lookup = {
        "Species": "Species_ID",
        "Mutations": "Mutation_ID",
        "DNA_Sequences": "DNA_Sequence_ID"
    }

    query = f'''
                DELETE FROM
                    {table_name}
                WHERE
                    {primary_key_lookup[table_name]} = ?
                '''
    
    if table_name == "Species":
        for table in ["Mutations", "DNA_Sequences"]:

            delete_query = f'''
                    DELETE FROM
                        {table}
                    WHERE
                        Species_ID = ?
                    '''
            cursor = connection.cursor()
            cursor.execute(delete_query, primary_key)
            connection.commit()

    cursor = connection.cursor()
    cursor.execute(query, primary_key)
    connection.commit()

def edit_selected_rows(table_name, window, initial_query, xposition, yposition, span, widgets, column_names):
    selected_rows = store.table.selection()

    if not selected_rows:
        return
    
    for row in selected_rows:
        row_data = store.table.item(row, 'values')
        pop_up_window = tk.Toplevel()
        pop_up_window.title(f"Edit Entry in {table_name}")

        for i, value in enumerate(row_data):
            label = tk.Label(pop_up_window, text = f"{store.table.heading(i)['text']}")
            label.grid(row=0, column=i, padx=10, pady=5)
            entry = tk.Entry(pop_up_window, width=30)
            entry.insert(0, value)
            entry.grid(row=1, column=i, padx=10, pady=5)

        def save_changes():
            row = pop_up_window.grid_slaves(row=1)
            row.reverse()
            new_values = conditions_check(1, row, table_name)
            if type(new_values) == str:
                messagebox.showerror("Error", new_values)
                return
            primary_key = fetch_primary_key(row_data, table_name)
            primary_key = primary_key[0] if primary_key else None
            update_row(primary_key, table_name, new_values)
            pop_up_window.destroy()
            filter_table(window, initial_query, xposition, yposition, span, widgets, column_names)
        
        menu = tk.Menu(pop_up_window)
        menu.add_command(label="Save", command=save_changes)
        menu.add_command(label="Cancel", command=pop_up_window.destroy)
        pop_up_window.config(menu=menu)

        pop_up_window.grab_set()
        pop_up_window.wait_window()

def update_row(primary_key, table_name, new_values):
    primary_key_lookup = {
        "Species": "Species_ID",
        "Mutations": "Mutation_ID",
        "DNA_Sequences": "DNA_Sequence_ID"
    }

    column_names_lookup = {
        "Species": ["Class", "Scientific_Name", "Common_Name", "Domesticated"],
        "Mutations": ["Species_ID", "DNA_Sequence_ID", "Gene", "Nucleotide_Change", "Amino_Acid_Change", "CpG_Associated", "Gain_of_Function", "URL"],
        "DNA_Sequences": ["Species_ID", "Gene", "DNA_Sequence", "Splice_Site"]
    }



    query = f'''
                UPDATE 
                    {table_name}
                SET
                    {', '.join([f"{col} = ?" for col in column_names_lookup[table_name]])}
                WHERE
                    {primary_key_lookup[table_name]} = ?
                '''

    values = new_values + [primary_key]
    cursor = connection.cursor()

    cursor.execute(query, values)
    connection.commit()

def add_row(query, values):
    cursor = connection.cursor()

    cursor.execute(query, values)
    connection.commit()

def extract_options(table, column):
    """
    Extracts unique options from a specified column in a given table.

    Args:
        table (str): The name of the table to query.
        column (str): The name of the column to extract options from.

    Returns:
        list: A list of unique options from the specified column.
    """
    query = f"SELECT DISTINCT {column} FROM {table}"
    cursor = connection.cursor()
    cursor.execute(query)
    options = [row[0] for row in cursor.fetchall()]
    return options

def filter_table(window, initial_query, xposition, yposition, span, widgets, column_names, table_name=None):
    """
    Sorts the options based on the widget type.

    Args:
        window (tk.Tk): The main application window.
        initial_query (str): The initial SQL query to filter data.
        xposition (int): The row position in the grid for the table.
        yposition (int): The column position in the grid for the table.
        span (int): The number of columns the table should span.
        widgets (list): A list of widgets to extract values from.
        column_names (list): A list of column names corresponding to the widgets.
    """
    values = []
    
    for i in range(len(widgets)):
        if widgets[i].winfo_class() == 'Entry':
            if widgets[i].get():
                value = '%'
                value += widgets[i].get()
                value += '%'  # Add wildcard for LIKE query
                values.append(value)
                initial_query += f" AND {column_names[i]} LIKE ?"
        elif widgets[i].winfo_class() == 'Listbox':
            if widgets[i].curselection():
                selected_indices = widgets[i].curselection()
                selected_items = [widgets[i].get(index) for index in selected_indices]
                for item in selected_items:
                    
                    values.append(item)
                initial_query += f" AND {column_names[i]} IN ({', '.join(['?'] * len(selected_items))})"
        elif widgets[i].winfo_class() == 'Checkbutton':
            if widgets[i].var.get():
                initial_query += f" AND {column_names[i]} IS NULL"

    create_table(window, initial_query, xposition, yposition, span, values, table_name = table_name)

def conditions_check(j, row, table_name):
    column_lookup = {
        "Species": ["Class", "Scientific_Name", "Common_Name", "Domesticated"],
        "Mutations": ["Species_ID", "DNA_Sequence_ID", "Gene", "Nucleotide_Change", "Amino_Acid_Change", "CpG_Associated", "Gain_of_Function", "URL"],
        "DNA_Sequences": ["Species_ID", "Gene", "DNA_Sequence", "Splice_Site"]
    }

    column_lookup_entry = {
        "Species": ["Class", "Scientific Name", "Common Name", "Domesticated"],
        "Mutations": ["Scientific Name", "DNA Sequence ID", "Gene", "Nucleotide Change", "Amino Acid Change", "CpG Associated", "Gain of Function", "URL"],
        "DNA_Sequences": ["Scientific Name", "Gene", "DNA Sequence", "Splice Site"]
        }

    entry_data = []
    scientific_name = None
    for i, widget in enumerate(row):
        if type(widget) == str:
            input = widget.strip()
        else:
            input = widget.get().strip()

        if column_lookup[table_name][i] == "Species_ID" and input != '':
            check = check_and_get_foregin_key("Species", input)
            if check:
                entry_data.append(check)
                scientific_name = input
            else:
                return f"Species with Scientific Name '{input}' does not exist in the database, please add it first."
        elif column_lookup[table_name][i] == "DNA_Sequence_ID" and not any(entry == '' for entry in entry_data):
            check = check_and_get_foregin_key("DNA_Sequences", (scientific_name, input))
            if check:
                entry_data.append(check)
                entry_data.append(input)
            else:
                messagebox.showinfo("Alert", f"Please be aware, the species '{scientific_name}' does not have a DNA sequence associated for gene {input}")
                entry_data.append('')
                entry_data.append(input)
        elif column_lookup[table_name][i] == "Splice_Site" and not any(entry == '' for entry in entry_data):
            pattern = r"""
                ^\(                              # Opening parenthesis
                (\[\d+,\s*\d+\]                  # A list like [1, 2]
                (,\s*\[\d+,\s*\d+\])*)           # Zero or more additional lists, comma-separated
                \)$                                         
                    """
            regex = re.compile(pattern, re.VERBOSE)
            if not regex.match(input) and input.lower() != '':
                return f"Invalid Splice Site format in row {j}. Please use the format ([location one, location two], [location three, location four] etc.)"
            else:
                entry_data.append(input)
        else:
            entry_data.append(input)

    if all(entry == '' for entry in entry_data):
        return None
    elif any(entry == '' for entry in entry_data):
        blank_occurence = [i for i, entry in enumerate(entry_data) if entry == '']
        column_names = []
        for index in blank_occurence:
            if column_lookup[table_name][index] == "DNA_Sequence_ID":
                entry_data[index] = None
            elif column_lookup_entry[table_name][index] == "Splice Site":
                entry_data[index] = None
            else:
                column_names.append(column_lookup_entry[table_name][index])
        if len(column_names) > 0:
            return f"All fields are required. Please fill in all fields in row {j+1}\n\nColumn(s): {column_names}."
        
    return entry_data

def run_model(window, model_names, frame, initial_query, xposition, yposition, span, widgets, column_names):
    
    popup = tk.Toplevel(window)
    popup.title("Running Analysis")
    popup.geometry("300x100")
    popup.resizable(False, False)

    # Disable close (X) button
    popup.protocol("WM_DELETE_WINDOW", lambda: None)

    # Make it modal
    popup.transient(window)
    popup.grab_set()

    label = ttk.Label(popup, text="Analysis running...\nPlease wait.", font=("Arial", 12))
    label.pack(pady=20)

    model_lookup = {
        "Model_1": Model1,
        "Model_2": Model2,
        "Model_3": Model3
    }

    query = f'''
                UPDATE
                    Results
                SET
                    {', '.join([f"{model_name} = ?" for model_name in model_names])}
                WHERE
                    Result_ID = ?
            '''

    row_data = []
    if store.table.selection():
        selected_rows = store.table.selection()
    else:
        selected_rows = store.table.get_children()
    
    for row in selected_rows:
        row_data.append(store.table.item(row, 'values'))

    for row in row_data:
        results = []
        if '****' in row[0]:
            continue
        DNA_Sequence_ID = check_and_get_foregin_key("DNA_Sequences", (row[0], row[1]))
        result_ID = fetch_primary_key(row, 'Results')


        DNA_Sequence, splice_site = get_dna_info(DNA_Sequence_ID)

        if DNA_Sequence is None:
            continue

        for model_name in model_names:
            model = model_lookup[model_name](DNA_Sequence, splice_site)
            result = model.get_expected_frequency()

            if isinstance(result, str):
                messagebox.showerror("Error", f"Error for {row[0]}, {row[1]} : {result}")
                continue
            results.append(result)
        
        if result_ID is None:
            query = f'''
                INSERT INTO
                    Results
                ({', '.join(model_names)}, DNA_Sequence_ID)
                VALUES
                    ({', '.join(['?'] * len(model_names))}, ?)
            '''
            results.append(DNA_Sequence_ID)
        else:
            result_ID = result_ID[0]
            results.append(result_ID)

        cursor = connection.cursor()

        cursor.execute(query, results)
        connection.commit()
    
    filter_table(frame, initial_query, xposition, yposition, span, widgets=widgets, column_names=column_names, table_name="Results")

    popup.destroy()

def show_wait_popup(parent):
    popup = tk.Toplevel(parent)
    popup.title("Running Analysis")
    popup.geometry("300x100")
    popup.resizable(False, False)

    # Disable close (X) button
    popup.protocol("WM_DELETE_WINDOW", lambda: None)

    # Make it modal
    popup.transient(parent)
    popup.grab_set()

    label = ttk.Label(popup, text="Analysis running...\nPlease wait.", font=("Arial", 12))
    label.pack(pady=20)

    return popup            
        
        
       
    

def get_dna_info(DNA_Sequence_ID):
    query = '''
                SELECT
                    DNA_Sequences.DNA_Sequence,
                    DNA_Sequences.Splice_Site
                FROM
                    DNA_Sequences
                WHERE
                    DNA_Sequences.DNA_Sequence_ID = ?
            '''
    
    cursor = connection.cursor()
    cursor.execute(query, (DNA_Sequence_ID,))
    result = cursor.fetchone()

    if result:
        return result[0], result[1]
    else:
        messagebox.showerror("Error", "DNA Sequence not found, please contact Nat.")
        return None, None
        
        
def check_mutations(species_id, gene):
    """
    When adding a new DNA sequence, this function checks if there are any mutations associated with the species and gene.
    If there are it appends the DNA sequence ID to the mutations table.
    """

    query = '''
                SELECT
                    DNA_Sequence_ID
                FROM
                    DNA_Sequences
                WHERE
                    Species_ID = ?
                AND
                    Gene = ?
            '''
    
    cursor = connection.cursor()
    cursor.execute(query, (species_id, gene))
    DNA_sequence_ID = cursor.fetchone()

    query = '''
                SELECT
                    Mutation_ID
                FROM
                    Mutations
                WHERE
                    Species_ID = ?
                AND
                    Gene = ?'''

    cursor.execute(query, (species_id, gene))
    mutations_IDs = cursor.fetchall()

    if DNA_sequence_ID and mutations_IDs:
        for mutation_ID in mutations_IDs:
            query = '''
                        UPDATE
                            Mutations
                        SET
                            DNA_Sequence_ID = ?
                        WHERE
                            Mutation_ID = ?
                    '''

            cursor.execute(query, (DNA_sequence_ID[0], mutation_ID[0]))
            connection.commit()

def show_row_details(event):
    """
    Show details of the selected row in a popup window when double-clicked.
    """

    item = store.table.identify_row(event.y)
    if not item:
        return
    values = store.table.item(item, 'values')

    details_window = tk.Toplevel()
    details_window.title("Row Details")
    details_window.geometry("400x300")

    for i, value in enumerate(values):
        label = tk.Label(details_window, text=f"{store.table.heading(i)['text']}:")
        text = tk.Text(details_window, wrap='word', height=1, width=40)
        text.insert(tk.END, value)
        label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
        text.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
    
    details_window.grid_columnconfigure(1, weight=1)
    
def build_base_menu(window):
    menu = tk.Menu(window)

    # Add dummy Apple menu if on macOS
    if sys.platform == "darwin":
        apple_menu = tk.Menu(menu, name='apple')
        apple_menu.add_command(label="About Mutational Bias")
        menu.add_cascade(menu=apple_menu)

    return menu
