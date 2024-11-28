@echo off
:: Définir le chemin du dossier contenant KeyPy.py
set KEYPY_DIR=D:\Jeux\script\Keypy

:: Ajouter ce dossier à la variable d'environnement PATH de l'utilisateur
setx PATH "%PATH%;%KEYPY_DIR%"

:: Créer un fichier .bat pour exécuter KeyPy.py avec l'alias 'keypy'
echo @echo off > "%KEYPY_DIR%\keypy.bat"
echo python "%KEYPY_DIR%\KeyPy.py" %* >> "%KEYPY_DIR%\keypy.bat"

echo "Commande 'keypy' ajoutée avec succès à l'invite de commande."
