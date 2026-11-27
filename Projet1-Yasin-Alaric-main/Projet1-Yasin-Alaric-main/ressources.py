import os

# Dossier de ce projet, quel que soit le répertoire depuis lequel on lance le jeu.
BASE = os.path.dirname(os.path.abspath(__file__))


def chemin(*parties):
    """Construit le chemin absolu d'une ressource (image, son) du projet.

    Exemple : chemin("image", "bullet.png")
    """
    return os.path.join(BASE, *parties)
