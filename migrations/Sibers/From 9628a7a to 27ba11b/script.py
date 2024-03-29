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

# USERS MODELS
from users.models import ExtendedPermission, User

# User
print("Mapping users\n")
users = []
um = User.objects.all().count()
uc = 1
for u in User.objects.all():
    progress_bar(uc, um)
    uc = uc + 1
    users.append(
        {
            "model": "users.user",
            "pk": u.pk,
            "fields": {
                "password": u.password,
                "last_login": None,
                "is_superuser": False,
                "username": u.username,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email,
                "is_staff": False,
                "is_active": u.is_active,
                "date_joined": u.date_joined.isoformat(),
                "surname": u.surname,
                "family": u.family,
                "balance": str(u.balance),
                "year": u.year,
                "campus": u.campus,
                "phone": u.phone,
                "token_id": "",
                "avatar": "",
                "theme": "light",
                "groups": [g.pk for g in u.groups.filter(pk__in=[1,2,3,4,5,6])]
            }
        }
    )
print("\n", str(len(users)), " Users mapped\n")


# SHOPS MODELS & MODULES MODELS
from shops.models import Shop, ProductBase

# Shop, SelfSaleModule, OperatorSaleModule
print("Mapping shops, selfsalemodules & operatorsalemodules\n")
shops = []
selfsalemodules = []
operatorsalemodules = []
modules_pk = 1
sm = Shop.objects.all().count()
sc = 1
for s in Shop.objects.all():
    progress_bar(sc, sm)
    sc = sc + 1
    shops.append(
        {
            "model": "shops.shop",
            "pk": s.pk,
            "fields": {
                "name": s.name,
                "description": s.description,
                "color": s.color
            }
        }
    )
    if s.pk != 1:
        selfsalemodules.append(
            {
                "model": "modules.selfsalemodule",
                "pk": modules_pk,
                "fields": {
                    "state": False,
                    "shop": s.pk,
                    "delay_post_purchase": None,
                    "limit_purchase": None,
                    "logout_post_purchase": False
                }
            }
        )
        operatorsalemodules.append(
            {
                "model": "modules.operatorsalemodule",
                "pk": modules_pk,
                "fields": {
                    "state": False,
                    "shop": s.pk,
                    "delay_post_purchase": None,
                    "limit_purchase": None,
                    "logout_post_purchase": False
                }
            }
        )
        modules_pk = modules_pk + 1
print("\n", str(len(shops)), " Shops, SelfSaleModules & OperatorSaleModules mapped\n")

# Product
print("Mapping products\n")
products = []
products_pk = 1
pm = ProductBase.objects.all().count()
for pb in ProductBase.objects.all():
    progress_bar(products_pk, pm)

    # Second product, no container for 73
    if (pb.pk in [73, 90, 67]):
        products.append({
            "model": "shops.product",
            "pk": products_pk,
            "fields": {
                "name": pb.name,
                "is_manual": True,
                "manual_price": str(pb.get_moded_usual_price()),
                "shop": pb.shop.pk,
                "is_active": True,
                "is_removed": False,
                "unit": None,
                "correcting_factor": "1"
            }
        })
        products_pk = products_pk + 1

    if pb.product_unit:
        if pb.product_unit.unit == "CL":
            products.append(
                {
                    "model": "shops.product",
                    "pk": products_pk,
                    "fields": {
                        "name": pb.name,
                        "is_manual": True,
                        "manual_price": str((pb.get_moded_usual_price() * 100) / pb.product_unit.usual_quantity()),
                        "shop": pb.shop.pk,
                        "is_active": True,
                        "is_removed": False,
                        "unit": "CL",
                        "correcting_factor": "1"
                    }
                }
            )
            #print("CL", pb.pk,
            #pb.name.encode('ascii', 'ignore').decode('ascii'), str((pb.get_moded_usual_price() * 100) / pb.product_unit.usual_quantity()))
        elif pb.product_unit.unit == "G":
            products.append(
                {
                    "model": "shops.product",
                    "pk": products_pk,
                    "fields": {
                        "name": pb.name,
                        "is_manual": True,
                        "manual_price": str((pb.get_moded_usual_price() * 1000) / pb.product_unit.usual_quantity()),
                        "shop": pb.shop.pk,
                        "is_active": True,
                        "is_removed": False,
                        "unit": "G",
                        "correcting_factor": "1"
                    }
                }
            )
            #print("G", pb.pk, pb.name.encode('ascii', 'ignore').decode('ascii'), str((pb.get_moded_usual_price() * 1000) / pb.product_unit.usual_quantity()))
    else:
        products.append({
            "model": "shops.product",
            "pk": products_pk,
            "fields": {
                "name": pb.name,
                "is_manual": True,
                "manual_price": str(pb.get_moded_usual_price()),
                "shop": pb.shop.pk,
                "is_active": True,
                "is_removed": False,
                "unit": None,
                "correcting_factor": "1"
            }
        })
        #print("None", pb.pk, pb.name.encode('ascii', 'ignore').decode('ascii'), str(pb.get_moded_usual_price()))
    products_pk = products_pk + 1
