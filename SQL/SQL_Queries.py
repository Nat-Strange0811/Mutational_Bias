import sqlite3
from Models.model1 import Model1
from Models.model2 import Model2
from Models.model3 import Model3

def set_connection(conn):
    global connection
    connection = conn


def print_table(rows, cursor):
    print('\n')
    if rows:
        headers = [description[0] for description in cursor.description]

        col_widths = [max(len(str(row[i])) for row in rows) for i in range(len(headers))]
        col_widths = [max(len(header), width) for header, width in zip(headers, col_widths)]


        header_line = " | ".join(header.ljust(col_widths[i]) for i, header in enumerate(headers))
        print(header_line)
        print("-" * len(header_line))

        for row in rows:
            row_line = " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row)))
            print(row_line)
        print('----------------------------------------------------------------')
        input("Press Enter to continue...")
        print('----------------------------------------------------------------\n\n\n')
        return True
    else:
        print('No entries matching those restrictions')
        print('----------------------------------------------------------------')
        input("Press Enter to continue...")
        print('----------------------------------------------------------------\n\n\n')
        return False
    
def View():
    criteria = []
    cursor = connection.cursor()
    query = f'''SELECT 
                            Mutations.Species_ID,
                            Species.Genus_Species,
                            Species.Common_Name,
                            Mutations.Mutation_ID,
                            Mutations.Gene,
                            Mutations.Nucleotide_Change,
                            Mutations.Amino_Acid_Change,
                            Mutations.CpG_Associated,
                            Mutations.Gain_of_Function 
                        FROM 
                            Mutations 
                        LEFT JOIN 
                            Species 
                        ON 
                            Species.Species_ID = Mutations.Species_ID 
                        WHERE 1=1'''

    parameters = []
    criteria = filter(["Species_ID", "Genus_Species", "Common_Name", "Mutation_ID", "Gene", "Nucleotide_Change", "Amino_Acid_Change", "CpG_Associated", "Gain_of_Function"])
    headings = [
                "Mutations.Species_ID",
                "Species.Genus_Species",
                "Species.Common_Name",
                "Mutations.Mutation_ID",
                "Mutations.Gene",
                "Mutations.Nucleotide_Change",
                "Mutations.Amino_Acid_Change",
                "Mutations.CpG_Associated",
                "Mutations.Gain_of_Function"]


    for i in range(len(criteria)):
        if criteria[i] != '':
            query += f" AND {headings[i]} = ?"
            parameters.append(criteria[i])

    cursor.execute(query,parameters)

    rows = cursor.fetchall()

    check = print_table(rows, cursor)           #calls the print function above
    return check

def filter(categories):
    criteria = []
    print(f"Please enter the values you would like to filter on when \nprompted, press enter to skip a field.")
    print(f"-------------------------------------------------------------")
    for category in categories:
        value = input(f"Enter the value for {category}: ")
        criteria.append(value)
    return criteria

def View_DNA_Sequences(DNA_Sequence_ID = None):
    cursor = connection.cursor()

    query = '''SELECT
                    DNA_Sequences.DNA_Sequence_ID,
                    Species.Genus_Species,
                    Species.Common_Name,
                    DNA_Sequences.Gene,
                    DNA_Sequences.DNA_Sequence
                FROM
                    DNA_Sequences
                LEFT JOIN
                    Species
                ON
                    Species.Species_ID = DNA_Sequences.Species_ID
                WHERE 1=1'''
    
    parameters = []
    criteria = filter(["DNA_Sequence_ID", "Genus_Species", "Common_Name", "Gene"])
    headings = [
                "DNA_Sequences.DNA_Sequence_ID",
                "Species.Genus_Species",
                "Species.Common_Name",
                "DNA_Sequences.Gene"]
    
    if DNA_Sequence_ID is None:
        pass
    else:
        query += " AND DNA_Sequences.DNA_Sequence_ID = ?"
        parameters.append(DNA_Sequence_ID)
        cursor.execute(query, parameters)
        rows = cursor.fetchall()
        return rows

    for i in range(len(criteria)):
        if criteria[i] != '':
            query += f" AND {headings[i]} = ?"
            parameters.append(criteria[i])
    cursor.execute(query, parameters)
    rows = cursor.fetchall()
    check = print_table(rows, cursor)
    return check

