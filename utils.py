from pathlib import Path
import shutil
import appdirs
import sys, os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import csv
from gui.gui_utils import *
from Bio import Entrez, SeqIO
import decimal

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):  # PyInstaller (Windows)
        base_path = Path(sys._MEIPASS)
    elif getattr(sys, 'frozen', False):  # py2app (macOS)
        base_path = Path(sys.executable).parent.parent / 'Resources'
    else:  # Development
        base_path = Path(__file__).parent
    return base_path / relative_path


def get_db_path():

    develop = False
    if develop:
        return resource_path("Database/CpG_data.db")
    
    APP_NAME = "Mutational_Bias"
    APP_AUTHOR = "NatStrange"

    data_dir = Path(appdirs.user_data_dir(APP_NAME, APP_AUTHOR))
    data_dir.mkdir(parents=True, exist_ok=True)

    target = data_dir / "Mutational_Bias.db"
    source = resource_path("Database/CpG_data.db")

    if not target.exists():
        shutil.copy2(source, target)

    return str(target)


def add_data_from_csv(main_window):
    """
    Extracts data from a CSV file and adds it to the database.
    """
    format_lookup = [["Class", "Scientific Name", "Common Name", "Domesticated"], ["Scientific Name", "Gene", "Nucleotide Change", "Amino Acid Change", "CpG Associated", "Gain of Function", "URL"], ["Scientific Name", "Gene", "DNA Sequence", "Splice Site"]]
    
    table_lookup = {
        ("Class", "Scientific Name", "Common Name", "Domesticated"): "Species",
        ("Scientific Name", "Gene", "Nucleotide Change", "Amino Acid Change", "CpG Associated", "Gain of Function", "URL"): "Mutations",
        ("Scientific Name", "Gene", "DNA Sequence", "Splice Site"): "DNA_Sequences"
    }

    column_lookup = {
            "Species": ["Class", "Scientific_Name", "Common_Name", "Domesticated"],
            "Mutations": ["Species_ID", "DNA_Sequence_ID","Gene", "Nucleotide_Change", "Amino_Acid_Change", "CpG_Associated", "Gain_of_Function", "URL"],
            "DNA_Sequences": ["Species_ID", "Gene", "DNA_Sequence", "Splice_Site"]
            }

    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv")]
    )

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the header row
        data = [row for row in reader]  # Read the rest of the rows

    if headers not in format_lookup:
        messagebox.showerror("Error", "CSV file does not have the correct headers. Please ensure the headers match the expected format.")
        return
    else:
        for j, row in enumerate(data):
            table_name = table_lookup[tuple(headers)]
            print(headers, row)
            entry_data = conditions_check(j, row, table_name)

            query = f'''INSERT INTO
                            {table_name}
                            ({', '.join(column_lookup[table_name])})
                        VALUES
                            ({', '.join(['%s'] * len(column_lookup[table_name]))})'''
            
            if entry_data == None:
                continue
            elif type(entry_data) != str:
                error = add_row(query, entry_data)
                if error:
                    messagebox.showerror("Error", f"An error occurred while adding the entry: {error}, please contact Nat")
            else:
                messagebox.showerror("Error", entry_data)
    


def add_dna_sequences_from_genbank(main_window):
    """
    Extracts DNA sequences from a GenBank link.
    """
    Entrez.email = "ns793@cantab.ac.uk"
    genbank_link = simpledialog.askstring("GenBank Accession ID", "Enter the GenBank Accession ID:", parent=main_window)

    if not genbank_link:
        return
    try:
        handle = Entrez.efetch(db="nuccore", id=genbank_link, rettype="gb", retmode="text")
        record = SeqIO.read(handle, "genbank")
        handle.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching the GenBank record: {e}\n\nPlease contact Nat")
        return
    
    dna_sequence = str(record.seq)
    scientific_name = record.annotations.get("organism", "Unknown Species")
    if 'MC1R' in record.description:
        gene = "MC1R"
    elif 'ASIP' in record.description:
        gene = "ASIP"
    else:
        gene = simpledialog.askstring("Gene", "Could not extract gene, please enter the gene name (e.g., MC1R, ASIP):", parent=main_window)

    source_store = record.annotations.get("source", "Unknown Source")
    if "(" in source_store and ")" in source_store:
        common_name = source_store.split("(")[-1].split(")")[0]
    else:
        common_name = simpledialog.askstring("Common Name", "Could not extract common name from scientific name stored in GenBank record. Please enter manually:", parent = main_window)
    
    species_id = check_and_get_foregin_key("Species", scientific_name)
    
    while True:
        species_id = check_and_get_foregin_key("Species", scientific_name)
        if species_id:
            query = '''INSERT INTO
                            DNA_Sequences
                            (Species_ID, Gene, DNA_Sequence, Splice_Site)
                        VALUES
                            (%s, %s, %s, %s)
                        '''
            splice_site = simpledialog.askstring("Splice Site", "Enter the splice site (if applicable, otherwise leave blank):", parent = main_window)
            if splice_site == "":
                splice_site = None
            entry_data = (species_id, gene, dna_sequence, splice_site)
            add_row(query, entry_data)
            check_mutations(species_id, gene)
            return
        else:
            class_name = simpledialog.askstring("Class", "Enter the class of the species (e.g., Mammal, Reptile etc.):").strip()
            domesticated = simpledialog.askstring("Domesticated", "Is this species domesticated? (yes/no):").strip()
            query = '''INSERT INTO 
                            Species
                            (Class, Scientific_Name, Common_Name, Domesticated)
                        VALUES
                            (%s, %s, %s, %s)
                        '''
            entry_data = (class_name, scientific_name, common_name, domesticated)
            add_row(query, entry_data)
            species_id = check_and_get_foregin_key("Species", scientific_name)
    





