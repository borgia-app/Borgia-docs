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
