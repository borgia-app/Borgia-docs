<p align="center">
   <img src="./img/borgia-logo-light.png" />
</p>

# Documentation - Installation

Build : 5.1+
Licence : [GNU GPL version 3](https://github.com/borgia-app/Borgia/blob/master/license.txt)

# Statut : EN COURS DE MODIFICATION POUR FICHIERS DE CONFIG

# Introduction

Ce guide permet d'installer, configurer et faire fonctionner Borgia sur un serveur web en production.

L'ensemble de l'installation se fait sur un serveur sous Linux. La distribution n'est pas importante, mais le guide est écrit pour une distribution Debian, si tel n'est pas le cas certaines commandes (notamment les commandes d'installation de paquets) seront peut-être à adapter.

# Première configuration du serveur

-   L'ensemble des commandes suivantes sont à effectuer en `sudo`, sauf cas exceptionnels contraires et indiqués explicitement par la suite.

-   Il est préférable que l'ensemble du serveur soit configuré sur une machine virtuelle (VM) et non sur le serveur physique directement. Elle pourra ainsi facilement être copiée, sauvegardée ou réinitialisée.

-   Afin que le guide soit plus clair, il est décidé de travailler dans un dossier spécifique nommé `borgia-app` situé à la racine du serveur (`/borgia-app`). Il est bien évidemment possible de changer ce répertoire, les commandes devront donc être modifiées.

## Préliminaires

#### Mettre à jour le serveur :

-   `apt-get update`
-   `apt-get upgrade`

#### Supprimer Apache s'il est installé :

`apt-get purge apache2`

#### Installer des paquets nécessaires pour la suite de l'installation :

`apt-get install curl apt-transport-https`

#### Installer les packages python de base :

`apt-get install build-essential libpq-dev python-dev libjpeg-dev libssl-dev libffi-dev`

#### Installation de nginx, postgres & git :

-   `apt-get install postgresql postgresql-contrib nginx git`

#### Installation de pip pour python3 :

-   S'assurer que la commande `python3 --version` retourne une version supérieure ou égale à `3.5` (Version par défaut sur Debian 9). Si ce n'est pas le cas, réinstaller `python3`.
-   `apt-get install python3-pip`

#### Installation de Yarn (cas explicite de Debian, sinon voir [ici](https://yarnpkg.com/lang/en/docs/install/)):

-   `curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -`
-   `echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list`
-   `apt-get update && sudo apt-get install yarn`

#### Création du dossier racine de Borgia :

`mkdir /borgia-app`

## Mise en place de l'environnement virtuel Python

#### Installation de `virtualenv`

-   `pip3 install virtualenv virtualenvwrapper`
-   Dans `/borgia-app`, créer un environnement virtuel : `virtualenv borgiaenv`.
-   Si la commande virtualenv n'existe pas, faire: `ln -s /usr/local/bin/virtualenv* /usr/bin/`

#### Fonctionnement de l'environnement virtuel

-   Dans la suite du tutoriel, lorsque des commandes sont effectuées dans l'environnement virtuel il faut s'assurer d'y être. Afin d'être sûr, l'invite de commande indique le nom de l'environnement en parenthèses (ici `(borgiaenv)` par exemple).
-   Lorsque c'est demandé, la commande `source /borgia-app/borgiaenv/bin/activate` permet d'entrer dans l'environnement. Et `deactivate` pour en sortir.

## Installation et configuration de la base de données

Cette partie ne doit pas être effectuée dans l'environnement virtuel.

#### Sélectionner l'utilisateur postgres

`su - postgres`

La suite des commandes est a effectuer dans l'invite de commande postgres. `psql` permet d'activer l'invite et `\q` permet d'en sortir. Attention, toutes les commandes se terminent par un `;`.

#### Création de la base de données

**MOT_DE_PASSE_DB** est le mot de passe choisi pour se connecter à la base de données. Faites attention à le modifier dans toutes les commandes.

Dans l'invite postgres :

-   `CREATE DATABASE borgia;`
-   `CREATE USER borgiauser WITH PASSWORD 'MOT_DE_PASSE_DB';`
-   `GRANT ALL PRIVILEGES ON DATABASE borgia TO borgiauser;`

## Copie de Borgia

Dans `/borgia-app` :

-   `git clone https://github.com/borgia-app/Borgia.git`

Ensuite dans `/borgia-app/Borgia` :

-   `git checkout tags/RELEASE_A_UTILISER`
-   `git checkout -b production_RELEASE_A_UTILISER`

## Installation des paquets nécessaires à l'application

Dans `/borgia-app/Borgia` et dans l'environnement virtuel :

-   `pip3 install -r requirements/prod.txt`

Et finalement, hors de l'environnement virtuel :

-   `yarn global add less`

# Configuration du logiciel

#### Paramètres vitaux

Copier le fichier `/borgia-app/Borgia/contrib/production/settings.py` dans `/borgia-app/Borgia/borgia/borgia/settings.py` et :

-   Modifier la ligne `SECRET_KEY =` en indiquant une clé privée aléatoire. Par exemple, [ce site](https://randomkeygen.com/) permet de générer des clés, choisissez au minimum "CodeIgniter Encryption Keys", par exemple : `SECRET_KEY = 'AAHHBxi0qHiVWWk6J1bVWCMdF45p6X9t'`.

-   S'assurer que `DEBUG = False`.

-   Modifier la ligne `ALLOWED_HOSTS =` en indiquant les domaines ou sous domaines acceptés par l'application. Par exemple : `ALLOWED_HOSTS = ['sibers.borgia-app.com', 'borgia-me.ueam.net']`.

#### Base de données

Dans le fichier `/borgia-app/Borgia/borgia/borgia/settings.py`, modifier la partie :

```python
DATABASES = {
...
}
```

en indiquant le nom de la base de données, le nom de l'utilisateur et le mot de passe définis lors de la configuration de cette dernière. Par exemple :

```python
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'borgia',
       'USER': 'borgiauser',
       'PASSWORD': 'mot_de_passe',
       'HOST': 'localhost',
       'PORT': '5432',
   }
}
```

#### Serveur mail

-   Créer un compte mail Google via le site [Gmail](https://www.google.com/gmail/) et noter le nom d'utilisateur **NOM_UTILISATEUR_MAIL** et le mot de passe **MOT_DE_PASSE_MAIL**.

Dans le fichier `/borgia-app/Borgia/borgia/borgia/settings.py` :

-   Modifier les lignes `DEFAULT_FROM_EMAIL`, `SERVER_EMAIL` et `EMAIL_HOST_USER` en indiquant l'email **NOM_UTILISATEUR_MAIL**.

-   Modifier la ligne `EMAIL_HOST_PASSWORD` en indiquant le bon mot de passe **MOT_DE_PASSE_MAIL**.

#### Administrateurs

Les administrateur reçoivent des emails en cas de problèmes lors de l'utilisation de Borgia. Par exemple, si la base de données est inacessible, Borgia enverra automatiquement un mail aux administrateurs. Ces mails sont précieux et permettent de corriger des erreurs. En effet, l'interface de debug utilisée en développement n'est pas accessible ici et les mails la remplacent. Il convient d'ajouter au moins un administrateur qui va stocker les éventuels mails d'erreurs pour débuguer ensuite ou transférer à l'équipe de mainteneurs de Borgia.

Pour ajouter des administrateurs, indiquer les adresses mails dans la ligne `ADMINS =` dans le fichier `/borgia-app/Borgia/borgia/borgia/settings.py`.

# Migration de la base de données

Dans `/borgia-app/Borgia/borgia` et dans l'environnement virtuel :

-   `python3 manage.py makemigrations configurations users shops finances events modules sales stocks`
-   `python3 manage.py migrate`
-   `python3 manage.py loaddata initial`
-   `python3 manage.py collectstatic --clear` en acceptant l'alerte

Ensuite, indiquer le mot de passe du compte administrateur (qui sera désactivé par la suite) :

-   `python3 manage.py shell`,
-   `from users.models import User`,
-   `u = User.objects.get(pk=2)`,
-   `u.set_password(NEW_PASSWORD)`.
-   `u.save()`
-   `exit()`

#### Test intermédiaire

La commande dans l'environnement virtuel `python3 manage.py runserver 0.0.0.0:8000` doit lancer le serveur et ne doit pas indiquer d'erreur. Si tel est le cas, continuer vers la suite et fin du guide d'installation.

# Fin de la configuration du serveur

Le fichiers suivants existent peut être déjà dans le dossier copié. Si c'est le cas, il suffit de les modifier.

#### Installation de nginx et wsgi

Dans l'environnement virtuel :

-   `pip3 install uwsgi`

-   Copier le fichier `/borgia-app/Borgia/contrib/production/borgia.wsgi` dans `/borgia-app/Borgia/borgia`. Le modifier si vous avez changer le répertoire de base.

-   Copier le fichier `/borgia-app/Borgia/contrib/production/wsgi.py` dans `/borgia-app/Borgia/borgia/borgia` (attention au sous-dossier ici).

-   Copier le fichier `/borgia-app/Borgia/contrib/production/uwsgi_params` dans `/borgia-app/Borgia/borgia`.

-   Copier le fichier `/borgia-app/Borgia/contrib/production/borgia_nginx.conf` dans `/borgia-app/Borgia/borgia`. Modifier les chemins si nécessaire et changer le nom de serveur "SERVEUR_NAME" qui correspond au domaine utilisé (par exemple `.borgia-app.com`).

-   Activer la configuration nginx en créant un lien symbolique :

`ln -s /borgia-app/Borgia/borgia/borgia_nginx.conf /etc/nginx/sites-enabled/`

-   Redémarrer nginx :

`service nginx restart`

#### Test intermédiaire

La commande `uwsgi --socket borgia.sock --module borgia.wsgi --chmod-socket=666` doit lancer le serveur sans problème (à condition d'avoir quelques modules python installés, le virtual env ne sera utilisé qu'ensuite). Si c'est le cas, c'est bientôt terminé !

#### Suite et fin de la configuration de nginx

-   Copier le fichier `/borgia-app/Borgia/contrib/production/borgia_uwsgi.ini` dans `/borgia-app/Borgia/borgia`. Le modifier si vous avez changer le répertoire de base.

-   Ce fichier peut être testé avec la commande `uwsgi --socket borgia.sock --module borgia.wsgi --ini borgia_uwsgi.ini`

#### Mode Empereur de nginx

Ce mode permet à Nginx de gérer automatiquement et de manière dynamique le projet. La suite n'est pas à effectuer dans l'environnement virtuel.

-   `mkdir /etc/uwsgi`
-   `mkdir /etc/uwsgi/vassals`
-   `ln -s /borgia-app/Borgia/borgia/borgia_uwsgi.ini /etc/uwsgi/vassals/`

#### Démarrer uwsgi au démarrage du serveur

Dernier point, toujours en sudo en dehors de l'environnement virtuel.
Ajoutez cette ligne à la fin du fichier (avant le `exit 0`) `/etc/rc.local`:

`/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals`

Le fichier `/etc/rc.local` a donc l'allure suivante:

`#!/bin/sh -e`

`/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals`

`exit 0`

Il faut ensuite le rendre exécutable:

`chmod 755 /etc/rc.local`

#### Sauvegarde dans git

Enfin, il convient de sauvegarder l'ensemble de cette configuration sur une branche de production (sudo non nécessaire ici) :

-   `git add .`
-   `git commit -m "production"`

Il n'est pas recommandé de push cette branche car elle pourrait contenir des informations sensibles comme des clés et des mots de passe.

# Début d'utilisation / TODO : A VERIFIER AVEC 5.1+

## Création d'un utilisateur

Le compte administrateur ne doit pas être utilisé lors de la production. Il permet simplement de créer un nouvel utilisateur réel et de lui donner les bonnes permissions.

-   Ainsi, connecter vous avec le nom d'utilisateur `admin` et le mot de passe **MOT_DE_PASSE_ADMIN** défini plus haut lors de la configuration.

-   Aller sur le groupe des présidents en cliquant sur `Groupes / Présidents` dans le menu latéral.

-   Aller dans `Utilisateurs / Nouveau` dans le menu latéral pour créer un nouvel utilisateur et remplir le formulaire. L'utilisateur présent sera désigné président, il convient donc de créer le vrai compte du président de l'association.

-   Cliquer sur `Gestion des groupes / Gestion président` et ajouter le compte nouvellement créer.

-   Le compte nouveau peut maintenant se connecter et avoir accès au groupe des présidents. Il peut désactiver le compte `admin` dans la liste des utilisateurs. De même, il peut ajouter d'autres utilisateurs et les ajouter aux bons groupes.

## Création d'un magasin

L'ensemble des magasins doivent être maintenant créés. Un seul exemple sera détaillé, mais il en est de même pour les autres.

-   Cliquer sur `Magasin / Nouveau` depuis l'interface du groupe des présidents et remplir le formulaire.

-   Par défaut, personne n'est chef ou associé du nouveau magasin. Il faut donc ajouter des utilisateurs à ces groupes (au moins au groupe des chefs du magasin). Les chefs pourront ensuite gérés eux-même les associés.

## Paramètres d'utilisation

### Divers

En étant dans le groupe des présidents, aller dans le système de paramètres et modifier l'ensemble des informations qui vous semblent utiles.

### Lydia

Les deux clés publique et privée `LYDIA_API_TOKEN` & `LYDIA_VENDOR_TOKEN` permettent d'identifier le compte auprès de Lydia. Ces informations sont obtenues en contactant le support de Lydia directement après avoir ouvert un compte professionnel chez eux.

# TODO : VERIFIER ICI EN 5.1+

De même, il faut changer les deux urls `LYDIA_CALLBACK_URL` et `LYDIA_CONFIRM_URL` en modifiant la première partie qui concerne uniquement le domaine (`borgia.iresam.org` par exemple). Attention, `LYDIA_CONFIRM_URL` doit être en `http` et Borgia fera automatiquement la redirection si SSL est activé, mais `LYDIA_CALLBACK_URL` **DOIT** être en `https` si SSL est activé !