print("\n", str(len(products)), " Products mapped\n")

# FINANCES MODELS

# ExceptionnalMovement

from finances.models import Sale
print("Mapping exceptionnal movements\n")
exceptionnal_movements = []
exceptionnal_movements_pk = 1
emm = Sale.objects.filter(category="exceptionnal_movement").count()
for s in Sale.objects.filter(category="exceptionnal_movement"):
    progress_bar(exceptionnal_movements_pk, emm)
    exceptionnal_movements.append(
        {
            "model": "finances.exceptionnalmovement",
            "pk": exceptionnal_movements_pk,
            "fields": {
                "datetime": s.date.isoformat(),
                "justification": s.justification,
                "operator": s.operator.pk,
                "recipient": s.sender.pk,
                "amount": str(s.amount),
                "is_credit": s.is_credit
            }
        }
    )
    exceptionnal_movements_pk = exceptionnal_movements_pk + 1
print("\n", len(exceptionnal_movements), ' ExceptionnalMovements mapped\n')

# Transfer

print("Mapping transfers\n")
transferts = []
transferts_pk = 1
tm = Sale.objects.filter(category = 'transfert').count()
for s in Sale.objects.filter(category = 'transfert'):
    progress_bar(transferts_pk, tm)
    transferts.append(
        {
            "model": "finances.transfert",
            "pk": transferts_pk,
            "fields": {
                "datetime": s.date.isoformat(),
                "justification": s.justification,
                "sender": s.sender.pk,
                "recipient": s.recipient.pk,
                "amount": str(s.amount),
            }
        }
    )
    transferts_pk = transferts_pk + 1
print("\n", str(len(transferts)) + " Transfers mapped\n")

# Recharging
print("Mapping rechargings\n")
rechargings = []
payment_solutions = []
lydias_online = []
lydias_facetoface = []
cashs = []
cheques = []
bank_accounts = []
rechargings_pk = 1
bank_accounts_pk = 1

rm = Sale.objects.filter(category = 'recharging').count()

