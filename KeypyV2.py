import os
import json
import base64
import getpass

# Logo ASCII à afficher au démarrage
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
| | ____   ____  | || |    _____     | |                                                            
| ||_  _| |_  _| | || |   / ___ `.   | |                                                            
| |  \ \   / /   | || |  |_/___) |   | |                                                            
| |   \ \ / /    | || |   .'____.'   | |                                                            
| |    \ ' /     | || |  / /____     | |                                                            
| |     \_/      | || |  |_______|   | |                                                            
| |              | || |              | |                                                            
| '--------------' || '--------------' |                                                            
 '----------------'  '----------------'                                                             
"""

# Emplacements des fichiers de données
app_data_folder = os.path.join(os.getenv('APPDATA'), "Keypy")
if not os.path.exists(app_data_folder):
    os.makedirs(app_data_folder)

password_file = os.path.join(app_data_folder, "passwords.json")
master_password_file = os.path.join(app_data_folder, "master_password.txt")

# Code secret pour réinitialiser le mot de passe maître
SECRET_CODE = "0695062814"

# Charger ou créer les fichiers nécessaires
if not os.path.exists(password_file):
    with open(password_file, 'w') as f:
        json.dump({}, f)

if not os.path.exists(master_password_file):
    with open(master_password_file, 'w') as f:
        f.write(base64.b64encode("default_password".encode('utf-8')).decode('utf-8'))

# Fonctions utilitaires pour le chiffrement
def crypter_texte(texte):
    return base64.b64encode(texte.encode('utf-8')).decode('utf-8')

def decrypter_texte(texte_crypte):
    return base64.b64decode(texte_crypte.encode('utf-8')).decode('utf-8')

# Gestion des mots de passe
def charger_mots_de_passe():
    with open(password_file, 'r') as f:
        try:
            mots_de_passe = json.load(f)
            for site, (pseudo, mot_de_passe) in mots_de_passe.items():
                try:
                    # Vérifier la validité des mots de passe
                    base64.b64decode(mot_de_passe)
                except base64.binascii.Error:
                    print(f"Erreur : Mot de passe pour {site} corrompu. Réinitialisation.")
                    mots_de_passe[site] = (pseudo, crypter_texte("motdepasse_invalide"))
            return mots_de_passe
        except json.JSONDecodeError:
            print("Erreur : fichier JSON corrompu. Réinitialisation.")
            return {}

def sauvegarder_mots_de_passe(mots_de_passe):
    with open(password_file, 'w') as f:
        json.dump(mots_de_passe, f)

# Fonctions du programme
def afficher_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)  # Affichage du logo ASCII
    print("""
    Bienvenue dans Keypy
    1. Voir les mots de passe
    2. Ajouter un mot de passe
    3. Quitter
    """)

def voir_mots_de_passe(mots_de_passe):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Mots de passe enregistrés :")
    for site, (pseudo, mot_de_passe) in mots_de_passe.items():
        try:
            mot_de_passe_decrypte = decrypter_texte(mot_de_passe)
        except (base64.binascii.Error, ValueError):
            mot_de_passe_decrypte = "motdepasse_invalide"
        print(f"{site} - Utilisateur : {pseudo}, Mot de passe : {mot_de_passe_decrypte}")
    input("\nAppuyez sur Entrée pour revenir au menu.")

def ajouter_mot_de_passe(mots_de_passe):
    os.system('cls' if os.name == 'nt' else 'clear')
    site = input("Entrez le nom du site ou de l'application : ")
    pseudo = input("Entrez le pseudo ou l'utilisateur : ")
    mot_de_passe = input("Entrez le mot de passe : ")
    mots_de_passe[site] = (pseudo, crypter_texte(mot_de_passe))
    sauvegarder_mots_de_passe(mots_de_passe)
    print("\nMot de passe ajouté avec succès !")
    input("\nAppuyez sur Entrée pour revenir au menu.")

def verifier_mot_de_passe(maitre_crypte, mot_de_passe_saisi):
    try:
        mot_de_passe_decrypte = decrypter_texte(maitre_crypte)
        return mot_de_passe_decrypte == mot_de_passe_saisi
    except (base64.binascii.Error, ValueError):
        return False

def reinitialiser_mot_de_passe():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Réinitialisation du mot de passe maître")
    
    code_secret = input("Entrez le code secret : ")
    
    if code_secret == SECRET_CODE:
        nouveau_mdp = getpass.getpass("Entrez le nouveau mot de passe maître : ")
        confirmer_mdp = getpass.getpass("Confirmez le nouveau mot de passe maître : ")
        if nouveau_mdp == confirmer_mdp:
            with open(master_password_file, 'w') as f:
                f.write(crypter_texte(nouveau_mdp))
            print("\nMot de passe maître réinitialisé avec succès !")
        else:
            print("\nLes mots de passe ne correspondent pas.")
    else:
        print("\nCode secret incorrect.")
    input("\nAppuyez sur Entrée pour revenir.")

# Fonction principale
def main():
    with open(master_password_file, 'r') as f:
        mot_de_passe_maitre_crypte = f.read().strip()

    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)  # Affichage du logo ASCII
    mot_de_passe_maitre = getpass.getpass("Entrez votre mot de passe maître : ")

    if not verifier_mot_de_passe(mot_de_passe_maitre_crypte, mot_de_passe_maitre):
        print("\nMot de passe maître incorrect.")
        reinitialiser_choix = input("Voulez-vous réinitialiser le mot de passe maître ? (O/N) : ")
        if reinitialiser_choix.lower() == 'o':
            reinitialiser_mot_de_passe()
        else:
            print("Le mot de passe maître est incorrect. Fin du programme.")
        return

    mots_de_passe = charger_mots_de_passe()

    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")

        if choix == '1':
            voir_mots_de_passe(mots_de_passe)
        elif choix == '2':
            ajouter_mot_de_passe(mots_de_passe)
        elif choix == '3':
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")
            input("\nAppuyez sur Entrée pour revenir au menu.")

if __name__ == '__main__':
    main()
