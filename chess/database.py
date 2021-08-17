from tinydb import TinyDB, Query
from settings import DATABASE_PATH

def get_database_table(table_name):
    db = TinyDB(DATABASE_PATH)
    table = db.table(table_name)
    return table

def empty_database_table(table_name, force = False):
    table = get_database_table(table_name)

    if force == False:
        confirmation = input(f"Are you sure you want to empty {table_name} table ? ")
        if confirmation:
            return 0
    
    table.truncate()



""" def database_verification():
    for tables:
        for object:
            for field:
                # check type
                pass """