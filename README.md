# Chronobio

## But du jeu

- Dominer le monde ! Devenir le meilleur producteur de soupe bio, en cultivant des légumes, en fabriquant des soupes, en les vendant.
- Cultivez plusieurs sortes de légumes : pomme de terre, poireau…
- Employez des ouvriers.
- Négociez avec la banque.
- Subissez l'économie de marché.
- Attention aux aléas climatiques.
- Ne faites pas banqueroute.

## Communication

### Informations envoyées par le serveur

- Une première ligne avec le nombre de joueurs `N` (entre 1 et 6)
- Les `N` lignes suivantes, le statut de chaque joueur :
  - Le solde financier
  - Le nombre d'employés
  - Le nombre de tracteurs
  - Le nombre de champs en exploitation
  - La quantité de semance par légumes


### Actions possibles

Il faut envoyer une ligne par action. Les champs entre accolades sont à remplacer par leur valeurs.

- `{OUVRIER}` : numéro de l'ouvrier
- `{LÉGUME}` : un légume parmi `PATATE`, `POIREAU`, `TOMATE`, `OIGNON`, `COURGETTE`
- `{CHAMP}` : numéro du champ

Une action invalide entraîne le blocage du joueur : il ne peut plus faire d'actions jusqu'à la fin du jeu.

#### Semer

`{OUVRIER} SEMER {LÉGUME} {CHAMP}`