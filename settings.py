# App execution settings
TEST = False
VERBOSE = False

# Database 
if TEST:
    DATABASE_PATH = "./test_db.json"
else:
    DATABASE_PATH = "./chess_database.json"

# Tournament details 
PLAYERS_PER_TOURNAMENT = 8
ROUNDS_PER_TOURNAMENT = 4
