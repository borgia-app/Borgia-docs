# Migration Borgia Lille Birse

# FROM 02a84cf TO 35f832b

## Preparation

* Clone the Borgia-docs repository
* Copy the file `script.py` into the `Borgia` folder: `cp /borgia/Borgia-docs/migrations/Birse/From 02a84cf to 35f832b/script.py /borgia/borgia/script.py`

## Dumping the database

* Enter the python environment: `source /borgia/borgiaenv/bin/activate`
* Dump useful tables with Django : `python3 manage.py dumpdata auth users shops finances.sale finances.saleproduct finances.recharging finances.paymentsolution finances.cheque finances.bankaccount finances.cheque finances.cash finances.lydiafacetoface finances.lydiaonline finances.transfert finances.exceptionnalmovement modules settings_data notifications stocks --indent 4 >> dump_useful.json`
* Dump the SharedEvent table with the script: `python3 script.py`
* Transfer the dump, for instance with SCP

## Loading the database

* Within the Python environment, load useful tables generated by dumpdata.
* Within the Python environment, load SharedEvent tables generated by the script.