def View_Species(species = None):
    cursor = connection.cursor()
    query = '''SELECT
                        Species.Species_ID,
                        Species.Class,
                        Species.Genus_Species,
                        Species.Common_Name
                    FROM
                        Species
                    WHERE 1=1
            '''
    
    parameters = []
    criteria = filter(["Species_ID", "Class", "Genus_Species", "Common_Name", "Domesticated"])
    headings = [
                "Species.Species_ID",
                "Species.Class",
                "Species.Genus_Species",
                "Species.Common_Name",
                "Species.Domesticated"]

    if species is None:
        pass
    else:
        query += " AND Species.Species_ID = ?"
        parameters.append(species)
        cursor.execute(query, parameters)
        rows = cursor.fetchall()
        return rows

    for i in range(len(criteria)):
        if criteria[i] != '':
            query += f" AND {headings[i]} = ?"
            parameters.append(criteria[i])
    cursor.execute(query, parameters)
    rows = cursor.fetchall()
    check = print_table(rows, cursor)
    return check

def Retrieve_URL():
    cursor = connection.cursor()
    query = '''SELECT 
                        Species.Genus_Species,
                        Species.Common_Name,
                        Mutations.Gene,
                        Mutations.Nucleotide_Change,
                        Mutations.Amino_Acid_Change,
                        Mutations.URL
                    FROM 
                        Species 
                    RIGHT JOIN 
                        Mutations 
                    ON 
                        Species.Species_ID = Mutations.Species_ID 
                    WHERE 1=1
            '''
    
    parameters = []

    print(f"-------------------------------------------------------------")
    print(f"Please enter the mutation ID(s) you would like to retrieve the \nURL for, leave blank when finished")
    print(f"-------------------------------------------------------------")

    active = True
    while active:
        species = input("Mutation ID: ")
        if species == '':
            active = False
        else:
            query += " AND Mutations.Mutation_ID = ?"
            parameters.append(species)

    cursor.execute(query, parameters)
    rows = cursor.fetchall()
    check = print_table(rows, cursor)
    return check

