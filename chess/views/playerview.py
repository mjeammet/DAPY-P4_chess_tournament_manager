from .baseview import BaseView


class PlayerHomeView(BaseView):

    def render(self):
        self.print_header("MENU DES JOUEURS")
        print(
            "1. Lister les joueurs présents dans la base de données.\n"
            "2. Ajouter un joueur à la base de données.\n"
            "3. Mettre à jour les données d'un joueur.\n"
            "0. Retour au menu principal.\n"
            "9. Quitter le programme.\n"
        )

    def get_first_name(self):
        return input('Prénom :')
    
    def get_last_name(self):
        return input('Nom de famille :')

    def get_gender(self):
        return input("Genre ('F','M','X'\) :")
    
    def get_birth_date(self):
        return input('Année de naissance (format DD-MM-YYYY) :')

    def get_ranking(self):
        return input('Classement (entier positif) :')

    def print_duplicate_alert(self, inputted_data, duplicate_list):
        print(
            "Vous souhaitez ajouter:\n"
            f"      {inputted_data[0]} {inputted_data[1]} ({inputted_data[2]}), né.e le {inputted_data[3]} et classé {inputted_data[4]}.\n"
            "La base de données contient déjà une ou des entrées similaires:"
        )
        for duplicate in duplicate_list:
            print(f"      {duplicate['first_name']} {duplicate['last_name']} ({duplicate['gender']}), né.e le {duplicate['birth_date']} et classé {duplicate['ranking']}.\n")
        print(
            "Que souhaitez-vous faire ?\n"
            "1. Ecraser le joueur existant avec les nouvelles données.\n"
            "2. Ajouter quand même un nouveau joueur.\n"
            "3. Annuler l'ajout.\n"            
        )
            
    def get_player_field_to_modify(self):
        print(
            "\n"
            "1. Prénom\n"
            "2. Nom de famille.\n"
            "3. Genre\n"
            "4. Date de naissance\n"
            "5. Classement.\n"
            "0 pour annuler la modification.\n"
            ) 
        return input("Quel champ souhaitez-vous modifier ? ")

    def get_updated_info(self):
        return input("Veuillez entrer la nouvelle valeur : ")
