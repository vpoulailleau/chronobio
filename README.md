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

Il faut envoyer une ligne par action.
Chaque employé peut réaliser au maximum une action par tour.
Le gérant de l'exploitation peut réaliser au maximum une action par tour.

Les champs entre accolades sont à remplacer par leur valeurs.

- `{GÉRANT}` : numéro du gérant (0)
- `{OUVRIER}` : numéro de l'ouvrier (supérieur ou égal à 1)
- `{LÉGUME}` : un légume parmi `PATATE`, `POIREAU`, `TOMATE`, `OIGNON`, `COURGETTE`
- `{CHAMP}` : numéro du champ (de 1 à 5)

#### Acheter un champ

`{GÉRANT} ACHETER CHAMP`

Un nouveau champ est acheté, 10 000 euros est enlevé du solde.

#### Semer

`{OUVRIER} SEMER {LÉGUME} {CHAMP}`

Semer sur un champ préalablement acheté remplace la culture existante sur le champ.

#### Arroser

`{OUVRIER} ARROSER {CHAMP}`

Il faut arroser 10 fois un champ avant qu'il soit récoltable.

#### Vendre des légumes

`{GÉRANT} VENDRE {CHAMP}`

Les légumes sont vendus après récolte, la récolte dure 2 jours : le gérant ne pourra pas faire d'action au prochain tour.

Les légumes sont vendus au prix du marché, c'est à dire que la récolte est vendue pour la somme de 2 000 euros - 50 fois le nombre de champs cultivant encore la même espèce de légume.

#### Acheter un tracteur

`{GÉRANT} ACHETER TRACTEUR`

Un tracteur coute 30 000 euros.

#### Stocker des légumes

`{OUVRIER} STOCKER {CHAMP} {TRACTEUR}`

Les légumes du champ récoltable sont stockés dans l'usine de fabrication de soupe. Cela prend 5 jours de transporter tous les légumes à l'usine : pendant les 4 tours suivants l'ouvrier, le champ et le tracteur ne peuvent plus être utilisés.

Après le transport, le stock de l'usine est augmenté de 1000 pour l'espèce de légume du champ.

#### Fabriquer des soupes

`{OUVRIER} CUISINER`

Un ouvrier fabrique 100 soupes. Pour chaque soupe, il piochera dans les stocks de l'usine. Il essaiera de mettre le plus grand nombre de légumes différents dans une soupe.

La soupe est vendue :

- 1 euros la soupe de 1 légume
- 2 euros la soupe de 2 légumes
- 4 euros la soupe de 3 légumes
- 6 euros la soupe de 4 légumes
- 8 euros la soupe de 5 légumes

## Conditions de victoire ou défaite

- Une action invalide entraîne le blocage du joueur : il ne peut plus faire d'actions jusqu'à la fin du jeu.
- Un achat sans l'argent disponible entraîne le blocage du joueur.
- Un joueur ne pouvant pas payer ses dépenses est bloqué.
- Le joueur ayant le plus d'argent disponible à la fin (coût total des emprunts déduits) gagne.