def Add(Table):
    active = True
    if Table == "Mutations" or Table == "DNA_Sequences":
        while active:
            print(f"-------------------------------------------------------------")
            print(f"Is the species you would like to add a mutation for already \nin the database? (Yes/No)")
            confirm = input(f"Species in Database: ")
            if confirm not in ['Yes', 'No']:
                print(f"Please enter either 'Yes' or 'No'.")
            elif confirm == 'No':
                print(f"Please add the species first.")
                Add("Species")
                active = False
            else:
                active = False

        print(f"-------------------------------------------------------------")
        print(f"Would you like to check the Species ID(s) in the database?")
        print(f"--------------------------------------------------------------")
        loop = True
        while loop:    
            confirm = input(f"Check Species IDs (Yes/No): ")
            if confirm.lower() not in ['yes', 'no']:
                print(f"Please enter either 'Yes' or 'No'.")
                print(f"-------------------------------------------------------------")
            elif confirm.lower() == 'yes':
                View_Species()
                loop = False
            else:
                loop = False

    if Table == "Mutations":
        going = True
        while going:
            print(f"-------------------------------------------------------------")
            print(f"Is the DNA sequence you would like to add a mutation for already \nin the database? (Yes/No)")
            confirm = input(f"DNA Sequence in Database: ")
            if confirm not in ['Yes', 'No']:
                print(f"Please enter either 'Yes' or 'No'.")
            elif confirm == 'No':
                print(f"Please add the DNA sequence first.")
                Add("DNA_Sequences")
                going = False
            else:
                going = False
            active = False
        
        print(f"-------------------------------------------------------------")
        print(f"Would you like to check the DNA Sequence ID(s) in the database?")
        print(f"--------------------------------------------------------------")
        loop = True
        while loop:    
            confirm = input(f"Check DNA_Sequence IDs (Yes/No): ")
            if confirm.lower() not in ['yes', 'no']:
                print(f"Please enter either 'Yes' or 'No'.")
            elif confirm.lower() == 'yes':
                View_DNA_Sequences()
                loop = False
            else:
                loop = False

    print(f"-------------------------------------------------------------")
    print(f"Please enter the details of the {Table} you would like to add")
    print(f"-------------------------------------------------------------")

    cursor = connection.cursor()
    Initial_query = f"SELECT * FROM {Table}"
    cursor.execute(Initial_query)
    headers = [description[0] for description in cursor.description]
    values = []

    for header in headers:
        if (header == 'Species_ID' and Table == "Species") or (header == 'Mutation_ID' and Table == "Mutations") or (header == 'DNA_Sequence_ID' and Table == "DNA_Sequences"):
            headers.pop(headers.index(header))

    for header in headers:
            User_Input = input(f"Enter the Value for {header}: ")
            values.append(User_Input)
            if header == 'Species_ID':
                if not View_Species(User_Input):
                    print(f"Species ID {User_Input} not found in the database. Please add the species first.")
                    return False
            if header == 'DNA_Sequence_ID':
                if not View_DNA_Sequences():
                    print(f"DNA Sequence ID {User_Input} not found in the database. Please add the DNA sequence first.")
                    return False

    values_formatted = ', '.join(['?'] * len(values))
    column_names = ', '.join(headers)
    query = f"INSERT INTO {Table} ({column_names}) VALUES ({values_formatted})"

    print(f"-------------------------------------------------------------")
    print(f"Please confirm the following values are correct before adding:")
    for header, value in zip(headers, values):
        print(f"{header}: {value}")
    print(f"-------------------------------------------------------------")
    confirm = input("Confirm (Yes/No): ")
    loop = True

    while loop:
        if confirm.lower() not in ['yes', 'no']:
            print(f"-------------------------------------------------------------")
            print("Please enter either 'Yes' or 'No'.")
            print(f"-------------------------------------------------------------")
            confirm = input("Confirm (Yes/No): ")
        else:
            loop = False

    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return True

    try:
        cursor.execute(query, values)
        connection.commit()
        print('Row succesfully added\n\n\n')
        return True

    except sqlite3.Error as e:
        print(f"An error occurred while saving changes: {e}\n\n\n")
        return True
    
