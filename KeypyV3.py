import os
import base64
import getpass

# Définir les messages multilingues
messages = {
    'fr_FR': {
        "welcome_message": "Bienvenue dans Keypy",
        "enter_master_password": "Entrez votre mot de passe maître : ",
        "incorrect_master_password": "Mot de passe maître incorrect.",
        "reset_master_password_prompt": "Voulez-vous réinitialiser le mot de passe maître ? (O/N) : ",
        "master_password_reset_successful": "Mot de passe maître réinitialisé avec succès.",
        "incorrect_reset_code": "Code secret incorrect.",
        "enter_reset_code": "Entrez le code secret pour réinitialiser : ",
        "enter_new_master_password": "Entrez un nouveau mot de passe maître : ",
        "choose_option": "Choisissez une option : ",
        "view_passwords": "1. Voir les mots de passe enregistrés",
        "add_password": "2. Ajouter un mot de passe",
        "reset_password": "3. Réinitialiser le mot de passe maître",
        "quit": "4. Quitter",
        "saved_passwords": "Mots de passe enregistrés :",
        "password_added_successfully": "Mot de passe ajouté avec succès !",
        "no_passwords_registered": "Aucun mot de passe enregistré.",
        "press_enter_to_continue": "Appuyez sur Entrée pour revenir au menu.",
        "invalid_choice": "Choix invalide. Veuillez réessayer.",
        "goodbye": "Au revoir !",
        "resetting_master_password": "Réinitialisation du mot de passe maître",
    },
    'en_US': {
        "welcome_message": "Welcome to Keypy",
        "enter_master_password": "Enter your master password: ",
        "incorrect_master_password": "Incorrect master password.",
        "reset_master_password_prompt": "Do you want to reset the master password? (Y/N): ",
        "master_password_reset_successful": "Master password reset successful.",
        "incorrect_reset_code": "Incorrect reset code.",
        "enter_reset_code": "Enter the secret reset code: ",
        "enter_new_master_password": "Enter a new master password: ",
        "choose_option": "Choose an option: ",
        "view_passwords": "1. View saved passwords",
        "add_password": "2. Add a password",
        "reset_password": "3. Reset master password",
        "quit": "4. Quit",
        "saved_passwords": "Saved passwords:",
        "password_added_successfully": "Password added successfully!",
        "no_passwords_registered": "No passwords registered.",
        "press_enter_to_continue": "Press Enter to continue.",
        "invalid_choice": "Invalid choice. Please try again.",
        "goodbye": "Goodbye!",
        "resetting_master_password": "Resetting the master password",
    }
}

# Détecter la langue du système (fr_FR ou en_US)
import locale
lang = locale.getdefaultlocale()[0]
if lang not in messages:
    lang = 'en_US'  # Si la langue n'est pas supportée, utiliser l'anglais

# Obtenir le fichier de mot de passe maître de l'utilisateur
master_password_file = os.path.join(os.environ['APPDATA'], 'Keypy', 'master_password.txt')

# Vérifier si le fichier de mot de passe maître existe
if not os.path.exists(master_password_file):
    os.makedirs(os.path.dirname(master_password_file), exist_ok=True)
    with open(master_password_file, 'w') as f:
        f.write(base64.b64encode("root".encode('utf-8')).decode('utf-8'))  # Mot de passe par défaut

# Charger et vérifier le mot de passe maître
def charger_mot_de_passe_maitre():
    with open(master_password_file, 'r') as f:
        return base64.b64decode(f.read()).decode('utf-8')

def enregistrer_mot_de_passe_maitre(mdp):
    with open(master_password_file, 'w') as f:
        f.write(base64.b64encode(mdp.encode('utf-8')).decode('utf-8'))

# Fonction pour réinitialiser le mot de passe maître
def reinitialiser_mot_de_passe():
    print(messages[lang]["resetting_master_password"])
    code_reset = input(messages[lang]["enter_reset_code"])
    if code_reset != "0695062814":
        print(messages[lang]["incorrect_reset_code"])
        return
    new_password = getpass.getpass(messages[lang]["enter_new_master_password"])
    enregistrer_mot_de_passe_maitre(new_password)
    print(messages[lang]["master_password_reset_successful"])

# Fonction principale du programme
def main():
    # Logo ASCII
    logo = """
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |  ___  ____   | || |  _________   | || |  ____  ____  | || |   ______     | || |  ____  ____  | |
| | |_  ||_  _|  | || | |_   ___  |  | || | |_  _||_  _| | || |  |_   __ \   | || | |_  _||_  _| | |
| |   | |_/ /    | || |   | |_  \_|  | || |   \ \  / /   | || |    | |__) |  | || |   \ \  / /   | |
| |   |  __'.    | || |   |  _|  _   | || |    \ \/ /    | || |    |  ___/   | || |    \ \/ /    | |
| |  _| |  \ \_  | || |  _| |___/ |  | || |    _|  |_    | || |   _| |_      | || |    _|  |_    | |
| | |____||____| | || | |_________|  | || |   |______|   | || |  |_____|     | || |   |______|   | |
| |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
 .----------------.  .----------------.                                                             
| .--------------. || .--------------. |                                                            
| | ____   ____  | || |    ______    | |                                                            
| ||_  _| |_  _| | || |   / ____ `.  | |                                                            
| |  \ \   / /   | || |   `'  __) |  | |                                                            
| |   \ \ / /    | || |   _  |__ '.  | |                                                            
| |    \ ' /     | || |  | \____) |  | |                                                            
| |     \_/      | || |   \______.'  | |                                                            
| |              | || |              | |                                                            
| '--------------' || '--------------' |                                                            
 '----------------'  '----------------'                                                             
"""
    print(logo)

    while True:
        print(messages[lang]["welcome_message"])
        mot_de_passe_maitre = input(messages[lang]["enter_master_password"])
        
        try:
            stored_password = charger_mot_de_passe_maitre()
            if mot_de_passe_maitre != stored_password:
                print(messages[lang]["incorrect_master_password"])
                reset_choice = input(messages[lang]["reset_master_password_prompt"]).lower()
                if reset_choice == 'o' or reset_choice == 'y':
                    reinitialiser_mot_de_passe()
                continue
        except Exception as e:
            print(f"Erreur lors de la vérification du mot de passe maître : {str(e)}")
            return

        # Afficher les options
        while True:
            print(messages[lang]["choose_option"])
            print(messages[lang]["view_passwords"])
            print(messages[lang]["add_password"])
            print(messages[lang]["reset_password"])
            print(messages[lang]["quit"])
            choix = input(messages[lang]["choose_option"])

            if choix == '1':
                print(messages[lang]["saved_passwords"])
                # Afficher les mots de passe enregistrés
                # Logique pour afficher les mots de passe ici
                input(messages[lang]["press_enter_to_continue"])
            elif choix == '2':
                print(messages[lang]["password_added_successfully"])
                # Logique pour ajouter un mot de passe ici
                input(messages[lang]["press_enter_to_continue"])
            elif choix == '3':
                print(messages[lang]["master_password_reset_successful"])
                # Logique pour réinitialiser le mot de passe maître ici
                input(messages[lang]["press_enter_to_continue"])
            elif choix == '4':
                print(messages[lang]["goodbye"])
                break
            else:
                print(messages[lang]["invalid_choice"])

if __name__ == "__main__":
    main()
