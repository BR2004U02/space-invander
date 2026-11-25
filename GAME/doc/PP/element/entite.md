ENTITE (base de tout objet affiché)

Variable :

- position (x, y)
- hitbox (rectangle de collision, suit la position)

Constante :

- image de l'objet (chargée une seule fois au démarrage)

Application :

- classe Entite dans classes/entite.py
- la hitbox est créée à partir de l'image : même taille, même position
- afficher(screen) : dessine l'image à la position (x, y)
- le joueur, les ennemis et les balles héritent de Entite
  -> pas besoin de réécrire l'affichage ni la hitbox dans chaque classe
