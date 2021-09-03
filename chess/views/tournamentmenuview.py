from .baseview import BaseView


class TournamentHomeView(BaseView):

    def render(self, current_tournament):
        self.print_header("MENU DES TOURNOIS")
        if current_tournament != None:
            print(f'Current tournament : {current_tournament.name}\n')
        else:
            print('Current tournament : None\n')
        print(
            "1. Sélectionner un tournoi / changer de tournoi sélectionné.\n"            
            "2. Ajouter des joueurs au tournoi.\n"
            "3. Commencer un nouveau tour de jeu.\n"
            "4. Entrer les résultats d'un tour non terminé.\n"            
            "5. Lister les joueurs du tournoi.\n"
            "6. Lister les tours du tournoi.\n"
            "7. Lister les matchs du tournoi.\n"
            "0. Retour au menu principal.\n"
            "9. Quitter le programme."
        ) 

    def print_round_header(self):
        print("Nom\t   Date de debut\t\t Date de fin\t\t       Match 1\t\t\tMatch 2\t\t\tMatch 3\t\t\tMatch 4")

    def print_round_details(self, round):
        details = (
            f'{round.name}    '
            f'{round.start_datetime}    '
            f'{round.end_datetime}    ')
        for round in round.matchs:
            details += f'{round[0][0]} ({round[0][1]}) vs {round[1][0]} ({round[1][1]})\t'
        print(details)
        return None

    def print_match_details(self, match):
        # print(f'{match}')
        return match

    def get_match_score(self, player_id):
        inputted_score = float(input(f"Score du joueur {player_id} : "))
        # TODO add a try except to catch les petits malins qui mettent des 
        if inputted_score not in [0, 0.5, 1]:
            print(f'Score must be 0, 1 or 0.5. Cannot be {inputted_score}')
            return self.get_match_score()
        
        return inputted_score

    @staticmethod
    def print_round_ended(round):
        round_name = round.name
        end_date = round.end_datetime
        print(f'{round_name} terminé {end_date}.')