def Update(Table):
    cursor = connection.cursor()
    Initial_query = f"SELECT * FROM {Table}"
    cursor.execute(Initial_query)
    headers = [description[0] for description in cursor.description]
    run = True
    rows_to_edit = []
    list_of_columns = []
    list_of_values = []
    
    print(f"-------------------------------------------------------------")
    print(f"Would you like to check the ID(s) in {Table} before editing?")
    print(f"-------------------------------------------------------------")
    confirm = input(f"Check IDs (Yes/No): ")
    go = True
    while go:
        if confirm not in ['Yes', 'No']:
            print(f"Please enter either 'Yes' or 'No'.")
        elif confirm == 'Yes':
            print(f"-------------------------------------------------------------")
            if Table == 'Mutations':
                View()
            elif Table == 'Species':
                View_Species()
            elif Table == 'DNA_Sequences':
                View_DNA_Sequences()
            print(f"-------------------------------------------------------------\n")
            go = False

    while run:
        if Table == 'Species':
            Primary_Key = Table + '_ID'
        else:
            Primary_Key = Table[:-1] + '_ID'

        print(f"-------------------------------------------------------------")
        Identifier = input(f'Which row would you like to edit? Enter the {Primary_Key}: ')
        print(f"-------------------------------------------------------------\n")
        rows_to_edit.append(Identifier)

        try:
            headers.remove(Primary_Key)
        except ValueError:
            pass

        trial_query = f"SELECT * FROM {Table} WHERE {Primary_Key} = {Identifier}"
        cursor.execute(trial_query)
        rows = cursor.fetchall()
        check = print_table(rows, cursor)

        if check:
            active = True
            columns = []
            values = []
            while active:
                print("----------------------------------------------------------------")
                column = input('Which column would you like to edit? ')
                if column in headers:
                    columns.append(column)
                    print('----------------------------------------------------------------')
                    value = input('What would you like the new value to be? ')
                    print('----------------------------------------------------------------\n')
                    values.append(value)
                    loop = True
                    while loop:
                        print('----------------------------------------------------------------')
                        check = input('Edit another column? (Yes/No): ')
                        if check not in ('Yes', 'No'):
                            print('Input not recognised\n----------------------------------------------------------------')
                        elif check == 'Yes':
                            print('----------------------------------------------------------------\n')
                            loop = False
                        else:
                            loop = False
                            active = False
                else:
                    print('----------------------------------------------------------------')
                    print(f'Column {column} does not exist in {Table}')
                    print('----------------------------------------------------------------\n')
            list_of_columns.append(columns)
            list_of_values.append(values)

            edit_again = True

        while edit_again:
            print('----------------------------------------------------------------')
            User_Input = input('Edit another row? (Yes/No): ')
            if User_Input not in ('Yes', 'No'):
                print('Input Not Recognised\n')
            elif User_Input == 'No':
                print('\n')
                run = False
            else:
                print('\n')
            edit_again = False

    for i in range(len(rows_to_edit)):
        print('----------------------------------------------------------------')
        print(f'Changing row, {Primary_Key} - {rows_to_edit[i]}')
        print('----------------------------------------------------------------')
        for j in range(len(list_of_columns[i])):
            print(f'Updating value of column {list_of_columns[i][j]} to {list_of_values[i][j]}\n')

    save_edits_loop = True
    while save_edits_loop:
        print('----------------------------------------------------------------')
        save_edits = input('Proceed? (Yes/No): ')
        if save_edits not in ('Yes', 'No'):
            print('Input not recognised')
        elif save_edits == 'No':
            print('No edits made')
        save_edits_loop = False

    try:
        for i in range(len(rows_to_edit)):
            set_clause = ", ".join([f"{col} = ?" for col in list_of_columns[i]])
            query = f"UPDATE {Table} SET {set_clause} WHERE {Primary_Key} = ?"
            parameters = list_of_values[i] + [rows_to_edit[i]]
            cursor.execute(query, parameters)
        connection.commit()
        print('Rows successfully updated\n\n\n')
        return True
    except sqlite3.Error as e:
        print(f"An error occurred while saving changes: {e}\n\n\n")
        return True
    
def Delete(Table):
    cursor = connection.cursor()
    rows_to_delete = []
    if Table == 'Species':
        Primary_Key = Table + '_ID'
    else:
        Primary_Key = Table[:-1] + '_ID'

    print(f"-------------------------------------------------------------")
    print(f"Would you like to check the ID(s) in {Table} before editing?")
    print(f"-------------------------------------------------------------")
    go = True
    while go:
        confirm = input(f"Check IDs (Yes/No): ")
        if confirm not in ['Yes', 'No']:
            print(f"Please enter either 'Yes' or 'No'.")
        elif confirm == 'Yes':
            print(f"-------------------------------------------------------------")
            if Table == 'Mutations':
                View()
            elif Table == 'Species':
                View_Species()
            elif Table == 'DNA_Sequences':
                View_DNA_Sequences()
            go = False
        else:
            go = False

        print(f"-------------------------------------------------------------")

    loop = True
    while loop:
        selected_row = input(f'Which entry would you like to delete? Enter the {Primary_Key}: ')
        rows_to_delete.append(selected_row)
        active = True
        while active:
            print(f"-------------------------------------------------------------")
            check = input('Would you like to delete another row? Yes/No: ')
            if check not in ('Yes', 'No'):
                print('Input not recognised')
                print(f"-------------------------------------------------------------")
            elif check == 'No':
                active = False
                loop = False
            else:
                active = False
                

    keys_to_delete = ', '.join(map(str, rows_to_delete))
    query = f"DELETE FROM {Table} WHERE {Primary_Key} IN ({', '.join(['?'] * len(rows_to_delete))})"
    parameters = rows_to_delete
    run = True
    while run:
        proceed = input(f'Deleting rows with {Primary_Key} = {keys_to_delete}. Proceed? Yes/No: ')
        if proceed not in ('Yes', 'No'):
            print('Input not recognised')
        elif proceed == 'No':
            print('Nothing deleted')
        else:
            print('Rows deleted')
            run = False

    cursor.execute(query, parameters)
    connection.commit()

