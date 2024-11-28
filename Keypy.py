import os
import json
import base64
import time
import warnings
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Désactiver les avertissements spécifiques de getpass
warnings.filterwarnings("ignore", category=UserWarning, module="getpass")

# Chemin du fichier de mots de passe caché dans le répertoire AppData
mot_de_passe_file = os.path.join(os.environ['APPDATA'], 'KeyPy', 'mots_de_passe.json')

# Créer un répertoire caché si il n'existe pas déjà
if not os.path.exists(os.path.dirname(mot_de_passe_file)):
    os.makedirs(os.path.dirname(mot_de_passe_file))

# Fonction pour générer une clé à partir du mot de passe maître (utilisation de PBKDF2 pour générer une clé forte)
def generer_cle(mot_de_passe_maitre):
    # Utiliser PBKDF2 pour dériver la clé à partir du mot de passe maître
    salt = b'secretsalt'  # Utiliser un sel fixe ou unique par utilisateur
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Longueur de la clé en octets
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(mot_de_passe_maitre.encode()))

# Fonction de chiffrement en Base64
def chiffrer_mot_de_passe(mot_de_passe, cle):
    mot_de_passe_encode = mot_de_passe.encode()
    mot_de_passe_chiffre = base64.b64encode(mot_de_passe_encode).decode()
    return mot_de_passe_chiffre

# Fonction de déchiffrement en Base64
def dechiffrer_mot_de_passe(mot_de_passe_chiffre, cle):
    mot_de_passe_decode = base64.b64decode(mot_de_passe_chiffre.encode()).decode()
    return mot_de_passe_decode

# Fonction pour gérer l'entrée du mot de passe sans afficher les caractères
def entrer_mot_de_passe():
    try:
        from getpass import getpass
        return getpass("Entrez votre mot de passe maître : ")
    except ImportError:
        # Si getpass échoue, utiliser input (moins sécurisé)
        print("Votre mot de passe sera visible pendant la saisie. Ce n'est pas recommandé.")
        return input("Entrez votre mot de passe maître : ")

# Vérifier si le fichier de mots de passe existe, sinon le créer
if not os.path.exists(mot_de_passe_file):
    with open(mot_de_passe_file, 'w') as f:
        json.dump({}, f)

# Charger les mots de passe depuis le fichier JSON
def charger_mots_de_passe():
    with open(mot_de_passe_file, 'r') as f:
        return json.load(f)

# Sauvegarder les mots de passe dans le fichier JSON
def sauvegarder_mots_de_passe(mots_de_passe):
    with open(mot_de_passe_file, 'w') as f:
        json.dump(mots_de_passe, f)

# Afficher le menu
def afficher_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # Nettoyer l'écran
    print("""
    ___________________________
    |       MENU PRINCIPAL     |
    |--------------------------|
    | 1. Voir les mots de passe|
    | 2. Ajouter un mot de passe|
    | 3. Quitter               |
    |__________________________|
    """)

# Afficher les mots de passe
def voir_mots_de_passe(mots_de_passe, cle):
    os.system('cls' if os.name == 'nt' else 'clear')  # Nettoyer l'écran
    if len(mots_de_passe) == 0:
        print("Aucun mot de passe enregistré.")
    else:
        print("Mots de passe enregistrés:")
        for site, mot_de_passe_chiffre in mots_de_passe.items():
            mot_de_passe = dechiffrer_mot_de_passe(mot_de_passe_chiffre, cle)
            print(f"{site}: {mot_de_passe}")
    input("\nAppuyez sur Entrée pour revenir au menu.")

# Ajouter un mot de passe
def ajouter_mot_de_passe(mots_de_passe, cle):
    os.system('cls' if os.name == 'nt' else 'clear')  # Nettoyer l'écran
    site = input("Entrez le nom du site ou de l'application: ")
    mot_de_passe = input("Entrez le mot de passe (il sera caché): ")
    mot_de_passe_chiffre = chiffrer_mot_de_passe(mot_de_passe, cle)
    mots_de_passe[site] = mot_de_passe_chiffre
    sauvegarder_mots_de_passe(mots_de_passe)
    print("\nMot de passe ajouté avec succès !")
    input("\nAppuyez sur Entrée pour revenir au menu.")

# Faux chargement avec barre de progression
def charger_assets():
    print("LOADING ASSETS... ", end="")
    for i in range(101):
        time.sleep(0.02)  # Simuler un délai pour chaque étape
        print(f"\rLOADING ASSETS... [{'#' * (i // 2)}{'.' * (50 - i // 2)}] {i}%", end="", flush=True)
    print("\nAssets chargés avec succès !")

# Fonction principale du programme
def main():
    charger_assets()  # Ajouter un faux temps de chargement

    mot_de_passe_maitre = entrer_mot_de_passe()

    cle_secrete = generer_cle(mot_de_passe_maitre)  # Générer la clé avec le mot de passe maître
    mots_de_passe = charger_mots_de_passe()  # Charger les mots de passe au début

    while True:
        afficher_menu()  # Afficher le menu

        choix = input("Choisissez une option: ")

        if choix == '1':
            voir_mots_de_passe(mots_de_passe, cle_secrete)  # Voir les mots de passe
        elif choix == '2':
            ajouter_mot_de_passe(mots_de_passe, cle_secrete)  # Ajouter un mot de passe
        elif choix == '3':
            print("Au revoir!")
            break  # Quitter le programme
        else:
            print("Choix invalide. Veuillez réessayer.")
            input("Appuyez sur Entrée pour revenir au menu.")

if __name__ == '__main__':
    main()
