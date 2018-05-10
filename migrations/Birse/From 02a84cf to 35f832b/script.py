import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "borgia.settings")
django.setup()

from decimal import Decimal
import json
import datetime
import sys

def progress_bar(value, endvalue, bar_length=40):
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        sys.stdout.write("\rProgress: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()

print("Mapping shared events\n")
from finances.models import SharedEvent
sharedevents = []
weightsusers = []
sharedevents_pk = 1
weightsusers_pk = 1
sem = SharedEvent.objects.all().count()

for se in SharedEvent.objects.all():
    progress_bar(sharedevents_pk, sem)
    for p in se.list_of_participants_ponderation():
        weightsusers.append(
            {
              "model": "finances.weightsuser",
              "pk": weightsusers_pk,
              "fields": {
                "user": p[0].pk,
                "shared_event": sharedevents_pk,
                "weights_registeration": 0,
                "weights_participation": p[1]
              }
            }
        )
        weightsusers_pk = weightsusers_pk + 1
    for p in se.list_of_registered_ponderation():
        weightsuser = False
        for w in weightsusers:
            if (w["fields"]["user"] == p[0].pk and w["fields"]["shared_event"] == sharedevents_pk):
                weightsuser = w
        if weightsuser:
            weightsusers.remove(weightsuser)
            weightsuser["fields"]["weights_registeration"] = p[1]
            weightsusers.append(weightsuser)
        else:
            weightsusers.append(
                {
                  "model": "finances.weightsuser",
                  "pk": weightsusers_pk,
                  "fields": {
                    "user": p[0].pk,
                    "shared_event": sharedevents_pk,
                    "weights_registeration": p[1],
                    "weights_participation": 0
                  }
                }
            )
            weightsusers_pk = weightsusers_pk + 1
    se_temp =  {
      "model": "finances.sharedevent",
      "pk": sharedevents_pk,
      "fields": {
        "description": se.description,
        "date": se.date.isoformat(),
        "datetime": se.datetime.isoformat(),
        "bills": se.bills,
        "done": se.done,
        "manager": se.manager.pk,
        "allow_self_registeration": True,
        "date_end_registration": se.date.isoformat(),
      }
    }
    if se.price:
        se_temp["fields"]["price"] = str(se.price)
    if se.remark:
        se_temp["fields"]["remark"] = se.remark
    sharedevents.append(se_temp)
    sharedevents_pk = sharedevents_pk + 1

print("\n", str(len(sharedevents)), ' Shared events mapped\n')

# DUMPING
print("Dumping to json ...\n")

with open('dump_' + datetime.datetime.now().isoformat() + '.json', 'w') as outfile:
    _list = sharedevents + weightsusers
    _str = json.dumps(_list,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(_str)
    outfile.close()
print("Dump completed.\n")
