<p align="center">
   <img src="./img/borgia-logo-light.png" />
</p>

# Documentation - Gestion d'un magasin

## Application

Build : [4.5.0 + ](https://github.com/borgia-app/Borgia/releases/tag/4.5.0)

Licence : [GNU GPL version 3](./license.txt)

# Introduction

Ce guide a pour objectif d'expliquer le fonctionnement de l'application de vente de Borgia.
Il détaillera la gestion des administrateurs d'un magasin, de ses produits et de ses modules de vente. Il ne s'attardera pas sur la gestion complète des stocks, qui fait l'objet d'un [autre guide](./stocks.md).

# Administrateurs du magasin

Lors de la création d'un magasin, deux groupes d'administrateurs sont également créés automatiquement, afin de gérer le magasin. Ces deux groupes sont nommés "Chefs du magasin" et "Associés du magasin". Ils n'ont pas les mêmes fonctionnalités, les mêmes permissions et ne sont pas gérés par le même groupe supérieur. Dans les deux cas, ces administrateurs peuvent accéder au "Workboard" du magasin en changeant de groupe dans le menu latéral (`Groupes / Chefs ou Associés NOM-DU-MAGASIN`).

## Chefs du magasin

Le groupe admin le plus important d'un magasin est le groupe des chefs du magasin. Le nom complet est "Chefs _NOM-DU-MAGASIN_ ".

La gestion de ce groupe est laissé par défaut aux groupe des présidents et des vice-présidents. C'est donc à eux de définir qui fait partie de ce groupe principal du magasin. Pour modifier les membres, cliquer sur `Gestion des groupes / Gestion chefs NOM_DU_MAGASIN` dans le menu latéral.

Par défaut, ce groupe a la permission de :

* Ajouter, lister et accéder aux détails des utilisateurs.
* Ajouter de l'argent à un utilisateur.
* Ajouter, modifier, lister, accéder aux détails et modifier les prix des produits (de ce magasin uniquement).
* Lister et accéder aux détails d'une vente (de ce magasin uniquement).
* Vendre des produits avec le module de vente par opérateur.
* Ajouter, lister et accéder aux détails des inventaires et des entrées de stocks (de ce magasin uniquement).
* Gérer les membres du groupe des associés de ce magasin.

L'ensemble des permissions peuvent être données à ce groupe par le(s) président(s) ou le(s) vice-président(s).

Théoriquement, ce groupe ne devrait contenir qu'un petit nombre de membres: uniquement le(s) chef(s) du magasin élu ou choisi au sein des administrateurs de celui-ci. Les autres devraient faire partie du groupe des associés.

## Associés du magasin

Ce second groupe est un cran en dessous des chefs en terme d'administration mais peuvent totalement disposer des mêmes permissions.

Ce groupe est directement gérés par le groupe des chefs du magasin. Ainsi, il est aisé d'ajouter et de supprimer des membres à ce groupe en cas de besoin (par exemple lors d'une soirée importante qui nécessite un grand nombre de collaborateurs pour la vente).

Ce groupe ne peut pas recevoir l'ensemble des permissions, mais seulement celles qui sont appliquées aux chefs du magasin. Ainsi, un associé ne peux pas obtenir une permission dont le chef du même magasin ne dispose pas lui-même. 
Par défaut, les permissions des associés sont :

* Ajouter, lister et accéder aux détails des utilisateurs.
* Ajouter de l'argent à un utilisateur.
* Ajouter, modifier, lister et accéder aux détails (de ce magasin uniquement).
* Lister et accéder aux détails d'une vente (de ce magasin uniquement).
* Vendre des produits avec le module de vente par opérateur.
* Ajouter, lister et accéder aux détails des inventaires et des entrées de stocks (de ce magasin uniquement).

# Gestion des produits

Les produits sont les éléments qui sont vendus au magasin à travers les différents modules de vente. Il convient de les utiliser correctement pour s'assurer que la gestion des stocks est cohérente et que le prix de vente correct.

## Ajouter un produit

Borgia propose deux types de produits différents pour les magasins : les produits unitaires et les produits vendus à la quantité. La différence est essentielle et fondamentale pour bien utiliser l'application des produits de Borgia.

### Produit unitaire

Un produit unitaire (aussi nommé produit tout court) est le produit de base de Borgia. L'acheteur repart avec l'intégrité du produit en une fois et il disparait physiquement du stock. Par exemple, une bouteille de bière, un écusson ou encore une blouse sont des produits basiques et unitaires.

![Ajout produit simple](./img/new_product.png)

L'ajout d'un tel produit ne nécessite qu'un nom de produit (qui sera le nom de vente).

### Produit vendu à la quantité

Un produit vendu à la quantité ne disparait pas physiquement du stock lorsqu'il est vendu. En effet, seulement une petite partie de son état est vendu à chaque fois.

Par exemple, de la bière provenant d'un fût est un produit vendu à la quantité. De même, le fromage ou le pain vendu au poids en font partie. Bien sûr, ce n'est pas limité aux produits alimentaires.

