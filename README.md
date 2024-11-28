# KeyPy

KeyPy est un gestionnaire de mots de passe sécurisé qui permet de stocker vos mots de passe de manière chiffrée à l'aide d'un mot de passe maître. Il utilise le chiffrement en Base64 pour protéger vos informations, et les mots de passe sont stockés dans un fichier caché dans le répertoire `NoGuys hehe, I want to make keypy safe so no.`.
KeyPy est inspiré du projet open-source KeyPass [Télécharger KeyPass](https://keepass.info/)

KEYPY ARE NOT 100% SAFE, YOU CAN MOD IT TO MAKE IT MORE SAFE!

## Fonctionnalités

- **Gestion des mots de passe** : Voir et ajouter des mots de passe pour différents sites et applications.
- **Chiffrement des mots de passe** : Les mots de passe sont chiffrés en Base64 pour garantir leur sécurité.
- **Mot de passe maître** : Un mot de passe maître est requis pour accéder aux mots de passe sauvegardés.
- **Faux temps de chargement** : Une barre de progression est affichée au lancement pour simuler le chargement des "assets".
- **Stockage sécurisé** : Les mots de passe sont stockés dans un fichier JSON caché dans le répertoire `AppData`.

## Prérequis

Avant d'exécuter KeyPy, assurez-vous d'avoir Python 3.x installé sur votre machine. Si ce n'est pas déjà fait, vous pouvez télécharger Python à partir du [site officiel de Python](https://www.python.org/downloads/).

### Bibliothèques Python requises

- `cryptography` : Pour la génération de clés et le chiffrement.
- `os` : Pour manipuler les chemins et répertoires du système.
- `base64` : Pour chiffrer et déchiffrer les mots de passe.
- `json` : Pour lire et écrire les mots de passe dans un fichier JSON.
- `time` : Pour simuler un temps de chargement.

Installez ces bibliothèques avec pip si nécessaire :

```bash
pip install cryptography