for s in Sale.objects.filter(category = 'recharging'):
    progress_bar(rechargings_pk, rm)
    if s.wording == "Rechargement automatique":
        if s.payment.unique_payment_type() == 'lydia_auto':
            lydias_online.append(
                {
                    "model": "finances.lydiaonline",
                    "pk": rechargings_pk,
                    "fields": {
                        "date_operation": s.date.isoformat().split("T")[0],
                        "id_from_lydia": s.payment.list_lydia()[0][0].id_from_lydia,
                        "banked": False,
                        "date_banked": None
                    }
                }
            )
            payment_solutions.append(
                {
                    "model": "finances.paymentsolution",
                    "pk": rechargings_pk,
                    "fields": {
                        "sender": s.sender.pk,
                        "recipient": s.recipient.pk,
                        "amount": str(s.amount)
                    }
                }
            )
            rechargings.append(
                {
                    "model": "finances.recharging",
                    "pk": rechargings_pk,
                    "fields": {
                        "datetime": s.date.isoformat(),
                        "sender": s.sender.pk,
                        "operator": s.operator.pk,
                        "payment_solution": rechargings_pk
                    }
                }
            )
            rechargings_pk = rechargings_pk + 1
    elif s.wording == "Rechargement manuel":
        if s.payment.unique_payment_type() == 'cash':
            cashs.append(
                {
                    "model": "finances.cash",
                    "pk": rechargings_pk,
                    "fields": {}
                }
            )
            payment_solutions.append(
                {
                    "model": "finances.paymentsolution",
                    "pk": rechargings_pk,
                    "fields": {
                        "sender": s.sender.pk,
                        "recipient": s.recipient.pk,
                        "amount": str(s.amount)
                    }
                }
            )
            rechargings.append(
                {
                    "model": "finances.recharging",
                    "pk": rechargings_pk,
                    "fields": {
                        "datetime": s.date.isoformat(),
                        "sender": s.sender.pk,
                        "operator": s.operator.pk,
                        "payment_solution": rechargings_pk
                    }
                }
            )
            rechargings_pk = rechargings_pk + 1
        elif s.payment.unique_payment_type() == 'lydia_face2face':
            lydias_facetoface.append(
                {
                    "model": "finances.lydiafacetoface",
                    "pk": rechargings_pk,
                    "fields": {
                        "date_operation": s.date.isoformat().split("T")[0],
                        "id_from_lydia": s.payment.list_lydia()[0][0].id_from_lydia,
                        "banked": False,
                        "date_banked": None
                    }
                }
            )
            payment_solutions.append(
                {
                    "model": "finances.paymentsolution",
                    "pk": rechargings_pk,
                    "fields": {
                        "sender": s.sender.pk,
                        "recipient": s.recipient.pk,
                        "amount": str(s.amount)
                    }
                }
            )
            rechargings.append(
                {
                    "model": "finances.recharging",
                    "pk": rechargings_pk,
                    "fields": {
                        "datetime": s.date.isoformat(),
                        "sender": s.sender.pk,
                        "operator": s.operator.pk,
                        "payment_solution": rechargings_pk
                    }
                }
            )
            rechargings_pk = rechargings_pk + 1
        elif s.payment.unique_payment_type() == 'cheque':
            bank_account = False
            for ba in bank_accounts:
                if ba["fields"]["account"] == s.payment.list_cheque()[0][0].bank_account.account and ba["fields"]["bank"] == s.payment.list_cheque()[0][0].bank_account.bank and ba["fields"]["owner"] == s.payment.list_cheque()[0][0].bank_account.owner.pk:
                    bank_account = ba["pk"]
            if not bank_account:
                bank_accounts.append(
                    {
                        "model": "finances.bank_account",
                        "pk": bank_accounts_pk,
                        "fields": {
                            "bank": s.payment.list_cheque()[0][0].bank_account.bank,
                            "account": s.payment.list_cheque()[0][0].bank_account.account,
                            "owner": s.payment.list_cheque()[0][0].bank_account.owner.pk
                        }
                    }
                )
                bank_account = bank_accounts_pk
                bank_accounts_pk = bank_accounts_pk + 1
            cheques.append(
                    {
                    "model": "finances.cheque",
                    "pk": rechargings_pk,
                    "fields": {
                        "is_cashed": False,
                        "signature_date": s.payment.list_cheque()[0][0].signature_date.isoformat(),
                        "cheque_number": s.payment.list_cheque()[0][0].cheque_number,
                        "bank_account": bank_account
                    }
                }
            )
            payment_solutions.append(
                {
                    "model": "finances.paymentsolution",
                    "pk": rechargings_pk,
                    "fields": {
                        "sender": s.sender.pk,
                        "recipient": s.recipient.pk,
                        "amount": str(s.amount)
                    }
                }
            )
            rechargings.append(
                {
                    "model": "finances.recharging",
                    "pk": rechargings_pk,
                    "fields": {
                        "datetime": s.date.isoformat(),
                        "sender": s.sender.pk,
                        "operator": s.operator.pk,
                        "payment_solution": rechargings_pk
                    }
                }
            )
            rechargings_pk = rechargings_pk + 1

print("\n", str(len(cashs)), ' Cashs mapped\n')
print(str(len(lydias_facetoface)), ' LydiaFaceToFaces mapped\n')
print(str(len(lydias_online)), ' LydiaOnlines mapped\n')
print(str(len(bank_accounts)), ' BankAccounts mapped\n')
print(str(len(cheques)), ' Cheques mapped\n')
print(str(len(payment_solutions)), ' PaymentSolutions Cheques mapped\n')
print(str(len(rechargings)), ' Rechargings mapped\n')

# Sale

print("Mapping sales\n")
from django.contrib.contenttypes.models import ContentType
sales = []
saleproducts = []
sales_pk = 1
saleproducts_pk = 1
map_sip_list = []
map_sip_err = 0
map_spfc_list = []
map_spfc_err = 0
sm = Sale.objects.filter(category = "sale").count()

