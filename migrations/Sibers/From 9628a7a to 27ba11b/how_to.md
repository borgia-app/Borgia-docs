# Migration Borgia Metz Sibers

# FROM 9628a7a TO 27ba11b

## Preparation

* Clone the Borgia-docs repository
* Copy the file `script.py` into the `Borgia` folder: `cp /borgia/Borgia-docs/migrations/Sibers/From\ 9628a7a\ to\ 27ba11b/script.py /borgia/borgia/script.py`

## Dumping the database

* Enter the python environment: `source /borgia/borgiaenv/bin/activate`
* Dump the database with the script: `python3 script.py`
* Get the content type pks, if not noted during the dump :
  * Enter the Django shell: `python3 manage.py shell`
  * `from django.contrib.contenttypes.models import ContentType`
  * Save the content type pk for selfsalemodule: `ContentType.objects.get(app_label='modules', model='selfsalemodule').pk`
  * Save the content type pk for operatorsalemodule: `ContentType.objects.get(app_label='modules', model='operatorsalemodule').pk`
* Transfer the dump, for instance with SCP

## Loading the database

* Change content type pks
  * Into the new Borgia configuration
  * Enter the Django shell: `python3 manage.py shell`
  * `from django.contrib.contenttypes.models import ContentType`
  * Save the content type pk for selfsalemodule: `ContentType.objects.get(app_label='modules', model='selfsalemodule').pk`
  * Save the content type pk for operatorsalemodule: `ContentType.objects.get(app_label='modules', model='operatorsalemodule').pk`
  * Replace old content type pks with new ones, using for instance Hex Friend for MacOs or nano for Unix. Search for `"content_type": X`
* Within the Python environment, load the database: `python3 manage.py loaddata file.json`

## Finish the work

* Check the name of each product and change it if necessary
* Check the price of each product and change it if necessary