def import_database(main_window):
    """
    Imports a database from a file.
    """
    confirm = messagebox.askyesno("Import Database", "Please note, this will overwrite the current database, and is not reversible.\n\nDo you want to continue?", parent=main_window)

    if not confirm:
        return
    
    file_path = filedialog.askopenfilename(
        title="Select Database File",
        filetypes=[("Database files", "*.db")]
    )
    tables = ["species", "mutations", "dna_sequences", "results"]

    data_type_lookup = {
        "species": ["TEXT", "TEXT", "TEXT", "INTEGER", "TEXT"],
        "mutations": ["INTEGER", "INTEGER", "INTEGER", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT"],
        "dna_sequences": ["INTEGER", "INTEGER", "TEXT", "TEXT", "TEXT"],
        "results" : ["INTEGER", "INTEGER", "NUMERIC(4,2)", "NUMERIC(4,2)", "NUMERIC(4,2)"]
    }


    if not file_path:
        return
    
    try:
        sqlite_conn = sqlite3.connect(file_path)
        sqlite_cursor = sqlite_conn.cursor()
        sqlpg_conn = set_connection()
        sqlpg_cursor = sqlpg_conn.cursor()
        for table in tables:
            query = f"SELECT * FROM {table}"
            sqlite_cursor.execute(query)
            rows = sqlite_cursor.fetchall()
            columns = [description[0] for description in sqlite_cursor.description]
            destroy = f"DROP TABLE IF EXISTS {table}"
            sqlpg_cursor.execute(destroy)
            create = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join([f'{col} {data_type_lookup[table][i]}' for i,col in enumerate(columns)])})"
            sqlpg_cursor.execute(create)
            if rows:
                for row in rows:
                    cleaned_row = [str(value) if isinstance(value, decimal.Decimal) else value for value in row]
                    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
                    sqlpg_cursor.execute(query, cleaned_row)

        sqlpg_conn.commit()

    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"An error occurred while importing the database: {e}\n\nPlease contact Nat")
        return



def export_database(main_window):
    """
    Exports the database to a file.
    """
    tables = ["species", "mutations", "dna_sequences", "results"]

    data_type_lookup = {
        "species": ["TEXT", "TEXT", "TEXT", "INTEGER", "TEXT"],
        "mutations": ["INTEGER", "INTEGER", "INTEGER", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT"],
        "dna_sequences": ["INTEGER", "INTEGER", "TEXT", "TEXT", "TEXT"],
        "results" : ["INTEGER", "INTEGER", "NUMERIC(4,2)", "NUMERIC(4,2)", "NUMERIC(4,2)"]
    }

    folder_path = filedialog.askdirectory(
        title="Select Export Folder")
    
    if not folder_path:
        return
    try:
        sqlite_conn = sqlite3.connect(os.path.join(folder_path, "Mutational_Bias.db"))
        sqlite_cursor = sqlite_conn.cursor()
        sqlpg_conn = set_connection()
        sqlpg_cursor = sqlpg_conn.cursor()
        for table in tables:
            query = f"SELECT * FROM {table}"
            sqlpg_cursor.execute(query)
            rows = sqlpg_cursor.fetchall()
            columns = [description[0] for description in sqlpg_cursor.description]
            destroy = f"DROP TABLE IF EXISTS {table}"
            sqlite_cursor.execute(destroy)
            create = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join([f'{col} {data_type_lookup[table][i]}' for i,col in enumerate(columns)])})"
            sqlite_cursor.execute(create)
            if rows:
                for row in rows:
                    cleaned_row = [str(value) if value is not None else '' for value in row]
                    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
                    sqlite_cursor.execute(query, cleaned_row)

        sqlite_conn.commit()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while exporting the database: {e}\n\nPlease contact Nat")
        return