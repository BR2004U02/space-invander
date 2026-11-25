SONS

Variable :

- aucune (les sons sont chargés une fois, puis seulement joués)

Constante :

| Son | Fichier | Volume | Joué quand |
| --- | --- | --- | --- |
| musique de fond | pvz.mp3 | 0.3 | tout le long de la partie, en boucle |
| explosion | boom2.wav | 0.1 | une balle détruit un ennemi |
| hit | roblox.wav | 0.5 | le joueur perd une vie |
| game over | gameover.wav | 0.5 | les vies tombent à 0 |

- chemins : MUSIC et SFX dans config/asset_paths.py

Application :

- classe Sons dans backend/audio.py, créée une seule fois dans le main
- _charger(nom_fichier, volume) : charge un bruitage et règle son volume
  -> ajouter un bruitage = une ligne
- stopper_musique() : coupe la musique au Game Over
- A AJOUTER pour la compétence (fichiers déjà dans assets/audio/sfx) :
    - mitrailleuse_demarrage.wav : au début de l'ouverture (0,4 s = 24 images)
    - mitrailleuse_rotation.wav : en boucle pendant le tir
    - mitrailleuse_tir.wav : à chaque balle
    - mitrailleuse_arret.wav : au début de la fermeture (0,4 s = 24 images)
