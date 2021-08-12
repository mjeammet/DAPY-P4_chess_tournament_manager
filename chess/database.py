from tinydb import TinyDB, Query
from chess.constants import DATABASE_PATH

def get_database_table(type, empty=False):
    db = TinyDB(DATABASE_PATH)
    table = db.table(type)
    
    if empty == True:
        # Empty tables for dev purposes 
        table.truncate()
       
    # players_table.insert_multiple()

    return table