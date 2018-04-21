from decimal import Decimal

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
print(len(users) + ' mapped')


# SHOPS MODELS
from shops.models import Shop, ProductBase

# Shop
print("Mapping shops")
shops = []
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
print(len(shops) + ' mapped')

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
print(len(products) + ' mapped')

# Product
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
print(len(exceptionnal_movements) + ' mapped')

print("Mapping transferts")
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
print(len(transferts) + ' mapped')

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

                    }
                }
            )
            payment_solutions.append(
                {
                    "models": "finances.paymentsolution",
                    "pk": rechargings_pk,
                    "fields": {

                    }
                }
            )
            rechargings.append(
                {
                    "models": "finances.paymentsolution",
                    "pk": rechargings_pk,
                    "fields": {

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
                    "fields": {

                    }
                }
            )
            payment_solutions.append(
                {
                    "models": "finances.paymentsolution",
                    "pk": rechargings_pk,
                    "fields": {

                    }
                }
            )
            rechargings.append(
                {
                    "models": "finances.paymentsolution",
                    "pk": rechargings_pk,
                    "fields": {

                    }
                }
            )
            echargings_pk = rechargings_pk + 1
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

                    }
                }
            )
            rechargings.append(
                {
                    "models": "finances.paymentsolution",
                    "pk": rechargings_pk,
                    "fields": {

                    }
                }
            )
            echargings_pk = rechargings_pk + 1
        elif s.payment.unique_payment_type = 'cheque':
            # Create bank account if needed
            cheques.append(
                {
                    "models": "finances.cheque",
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

                    }
                }
            )
            rechargings.append(
                {
                    "models": "finances.paymentsolution",
                    "pk": rechargings_pk,
                    "fields": {

                    }
                }
            )
            echargings_pk = rechargings_pk + 1

print(len(rechargings) + ' mapped')