def run_model(model):
    models = {
        1: Model1,
        2: Model2,
        3: Model3
    }

    format = {
        1: "Results.Model_1",
        2: "Results.Model_2",
        3: "Results.Model_3",
    }

    cursor = connection.cursor()
    initial_query = '''
                    SELECT
                        Species.Species_ID,
                        Species.Common_Name,
                        DNA_Sequences.Gene,
                    '''
    for m in model:
        initial_query += format.get(m) + ', '
    initial_query = initial_query.rstrip(', ')

    initial_query += '''
                    FROM
                        Results
                    LEFT JOIN
                        DNA_Sequences
                    ON
                        DNA_Sequences.DNA_Sequence_ID = Results.DNA_Sequence_ID
                    LEFT JOIN
                        Species
                    ON
                        Species.Species_ID = DNA_Sequences.Species_ID
                    WHERE
                        1 = 1
                    '''

    
    print(f"Current Results")
    print(f"-------------------------------------------------------------")

    cursor.execute(initial_query)
    rows = cursor.fetchall()
    if rows:
        average = 0
        list = ('', 'Average')
        for i in range(len(model)):
            average = 0
            length = 0
            for row in rows:
                if row[i+2] is None:
                    continue
                length += 1
                average += row[i+2]
            try:
                average /= length
            except ZeroDivisionError:
                average = 0
            list += (average,)
        rows.append(list)
        print_table(rows, cursor)
    else:
        print(f"No results found in the database.\n\n\n")

    query = '''SELECT
                    Species.Common_Name,
                    DNA_Sequences.Gene,
                    DNA_Sequences.DNA_Sequence_ID,
                    DNA_Sequences.DNA_Sequence
                FROM
                    DNA_Sequences
                LEFT JOIN
                    Species
                ON
                    Species.Species_ID = DNA_Sequences.Species_ID
                WHERE
                    1 = 1                
    '''
    parameters = []

    print(f"Would you like to filter which genes/species/DNA Sequences are run?")
    print(f"-------------------------------------------------------------")
    filter_choice = input(f"Filter Results (Yes/No): ")
    active = True

    while active:
        if filter_choice.lower() not in ['yes', 'no']:
            print(f"Please enter either 'Yes' or 'No'.")
            print(f"-------------------------------------------------------------")
            filter_choice = input(f"Filter Results (Yes/No): ")
        else:
            active = False

    if filter_choice.lower() == 'yes':
        criteria = filter(["Class", "Species_ID", "Common_Name", "Gene"])
        headings = ["Species.Class",
                    "Species.Species_ID",
                    "Species.Common_Name",
                    "DNA_Sequences.Gene"]

        for i in range(len(criteria)):
            if criteria[i] != '':
                pass
            else:
                query += f" AND {headings[i]} = ?"
                parameters.append(criteria[i])
            
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)
    
    rows = cursor.fetchall()
    print(f"-------------------------------------------------------------\n")
    if not rows:
        print(f"No DNA Sequences found in the Database matching those criteria.")
        return
    
    print(f"-------------------------------------------------------------")
    print(f"Running...")
    print(f"-------------------------------------------------------------")

    update_query = '''UPDATE Results
                    SET 
                    '''
    for m in model:
        update_query += f"Model_{m} = ?, "
    
    update_query = update_query.rstrip(', ')
    update_query += '''
                    WHERE
                        DNA_Sequence_ID = ?
                    '''


    for row in rows:
        results = []
        dna_sequence_id = row[2]
        dna_sequence = row[3]
        for m in model:
            result = models.get(m)(dna_sequence).get_expected_frequency()
            results.append(result)

        parameters = results + [dna_sequence_id]

        cursor.execute(update_query, parameters)

        print(f"Species: {row[0]}, Gene: {row[1]}, DNA Sequence ID: {dna_sequence_id}, Result: {results}")
    
    print(f"-------------------------------------------------------------")
    connection.commit()

        

    

        