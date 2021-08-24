from tinydb import TinyDB
from settings import DATABASE_PATH, VERBOSE

class Database:

    def __init__(self):
        self.database = TinyDB(DATABASE_PATH)
        self.current_tournament = None
        self.players_table = self.database.table("players")
        self.tournaments_table = self.database.table("tournaments")

    def get_db_object(self, table, object_id, serialized = True):
        """Selects a tournament, using its id """
        try:
            int(object_id)
        except:
            error_message = f"{object_id} not an integer. Can't retrieved object in database."
            print(error_message)
        serialized_object = self.database.table(table).get(doc_id = int(object_id))

        if serialized: 
            return serialized_object
        else: 
            object = unserialize_object(serialized_object, table)
            return object

    
    def add_object_to_database(self, table_name, serialized_object):
        """Add an new object to the database.
        
        return id of the newly added element."""
        table = self.database.table(table_name)
        # players_database.append(object) # relique de quand la db était une simple liste 
        # print(vars(self))
        table.insert(vars(serialized_object))
        if VERBOSE:           
            print(f'    {serialized_object} ajouté.e à la base de données.')
        return table.all()[-1].doc_id

    def empty_database_table(self, table_name, force = False):
        table = self.table(table_name)

        if force == False:
            confirmation = input(f"Are you sure you want to empty {table_name} table ? ")
            if confirmation:
                return None
        else:     
            table.truncate()
            return None



    """ def database_verification():
        for tables:
            for object:
                for field:
                    # check type
                    pass """