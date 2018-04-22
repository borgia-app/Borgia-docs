import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "borgia.settings")
django.setup()

from decimal import Decimal
import json
import datetime

# USERS MODELS
from users.models import ExtendedPermission, User

# User
print("Mapping users\n")
users = []
for u in User.objects.all():
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
                "theme": "light"
            }
        }
    )
print(str(len(users)), " Users mapped\n")


# SHOPS MODELS & MODULES MODELS
from shops.models import Shop, ProductBase

# Shop, SelfSaleModule, OperatorSaleModule
print("Mapping shops, selfsalemodules & operatorsalemodules\n")
shops = []
selfsalemodules = []
operatorsalemodules = []
modules_pk = 1
for s in Shop.objects.all():
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
print(str(len(shops)), " Shops, SelfSaleModules & OperatorSaleModules mapped\n")

# Product
print("Mapping products\n")
products = []
products_pk = 1
for pb in ProductBase.objects.all():
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
    products_pk = products_pk + 1
print(str(len(products)), " Products mapped\n")

# FINANCES MODELS

# ExceptionnalMovement

from finances.models import Sale
print("Mapping exceptionnal movements\n")
exceptionnal_movements = []
exceptionnal_movements_pk = 1
for s in Sale.objects.filter(category="exceptionnal_movement"):
    exceptionnal_movements.append(
        {
            "models": "finances.exceptionnal_movement",
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
print(len(exceptionnal_movements), ' ExceptionnalMovements mapped\n')

# Transfer

print("Mapping transfers\n")
transferts = []
transferts_pk = 1
for s in Sale.objects.filter(category = 'transfert'):
    transferts.append(
        {
            "models": "finances.transfert",
            "pk": transferts_pk,
            "fields": {
                "datetime": s.date.isoformat(),
                "justification": s.justification,
                "operator": s.operator.pk,
                "recipient": s.recipient.pk,
                "amount": str(s.amount),
            }
        }
    )
    transferts_pk = transferts_pk + 1
print(str(len(transferts)) + " Transfers mapped\n")

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
for s in Sale.objects.filter(category = 'recharging'):
    if s.wording == "Rechargement automatique":
        print("auto")
        if s.payment.unique_payment_type() == 'lydia_auto':
            print("lydia_auto")
            lydias_online.append(
                {
                    "models": "finances.lydiaonline",
                    "pk": rechargings_pk,
                    "fields": {
                        "date_operation": s.date.isoformat(),
                        "id_from_lydia": s.payment.list_lydia()[0][0].id_from_lydia,
                        "banked": False,
                        "date_banked": None
                    }
                }
            )
            payment_solutions.append(
                {
                    "models": "finances.paymentsolution",
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
                    "models": "finances.paymentsolution",
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
                    "models": "finances.cash",
                    "pk": rechargings_pk,
                    "fields": {}
                }
            )
            payment_solutions.append(
                {
                    "models": "finances.paymentsolution",
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
                    "models": "finances.paymentsolution",
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
                    "models": "finances.lydiafacetoface",
                    "pk": rechargings_pk,
                    "fields": {

                    }
                }
            )
            payment_solutions.append(
                {
                    "models": "finances.paymentsolution",
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
                    "models": "finances.paymentsolution",
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
                        "models": "finances.bank_account",
                        "pk": bank_accounts_pk,
                        "fields": {
                            bank: s.payment.list_cheque()[0][0].bank_account.bank,
                            account: s.payment.list_cheque()[0][0].bank_account.account,
                            owner: s.payment.list_cheque()[0][0].bank_account.owner.pk
                        }
                    }
                )
                bank_account = bank_accounts_pk
                bank_accounts_pk = bank_accounts_pk + 1
            cheques.append(
                    {
                    "models": "finances.cheque",
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
                    "models": "finances.paymentsolution",
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
                    "models": "finances.paymentsolution",
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

print(str(len(cashs)), ' Cashs mapped\n')
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
for s in Sale.objects.filter(category = "sale"):
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
                    p["fields"]["manual_price"] == sip.product_base.get_moded_usual_price() and
                    p["fields"]["shop"] == sip.product_base.shop.pk and
                    p["fields"]["unit"] == None):
                product = sip

        # Check if SaleProduct exist
        saleproduct = False
        for sap in saleproducts:
            if (sap["fields"]["sale"] == sales_pk and sap["fields"]["product"] == product["pk"]):
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
                "sale": s.pk,
                "product": product["pk"],
                "quantity": "1",
                "price": str(sip.sale_price)
              }
            })
            saleproducts_pk = saleproducts_pk + 1

    for spfc in s.list_single_products_from_container()[0]:
        # Get product
        product = False # No else case here, the product must exists
        for p in products:
            if spfc.product_base.product_unit.unit == "CL":
                if (p["fields"]["name"] == spfc.product_base.name and
                        p["fields"]["manual_price"] == str((spfc.product_base.get_moded_usual_price() * 100) / spfc.product_base.product_unit.usual_quantity) and
                        p["fields"]["shop"] == spfc.product_base.shop.pk and
                        p["fields"]["unit"] == spfc.product_base.product_unit.unit):
                    product = spfc
            elif spfc.product_base.product_unit.unit == "G":
                if (p["fields"]["name"] == spfc.product_base.name and
                        p["fields"]["manual_price"] == str((spfc.product_base.get_moded_usual_price() * 1000) / spfc.product_base.product_unit.usual_quantity) and
                        p["fields"]["shop"] == spfc.product_base.shop.pk and
                        p["fields"]["unit"] == spfc.product_base.product_unit.unit):
                    product = spfc

        # Check if SaleProduct exist
        saleproduct = False
        for sap in saleproducts:
            if (sap["fields"]["sale"] == sales_pk and sap["fields"]["product"] == product["pk"]):
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
                "sale": s.pk,
                "product": product["pk"],
                "quantity": str(spfc.quantity),
                "price": str(spfc.sale_price)
              }
            })
            saleproducts_pk = saleproducts_pk + 1
print(str(len(sales)), ' Sales mapped\n')

# DUMPING
print("Dumping to json ...\n")
with open('dump_' + datetime.datetime.now().isoformat() + '.json', 'w') as outfile:
    json.dump(users, outfile)
    json.dump(shops, outfile)
    json.dump(selfsalemodules, outfile)
    json.dump(operatorsalemodules, outfile)
    json.dump(products, outfile)
    json.dump(exceptionnal_movements, outfile)
    json.dump(transferts, outfile)
    json.dump(cashs, outfile)
    json.dump(lydias_facetoface, outfile)
    json.dump(lydias_online, outfile)
    json.dump(cheques, outfile)
    json.dump(payment_solutions, outfile)
    json.dump(rechargings, outfile)
    json.dump(sales, outfile)
    json.dump(saleproducts, outfile)
print("Dump completed.\n")
