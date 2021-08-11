from tinydb import TinyDB, Query
from chess.constants import DATABASE_PATH

def get_database_table(table, empty=False):
    db = TinyDB(DATABASE_PATH)
    table = db.table(table)
    
    if empty == True:
        # Empty tables for dev purposes 
        table.truncate()
       
    # players_table.insert_multiple()
    # db.all()

    return table