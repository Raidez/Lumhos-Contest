# Lumhos Got Talent
Concours de talent du duo de streameuses [Lumhos](https://www.twitch.tv/lumhos).
Ce projet contient plusieurs *petits* jeux fait avec la bibliothèque **Pygame** et compilé avec **cx_Freeze**.

## Lucioles
Des petites lucioles qui s'agitent devant l'écran.
En cliquant, elles s'agitent autour de la souris.

### Comment ça marche ?
1. Les lucioles sont un objet géométrique très simple => un cercle
2. Chacune possède ses propres cractéristiques aléatoire (vitesse, taille, position)
3. Chaque luciole, s'allume/s'éteint à une vitesse donnée
4. Les lucioles obtiennent aléatoirement une cible qui une fois atteinte sera répositionnée aléatoirement
5. Quand on clique, la cible des lucioles devient temporairement un cercle autour de la souris (et les lucioles restent allumées)
6. Si l'utilsateur n'as toujours pas cliqué après X secondes, un message apparait (et disparait si cliqué)