for s in Sale.objects.filter(category = "sale"):
    progress_bar(sales_pk, sm)
    if s.sender == s.operator:
        for m in selfsalemodules:
            if m["fields"]["shop"] == s.from_shop().pk:
                module = {
                    "content_type": ContentType.objects.get(app_label='modules', model='selfsalemodule').pk,
                    "module_id": m["pk"]
                }
    else:
        for m in selfsalemodules:
            if m["fields"]["shop"] == s.from_shop().pk:
                module = {
                    "content_type": ContentType.objects.get(app_label='modules', model='operatorsalemodule').pk,
                    "module_id": m["pk"]
                }
    sales.append(
        {
          "model": "finances.sale",
          "pk": sales_pk,
          "fields": {
            "datetime": s.date.isoformat(),
            "sender": s.sender.pk,
            "recipient": s.recipient.pk,
            "operator": s.operator.pk,
            "content_type": module["content_type"],
            "module_id": module["module_id"],
            "shop": s.from_shop().pk
          }
        }
    )

    for sip in s.list_single_products()[0]:
        # Get product
        product = False # No else case here, the product must exists
        for p in products:
            if (p["fields"]["name"] == sip.product_base.name and
                    p["fields"]["manual_price"] == str(sip.product_base.get_moded_usual_price()) and
                    p["fields"]["shop"] == sip.product_base.shop.pk and
                    p["fields"]["unit"] == None):
                product = p["pk"]

        if not product:
            if sip.product_base.pk not in map_sip_list:
                map_sip_list.append(sip.product_base.pk)
            map_sip_err = map_sip_err + 1
            #sys.exit("Error")

        if product:
            # Check if SaleProduct exist
            saleproduct = False
            for sap in saleproducts:
                if (sap["fields"]["sale"] == sales_pk and sap["fields"]["product"] == product):
                    saleproduct = sap
            if saleproduct:
                # update current saleproduct
                # Delete, update, append
                saleproducts.remove(saleproduct)
                saleproduct["fields"]["quantity"] = str(int(saleproduct["fields"]["quantity"]) + 1)
                saleproduct["fields"]["price"] = str(Decimal(saleproduct["fields"]["price"]) + sip.sale_price)
                saleproducts.append(saleproduct)
            else:
                saleproducts.append({
                  "model": "finances.saleproduct",
                  "pk": saleproducts_pk,
                  "fields": {
                    "sale": sales_pk,
                    "product": product,
                    "quantity": "1",
                    "price": str(sip.sale_price)
                  }
                })
                saleproducts_pk = saleproducts_pk + 1

    for spfc in s.list_single_products_from_container()[0]:
        # Get product
        product = False # No else case here, the product must exists
        for p in products:
            if spfc.container.product_base.product_unit.unit == "CL":
                if (p["fields"]["name"] == spfc.container.product_base.name and
                        p["fields"]["manual_price"] == str((spfc.container.product_base.get_moded_usual_price() * 100) / Decimal(spfc.container.product_base.product_unit.usual_quantity())) and
                        p["fields"]["shop"] == spfc.container.product_base.shop.pk and
                        p["fields"]["unit"] == spfc.container.product_base.product_unit.unit):
                    product = p["pk"]
            elif spfc.container.product_base.product_unit.unit == "G":
                if (p["fields"]["name"] == spfc.container.product_base.name and
                        p["fields"]["manual_price"] == str((spfc.container.product_base.get_moded_usual_price() * 1000) / Decimal(spfc.container.product_base.product_unit.usual_quantity())) and
                        p["fields"]["shop"] == spfc.container.product_base.shop.pk and
                        p["fields"]["unit"] == spfc.container.product_base.product_unit.unit):
                    product = p["pk"]

        if not product:
            if spfc.container.product_base.pk not in map_spfc_list:
                map_spfc_list.append(sfpc.container.product_base.pk)
            map_spfc_err = map_spfc_err + 1

        # Check if SaleProduct exist
        saleproduct = False
        for sap in saleproducts:
            if (sap["fields"]["sale"] == sales_pk and sap["fields"]["product"] == product):
                saleproduct = sap
        if saleproduct:
            # update current saleproduct
            # Delete, update, append
            saleproducts.remove(saleproduct)
            saleproduct["fields"]["quantity"] = str(Decimal(saleproduct["fields"]["quantity"]) + spfc.quantity)
            saleproduct["fields"]["price"] = str(Decimal(saleproduct["fields"]["price"]) + spfc.sale_price)
            saleproducts.append(saleproduct)
        else:
            saleproducts.append({
              "model": "finances.saleproduct",
              "pk": saleproducts_pk,
              "fields": {
                "sale": sales_pk,
                "product": product,
                "quantity": str(spfc.quantity),
                "price": str(spfc.sale_price)
              }
            })
            saleproducts_pk = saleproducts_pk + 1

    sales_pk = sales_pk + 1
# 73, 90, 67

print("\nsip : ", map_sip_err, map_sip_list)
print("spfc : ", map_spfc_err, map_spfc_list)
print("\n", str(len(sales)), ' Sales mapped\n')

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
        "datetime": se.date.isoformat(),
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
    _list = users + shops + selfsalemodules + operatorsalemodules + products + exceptionnal_movements + transferts + cashs + lydias_facetoface + lydias_online + cheques + payment_solutions + rechargings + sales + saleproducts + sharedevents + weightsusers
    _str = json.dumps(_list,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(_str)
    outfile.close()
print("Dump completed.\n")

print("Selfsalemodule content type pk: ", ContentType.objects.get(app_label='modules', model='selfsalemodule').pk, "\n")
print("Operatorsalemodule content type pk: ", ContentType.objects.get(app_label='modules', model='operatorsalemodule').pk, "\n")
