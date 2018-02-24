<p align="center">
   <img src="./img/borgia-logo-light.png" />
</p>

# Documentation - Installation

## Application

Build : [4.5.0 + ](https://github.com/borgia-app/Borgia/releases/tag/4.5.0)

Licence : [GNU GPL version 3](./license.txt)

# Introduction

Ce guide permet d'installer, configurer et faire fonctionner Borgia sur un serveur web.

L'ensemble de l'installation se fait sur un serveur sous Linux. La distribution n'est pas importante, mais le guide est écrit pour une distribution Debian, si tel n'est pas le cas certaines commandes (notamment les commandes d'installation de paquets) seront peut-être à adapter.

# Première configuration du serveur

* L'ensemble des commandes suivantes sont à effectuer en `sudo`, sauf cas exceptionnels contraires et indiqués explicitement par la suite.

* Il est préférable que l'ensemble du serveur soit configuré sur une machine virtuelle (VM) et non sur le serveur physique directement. Elle pourra ainsi facilement être copiée, sauvegardée ou réinitialisée.

* Afin que le guide soit plus clair, il est décidé de travailler dans un dossier spécifique nommé `borgia-app` situé à la racine du serveur (`/borgia-app`). Il est bien évidemment possible de changer ce répertoire, les commandes devront donc être modifiées.

## Préliminaires

#### Mettre à jour le serveur :

* `apt-get update`
* `apt-get upgrade`
* `apt-get dist-upgrade`

#### Supprimer Apache s'il est installé :

`apt-get purge apache2`

#### Installer les packages python de base :

`apt-get install build-essential libpq-dev python-dev libjpeg-dev`

#### Installation de nginx, postgres & git :

* `apt-get install postgresql postgresql-contrib nginx git`

#### Installation de pip pour python3 :

* S'assurer que la commande `python3 --version` retourne une version supérieure ou égale à `3.6`. Si ce n'est pas le cas, réinstaller `python3`.
* `apt-get install python3-pip`

#### Installation de Yarn (cas explicite de Debian, sinon voir [ici](https://yarnpkg.com/lang/en/docs/install/)):

* `curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -`
* `echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list`
* `apt-get update && sudo apt-get install yarn`

#### Création du dossier racine de Borgia :

`mkdir /borgia-app`

## Mise en place de l'environnement virtuel Python

#### Installation de `virtualenv`

* `pip3 install virtualenv virtualenvwrapper`
* Dans `/borgia-app`, créer un environnement virtuel : `virtualenv borgiaenv`.

#### Fonctionnement de l'environnement virtuel

* Dans la suite du tutoriel, lorsque des commandes sont effectuées dans l'environnement virtuel il faut s'assurer d'y être. Afin d'être sûr, l'invite de commande indique le nom de l'environnement en parenthèses (ici `(borgiaenv)` par exemple).
* Lorsque c'est demandé, la commande `source /borgia-app/borgiaenv/bin/activate` permet d'entrer dans l'environnement. Et `deactivate` pour en sortir.

## Installation et configuration de la base de données

Cette partie ne doit pas être effectuée dans l'environnement virtuel.

#### Sélectionner l'utilisateur postgres

`su - postgres`

La suite des commandes est a effectuer dans l'invite de commande postgres. `psql` permet d'activer l'invite et `\q` permet d'en sortir. Attention, toutes les commandes se terminent par un `;`.

#### Création de la base de données

**MOT_DE_PASSE_DB** est le mot de passe choisi pour se connecter à la base de données. Faites attention à le modifier dans toutes les commandes.

Dans l'invite postgres :

* `CREATE DATABASE borgia;`
* `CREATE USER borgiauser WITH PASSWORD 'MOT_DE_PASSE_DB';`
* `GRANT ALL PRIVILEGES ON DATABASE borgia TO borgiauser;`

## Copie de Borgia

La liste des versions de Borgia est disponible [ici](https://github.com/borgia-app/Borgia/tags). Ce guide est destiné aux versions supérieures à 4.5.0. Ici par exemple, la version 4.5.0 est choisie et installée.

Dans `/borgia-app` :

* `git clone git@github.com:borgia-app/Borgia.git`
* `git checkout tags/4.5.0`

## Installation des paquets nécessaires à l'application

Dans `/borgia-app/Borgia` et dans l'environnement virtuel :

* `pip3 install -r requirements.txt`

Et finalement, hors de l'environnement virtuel :

* `yarn global add less`

# Configuration du logiciel

#### Paramètres vitaux

Dans le fichier `/borgia-app/Borgia/borgia/settings.py` :

* Modifier la ligne `SECRET_KEY = 'need to be changed'` en indiquant une clé privée aléatoire. Par exemple, [ce site](JPMGCpIqzP) permet de générer des clés, choisissez au minimum "CodeIgniter Encryption Keys", par exemple : `SECRET_KEY = 'AAHHBxi0qHiVWWk6J1bVWCMdF45p6X9t'`.

* Modifier la ligne `DEBUG = True` en `DEBUG = False`.

* Modifier la ligne `ALLOWED_HOSTS = ['*']` en indiquant les domaines ou sous domaines acceptés par l'application. Par exemple : `ALLOWED_HOSTS = ['www.borgia.iresam.org', 'borgia.iresam.org']`.

#### Base de données

Dans le fichier `/borgia-app/Borgia/borgia/settings.py`, changer la partie :
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
en (où **MOT_DE_PASSE_DB** a été indiqué lors de la configuragion de la base de données) :

```
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'borgia',
       'USER': 'borgiauser',
       'PASSWORD': 'MOT_DE_PASSE_DB',
       'HOST': 'localhost',
       'PORT': '5432',
   }
}
```

#### Serveur mail

* Créer un compte mail Google via le site [Gmail](https://www.google.com/gmail/) et noter le nom d'utilisateur **NOM_UTILISATEUR_MAIL** et le mot de passe **MOT_DE_PASSE_MAIL**.

Dans le fichier `/borgia-app/Borgia/borgia/settings.py` :

* Modifier les lignes `DEFAULT_FROM_EMAIL`, `SERVER_EMAIL` et `EMAIL_HOST_USER` en remplaçant `ae.ensam.assoc@gmail.com` par **NOM_UTILISATEUR_MAIL**.

* Modifier la ligne `EMAIL_HOST_PASSWORD` en indiquant le bon mot de passe **MOT_DE_PASSE_MAIL**.

#### Administrateurs

Les administrateur reçoivent des emails en cas de problèmes lors de l'utilisation de Borgia. Par exemple, si la base de données est inacessible, Borgia enverra automatiquement un mail aux administrateurs. Ces mails sont précieux et permettent de corriger des erreurs. Il convient d'ajouter au moins un administrateur qui va stocker les éventuels mails d'erreurs pour débuguer ensuite ou transférer à l'équipe de mainteneurs de Borgia-app.

Pour ajouter des administrateurs, indiquer les adresses mails dans la ligne `ADMINS = []`  dans le fichier `/borgia-app/Borgia/borgia/settings.py`.

#### Paramètres d'utilisation

##### Divers

Toujours dans le fichier `/borgia-app/Borgia/borgia/settings.py`, modifier les lignes dans le dictionnaire `SETTINGS_DEFAULT`. Il faut modifier à chaque fois uniquement la quatrième valeur du tuple `(val1, val2, val3, VAL4_A_MODIFIER)`. Il faut de même respecter le type de valeur définie par la valeur 3 ("f" indique un nombre décimal à deux décimales, "i" un entier, "s" du texte, "b" un booléen), même si l'ensemble des valeurs doivent être entrées en texte (ainsi on écrira `'1.00'` et non `1.00`).

Les paramètres sont :

* `CENTER_NAME`: nom du centre Borgia (texte).
* `MARGIN_PROFIT`: Marge (%) à appliquer sur le prix des produits calculés automatiquement (décimal 2 décimales).
* `LYDIA_MIN_PRICE`: Valeur minimale (€) de rechargement en automatique par Lydia (décimal 2 décimales).
* `LYDIA_MAX_PRICE`: Valeur maximale (€) de rechargement en automatique par Lydia (décimal 2 décimales).
* `LYDIA_API_TOKEN`: Clé API (privée) (texte), détails dans la section suivante.
* `LYDIA_VENDOR_TOKEN`: Clé vendeur (publique) (texte), détails dans la section suivante.
* `BALANCE_THRESHOLD_MAIL_ALERT`: Valeur seuil (€) en dessous de laquelle (strictement) l'alerte par email est activée (décimal 2 décimales), expérimental uniquement.
* `BALANCE_FREQUENCY_MAIL_ALERT`: Fréquence (jours) à laquelle l'alerte mail est envoyée si le solde est inférieur à la valeur seuil (entier), expérimental uniquement.
* `BALANCE_THRESHOLD_PURCHASE`: Valeur seuil (€) en dessous de laquelle (strictement) la commande est impossible (décimal 2 décimales).

##### Lydia

Les deux clés publique et privée `LYDIA_API_TOKEN` & `LYDIA_VENDOR_TOKEN` permettent d'identifier le compte auprès de Lydia. Ces informations sont obtenues en contactant le support de Lydia directement après avoir ouvert un compte professionnel chez eux.

De même, il faut changer les deux urls `LYDIA_CALLBACK_URL` et `LYDIA_CONFIRM_URL` en modifiant la première partie qui concerne uniquement le domaine (`borgia.iresam.org` par exemple). Attention, `LYDIA_CONFIRM_URL` doit être en `http` et Borgia fera automatiquement la redirection si SSL est activé, mais `LYDIA_CALLBACK_URL` **DOIT** être en `https` si SSL est activé !

# Migration de la base de données

Dans `/borgia-app/Borgia` et dans l'environnement virtuel :

* `python3 manage.py makemigrations users shops finances modules settings_data notifications stocks`
* `python3 manage.py migrate`
* `python3 manage.py loaddata initial`
* `python3 manage.py loaddata first_member`
* `python3 manage.py collectstatic --clear` en acceptant l'alerte

Ensuite, indiquer le mot de passe du compte administrateur (qui sera désactivé par la suite) :

* `python manage.py shell`
* `from users.models import User`
* `u = User.objects.get(pk=2)`
* `u.set_password('MOT_DE_PASSE_ADMIN')`
* `u.save()`

#### Test intermédiaire

La commande dans l'environnement virtuel `python3 manage.py runserver 0.0.0.0:8000` doit lancer le serveur et ne doit pas indiquer d'erreur. Si tel est le cas, continuer vers la suite et fin du guide d'installation.

# Fin de la configuration du serveur

Le fichiers suivants existent peut être déjà dans le dossier copié. Si c'est le cas, il suffit de les modifier.

#### Installation de nginx et wsgi

Dans l'environnement virtuel :

* `pip3 install uwsgi`

* Créer un fichier `borgia.wsgi` dans `/borgia-app/Borgia` :

```
[uwgi]
socket = :8000
chdir = /borgia-app/Borgia
wsgi-file = borgia/wsgi.py
```

* Créer un fichier `wsgi.py` dans `/borgia-app/Borgia/borgia` :

```
#-*- coding: utf-8 -*-
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "borgia.settings")

application = get_wsgi_application()
```

* Créer un fichier `uwsgi_params` dans `/borgia-app/Borgia` :

```
uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;

uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;

uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;
```

* Créer un fichier `borgia_nginx.conf` dans `/borgia-app/Borgia` en modifiant le nom du serveur `SERVEUR_NAME` (par exemple `.iresam.org`) :

```
upstream django {
    server unix:///borgia-app/Borgia/borgia.sock;
}

# configuration of the server
server {
    listen      80;
    server_name SERVEUR_NAME;
    charset     utf-8;

    client_max_body_size 75M;

    location /media  {
        alias /borgia-app/Borgia/static/media;
    }

    location /static {
        alias /borgia-app/Borgia/static/static_root;
    }

    location / {
        uwsgi_pass  django;
        include /borgia-app/Borgia/uwsgi_params;
    }
}
```

* Activer la configuration nginx en créant un lien symbolique :

`ln -s /borgia-app/Borgia/borgia_nginx.conf /etc/nginx/sites-enabled/`

* Redémarrer nginx :

`service nginx restart`

#### Test intermédiaire

La commande `uwsgi --socket mysite.sock --module borgia.wsgi --chmod-socket=666` doit lancer le serveur sans problème. Si c'est le cas, c'est bientôt terminé !

#### Suite et fin de la configuration de nginx

* Créer un fichier `borgia_uwsgi.ini` dans `/borgia-app/Borgia` :

```
[uwsgi]

chdir           = /borgia-app/Borgia
module          = borgia.wsgi
home            = /borgia-app/borgiaenv

master          = true
processes       = 10
socket          = /borgia-app/Borgia/borgia.sock
chmod-socket    = 666
vacuum          = true
```

* Ce fichier peut être testé avec la commande `uwsgi --ini mysite_uwsgi.ini`

#### Mode Empereur de nginx

Ce mode permet à Nginx de gérer automatiquement et de manière dynamique le projet. La suite n'est pas à effectuer dans l'environnement virtuel.

* `mkdir /etc/uwsgi`
* `mkdir /etc/uwsgi/vassals`
* `ln -s /borgia-app/Borgia/borgia_uwsgi.ini /etc/uwsgi/vassals/`

#### Démarrer uwsgi au démarrage du serveur

Dernier point, toujours en sudo en dehors de l'environnement virtuel.
Ajoutez cette ligne à la fin du fichier (avant le `exit 0`) `/etc/rc.local`:

`/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals`

#### Sauvegarde dans git

Enfin, il convient de sauvegarder l'ensemble de cette configuration sur une branche de production (sudo non nécessaire ici) :

* `git checkout -b production`
* `git add .`
* `git commit -m "production"`

# Début d'utilisation

## Création d'un utilisateur

Le compte administrateur ne doit pas être utilisé lors de la production. Il permet simplement de créer un nouvel utilisateur réel et de lui donner les bonnes permissions.

* Ainsi, connecter vous avec le nom d'utilisateur `admin` et le mot de passe **MOT_DE_PASSE_ADMIN** défini plus haut lors de la configuration.

* Aller sur le groupe des présidents en cliquant sur `Groupes / Présidents` dans le menu latéral.

* Aller dans `Utilisateurs / Nouveau` dans le menu latéral pour créer un nouvel utilisateur et remplir le formulaire. L'utilisateur présent sera désigné président, il convient donc de créer le vrai compte du président de l'association.

* Cliquer sur `Gestion des groupes / Gestion président` et ajouter le compte nouvellement créer.

* Le compte nouveau peut maintenant se connecter et avoir accès au groupe des présidents. Il peut désactiver le compte `admin` dans la liste des utilisateurs. De même, il peut ajouter d'autres utilisateurs et les ajouter aux bons groupes.

## Création d'un magasin

L'ensemble des magasins doivent être maintenant créés. Un seul exemple sera détaillé, mais il en est de même pour les autres.

* Cliquer sur `Magasin / Nouveau` depuis l'interface du groupe des présidents et remplir le formulaire.

* Par défaut, personne n'est chef ou associé du nouveau magasin. Il faut donc ajouter des utilisateurs à ces groupes (au moins au groupe des chefs du magasin). Les chefs pourront ensuite gérés eux-même les associés.
