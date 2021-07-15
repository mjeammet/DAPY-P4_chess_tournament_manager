from models import PLAYERS_DATABASE, Player, Tournament


def main():
    """Main function."""
    player1 = Player("Pupo", "Marie", "1990", "F")
    player2 = Player("Gay", "Amandine", "1980", "F")
    player3 = Player('King', 'Stephen', "1947", "M")
    player1.add_to_database()
    player2.add_to_database()
    player3.add_to_database()

    tournoi = Tournament()
    tournoi.add_player(0)
    tournoi.add_player(1)
    tournoi.add_player(2)
