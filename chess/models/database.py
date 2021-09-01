from tinydb import TinyDB
DATABASE_PATH = "./chess_database.json"

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

    def add_to_database(self, table_name, serialized_object):
        """Add an new object to the database.
        Arguments:
            - (str) Table name
            - (dictionary) serialized_object
        Returns:
            - (int) id of the newly added element."""
        table = self.database.table(table_name)
        table.insert(vars(serialized_object))
        return int(table.all()[-1].doc_id)

    def empty_database_table(self, table_name, force = False):
        table = self.table(table_name)

        if force == False:
            confirmation = input(f"Are you sure you want to empty {table_name} table ? ")
            if confirmation:
                return None
        else:     
            table.truncate()
            return None

    # TODO ajouter une fonction qui vérifie tous les éléments de la base de données