![Ajout produit vendu à la quantité](./img/new_product_quantity.png)

L'ajout d'un tel produit nécessite un nom et aussi une unité de vente : gramme ou centilitre.

### Détails d'un produit

L'ensemble des informations d'un produit est disponible en cliquant sur "détails" pour le produit concerné dans la liste des produits du magasin.

![Produit dans la liste](./img/product_in_list.png)

La page qui s'affiche indique les informations du produit ainsi que les différentes manipulations possibles à effectuer (voir la suite).

![Détails d'un produit](./img/product_retrieve.png)

## Activation / suppression

Un produit peut être désactivé ou supprimé en cas de besoin.

Lors de la désactivation, le produit :
* n'est plus visible à la vente.
* reste présent dans la liste des produits.
* peut être réactivé à tout moment, cette action **est reversible**.

Et lors de la suppression, le produit :
* disparait purement et simplement de Borgia.
* n'est plus modifiable, visible dans les listes ou disponible à la vente.
* cette action est **irreversible**.

Ainsi, la suppression d'un produit est à réserver si une erreur a été faite concernant ce produit. Si l'objectif est simplement de le retirer de la vente temporairement, la désactivation est à privilégier.

## Gestion du prix de vente

Borgia peut gérer automatiquement le prix de vente des produits en utilisant les données d'entrées et de sorties du stocks (voir la section stock pour plus d'informations). 
Le paramètre qui indique la marge de vente à appliquer est défini dans la configuration de Borgia, et est commun à tout les magasins. Ce paramètre n'est modifiable que par les personnes autorisées (par défaut le(s) président(s), le(s) vice-président(s), et le(s) trésorier(s))

De plus, il est également possible d'utiliser un prix défini manuellement pour chacun des produits en cliquant sur le bouton `Gestion manuelle du prix`.

![Gestion manuelle du prix](./img/manual_price.png)

Si c'est le cas, Borgia indique la déviation par rapport au prix qu'il calcule afin d'informer les administrateurs de la cohérence ou non du prix manuel.

![Ajout produit simple](./img/manual_price_deviant.png)

## Stock

Cette section fait l'objet d'un [guide à part entière](./stocks.md).

Notez simplement qu'un produit ne peut pas être vendu s'il n'y a pas encore eu d'entrée de stocks. Sinon le prix de vente sera nul et Borgia refusera de l'afficher dans les modules.

# Modules de ventes

L'objectif principal des produits et de l'application magasin est de vendre des choses pour l'association, par l'intermédiaire  de Borgia.

## Les deux types de modules de ventes

Afin de proposer des produits aux membres et utilisateurs du site, deux modules de vente différents sont disponibles. Les deux modules ont des contenus distinct et une fonction différente, mais leurs configurations sont similaires, et ne sont donc pas différenciées dans ce guide (voir suite).

Le premier est le module de "vente directe". Il autorise les utilisateurs à indiquer eux-même leurs achats via une interface simplifiée. Tout fonctionne **sans** l'intervention d'un administrateur du magasin et est donc basé sur la confiance entre les membres et l'association. Pour activer et configurer ce module, il faut cliquer sur "Module vente libre service" dans le menu latéral des gestionnaires du magasin.

![Module vente libre service](./img/module_selfsale.png)

Le second est un module équivalent mais disponible **uniquement pour et avec** les gestionnaires du magasin. La vente est donc approuvée par un administrateur directement. Ce module est nommé "Module vente par opérateur".

![Module vente par opérateur](./img/module_operator.png)

## Configuration

En cliquant sur le lien du module dans le menu latéral, la page de configuration s'ouvre. La section du haut indique les paramètres actuels du module, notamment s'il est activé ou non.

![Configuration du module](./img/module_config.png)

Pour modifier ces paramètres, cliquer sur le bouton "Modifier".

## Catégories de vente

La seconde section indique les produits qui sont disponibles à la vente.

Ils sont organisés par catégories que l'on peut ajouter, modifier et supprimer à la volée. Le nom de la catégorie est associée au nom affiché dans l'onglet sur l'interface utilisée par les utilisateurs.

Un produit peut être ajouté à plusieurs catégories en même temps. Si c'est un produit vendu à la quantité, il faut indiquer la quantité vendu à chaque fois. Par exemple 25 cl pour un verre, 50 pour une pinte etc.

![Sélection de la quantité dans une catégorie](./img/quantity_in_cat.png)


## Accès aux modules

Une fois activés, les modules de vente sont accessibles par les utilisateurs.

Les module de vente font l'objet d'une page de login spécifique qui doit être sélectionnée en cliquant sur le bouton vert "liens directs" sur la page de login usuelle.

![Liens directs](./img/direct_links.png)


![Modal liens directs](./img/direct_links_modal.png)

En plus de ces liens, des redirections sont disponibles dans le menu latéral. Par le groupe "Gadz'Arts" via "Vente directe _NOM-DU-MAGASIN_" et "Module vente" par les groupes des chefs et associés du magasin en question.

# Bilan de santé
