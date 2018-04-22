from decimal import Decimal
import json
import datetime

# USERS MODELS
from users.models import ExtendedPermission, User

# User
print("Mapping users")
users = []
for u in User.objects.all():
    users.append(
        {
            "model": "users.user",
            "pk": u.pk,
            "fields": {
                "password": u.password,
                "last_login": null,
                "is_superuser": false,
                "username": u.username,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email,
                "is_staff": false,
                "is_active": u.is_active,
                "date_joined": u.date_joined.iso_format(),
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
print(len(users) + ' Users mapped')


# SHOPS MODELS & MODULES MODELS
from shops.models import Shop, ProductBase

# Shop, SelfSaleModule, OperatorSaleModule
print("Mapping shops, selfsalemodules & operatorsalemodules")
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
                    "state": false,
                    "shop": s.pk,
                    "delay_post_purchase": null,
                    "limit_purchase": null,
                    "logout_post_purchase": false
                }
            }
        )
        operatorsalemodules.append(
            {
                "model": "modules.operatorsalemodule",
                "pk": modules_pk,
                "fields": {
                    "state": false,
                    "shop": s.pk,
                    "delay_post_purchase": null,
                    "limit_purchase": null,
                    "logout_post_purchase": false
                }
            }
        )
        modules_pk = modules_pk + 1
print(len(shops) + ' Shops, SelfSaleModules & OperatorSaleModules mapped')

# Product
print("Mapping products")
products = []
products_pk = 1
for pb in ProductBase.objects.all():
    if pb.product_unit:
        if pb.product_unit.unit = "CL":
            products.append(
                {
                    "model": "shops.product",
                    "pk": products_pk,
                    "fields": {
                        "name": pb.name,
                        "is_manual": true,
                        "manual_price": str((pb.get_moded_usual_price() * 100) / pb.product_unit.usual_quantity),
                        "shop": pb.shop.pk,
                        "is_active": true,
                        "is_removed": false,
                        "unit": "CL",
                        "correcting_factor": "1"
                    }
                }
            )
        elif pb.product_unit.unit = "G":
            products.append(
                {
                    "model": "shops.product",
                    "pk": products_pk,
                    "fields": {
                        "name": pb.name,
                        "is_manual": true,
                        "manual_price": str((pb.get_moded_usual_price() * 1000) / pb.product_unit.usual_quantity),
                        "shop": pb.shop.pk,
                        "is_active": true,
                        "is_removed": false,
                        "unit": "G",
                        "correcting_factor": "1"
                    }
                }
            )
    else:
        products.append(
            {
                "model": "shops.product",
                "pk": products_pk,
                "fields": {
                    "name": pb.name,
                    "is_manual": true,
                    "manual_price": str(pb.get_moded_usual_price()),
                    "shop": pb.shop.pk,
                    "is_active": true,
                    "is_removed": false,
                    "unit": null,
                    "correcting_factor": "1"
                }
            }
        )

    products_pk = products_pk + 1
print(len(products) + ' Products mapped')


# FINANCES MODELS

# ExceptionnalMovement

print("Mapping exceptionnal movements")
exceptionnal_movements = []
exceptionnal_movements_pk = 1
for s in Sale.objects.filter(category="exceptionnal_movement"):
    exceptionnal_movements.append(
        {
            "models": "finances.exceptionnal_movement",
            "pk": exceptionnal_movements_pk,
            "fields": {
                "datetime": s.date.iso_format(),
                "justification": s.justification,
                "operator": s.operator.pk,
                "recipient": s.sender.pk,
                "amount": str(s.amount),
                "is_credit": s.is_credit
            }
        }
    )
    exceptionnal_movements_pk = exceptionnal_movements_pk + 1
print(len(exceptionnal_movements) + ' ExceptionnalMovements mapped')

# Transfer

print("Mapping transfers")
transferts = []
transferts_pk = 1
for s in Sale.objects.filter(category = 'transfer'):
    transferts.append(
        {
            "models": "finances.transfert",
            "pk": transferts_pk,
            "fields": {
                "datetime": s.date.iso_format(),
                "justification": s.justification,
                "operator": s.operator.pk,
                "recipient": s.recipient.pk,
                "amount": str(s.amount),
            }
        }
    )
    transferts_pk = transferts_pk + 1
print(len(transferts) + ' Transfers mapped')

# Recharging

print("Mapping rechargings")
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
    if s.wording = "Rechargement automatique":
        if s.payment.unique_payment_type = 'lydia_auto':
            lydias_online.append(
                {
                    "models": "finances.lydiaonline",
                    "pk": rechargings_pk,
                    "fields": {
                        "date_operation": s.date.iso_format(),
                        "id_from_lydia": s.payment.lydias[0].id_from_lydia,
                        "banked": false,
                        "date_banked": null
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
                        "datetime": s.date.iso_format(),
                        "sender": s.sender.pk,
                        "operator": s.operator.pk,
                        "payment_solution": rechargings_pk
                    }
                }
            )
            rechargings_pk = rechargings_pk + 1
    elif s.wording = "Recharging manuel":
        if s.payment.unique_payment_type = 'cash':
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
                        "datetime": s.date.iso_format(),
                        "sender": s.sender.pk,
                        "operator": s.operator.pk,
                        "payment_solution": rechargings_pk
                    }
                }
            )
            rechargings_pk = rechargings_pk + 1
        elif s.payment.unique_payment_type = 'lydia_face2face':
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
                        "datetime": s.date.iso_format(),
                        "sender": s.sender.pk,
                        "operator": s.operator.pk,
                        "payment_solution": rechargings_pk
                    }
                }
            )
            rechargings_pk = rechargings_pk + 1
        elif s.payment.unique_payment_type = 'cheque':
            bank_account = False
            for ba in bank_accounts:
                if ba.fields.account = s.payment.cheques[0].bank_account.account and ba.fields.bank = s.payment.cheques[0].bank_account.bank and ba.fields.owner = s.payment.cheques[0].bank_account.owner.pk:
                    bank_account = ba.account.pk
                else:
                    bank_accounts.append(
                        {
                            "models": "finances.bank_account",
                            "pk": bank_accounts_pk,
                            "fields": {
                                bank: s.payment.cheques[0].bank_account.bank,
                                account: s.payment.cheques[0].bank_account.account,
                                owner: s.payment.cheques[0].bank_account.owner.pk
                            }
                        }
                    )
                    bank_accounts_pk = bank_accounts_pk + 1
            cheques.append(
                {
                    "models": "finances.cheque",
                    "pk": rechargings_pk,
                    "fields": {
                        "is_cashed": false,
                        "signature_date": s.payment.cheques[0].signature_date.iso_format()),
                        "cheque_number": s.payment.cheques[0].cheque_number,
                        "bank_account": bank_accounts_pk
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
                        "datetime": s.date.iso_format(),
                        "sender": s.sender.pk,
                        "operator": s.operator.pk,
                        "payment_solution": rechargings_pk
                    }
                }
            )
            rechargings_pk = rechargings_pk + 1

print(len(cashs) + ' Cashs mapped')
print(len(lydias_facetoface) + ' LydiaFaceToFaces mapped')
print(len(lydias_online) + ' LydiaOnlines mapped')
print(len(bank_accounts) + ' BankAccounts mapped')
print(len(cheques) + ' Cheques mapped')
print(len(payment_solutions) + ' PaymentSolutions Cheques mapped')
print(len(rechargings) + ' Rechargings mapped')


# DUMPING

print("Dumping to json ...")
with open('dump_' + datetime.datetime.now().iso_format() + '.json', 'w') as outfile:
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
print("Dump completed.")
