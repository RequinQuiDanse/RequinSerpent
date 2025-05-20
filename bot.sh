#!/bin/bash

# Changer de répertoire
cd /home/adam/code/RequinSerpentDpy/ || exit

# Lancer le script Python
source .env/bin/activate  # Si vous utilisez un environnement virtuel
python main.py

# Pause (attendre une entrée de l'utilisateur)
read -p "Appuyez sur une touche pour continuer..."

