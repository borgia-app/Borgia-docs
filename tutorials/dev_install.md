<p align="center">
   <img src="./img/borgia-logo-light.png" />
</p>

# Documentation - Installation

Build : 5.1+
Licence : [GNU GPL version 3](https://github.com/borgia-app/Borgia/blob/master/license.txt)

# Introduction

Ce guide permet d'installer, configurer et faire fonctionner Borgia en local pour le developpement.

L'ensemble de ce qui suit est indépendant du système d'exploitation utilisé. Il fonctionne sous Windows, MacOS et Linux.

Attention, si Python 2 et 3 cohabitent, python 3 sera appelé avec `python3`. Dans tous les cas, vérifiez que c'est bien Python 3 qui est utilisé pour les commandes suivantes, en faisant : `python --version` ou `python3 --version`. Pareil pour `pip` et `pip3` si nécessaire.

# Installation des dépendances

-   Packages Python : `pip install -r requirements/dev.txt`
-   Less : `yarn global add less` ou `npm install -g less`

# Configuration `settings.py`

-   Copier / coller le fichier `settings.py` se trouvant dans `/contrib/development` dans `/borgia/borgia`.
-   Modifier l'ensemble des variables qui le doivent en parcourant le fichier.
-   Dans le cas de la configuration d'un email Gmail, avec comme email `GMAIL_EMAIL` et mot de passe `GMAIL_PASSWORD`, utiliser :

```python
DEFAULT_FROM_EMAIL = 'GMAIL_EMAIL'
SERVER_EMAIL = 'GMAIL_EMAIL'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'GMAIL_EMAIL'
EMAIL_HOST_PASSWORD = 'GMAIL_PASSWORD'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

-   Ne pas oublier de configurer Gmail pour accepter les "applications moins sécurisées".

# Migrations et données initiales

Les commandes qui suivent sont à exécuter dans le dossier d'application `/borgia`.

-   `python manage.py makemigrations configurations users shops finances events modules sales stocks`,
-   `python manage.py migrate`,
-   `python manage.py loaddata initial`.
-   `python manage.py collectstatic --clear` en indiquant "yes" à la validation.

Données initiales pour simulation et développement.

-   `python manage.py loaddata tests_data`

Modification du mot de passe du premier utilisateur `1Me215`:

-   `python manage.py shell`,
-   `from users.models import User`,
-   `u = User.objects.get(pk=2)`,
-   `u.set_password(NEW_PASSWORD)`.
-   `u.save()`
-   `exit()`

# Tests

Les tests unitaires sont exécutés par `python manage.py test` ou `python manage.py test NOM_APPLICATION` pour tester une application en particulier.

Ils doivent être exécutés, sans erreurs avant chaque push.
