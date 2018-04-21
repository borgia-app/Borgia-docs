# FROM 9628a7a8abf36b2dff99c513aef84d3ad9701897 TO 27ba11b03a2e6fe5303d6370f718d8f5738db2d8

## users.models

### User

1 -> 1
theme —> ‘light’

TODO: groups

## shops.models

### Shop

1 -> 1

### Products (name, is_manual, manual_price, shop, is_active, is_removed, unit, correcting_factor)

### ProductBase_old (Name, description , is_manual, manual_price, brand, type, quantity, shop, product_unit, is_active)

```
For each ProductBase:
	Create new Product
		name —> name
		is*manual = True
		if product_unit:
			If product_unit.unit = ‘CL’:
				manual_price = (get_moded_usual_price() * 100) / product*unit.usual_quantity
			Else product_unit.unit = ‘G’:
				manual_price = (get_moded_usual_price() * 1000) / product_unit.usual_quantity
		else:
			manual_price = get_moded_usual_price()
		shop —> shop
		is_active = True
		is_removed = False
		if product_unit:
		unit = product_unit.unit
		correcting_factor = Decimal(1)
```

### Caution:

Remove products with unit ‘CENT’
Must review all product prices before prod
Must do an inventory before prod

## stocks.models

No populate for all models.

## settings_data.models

No populate for all models.

## notifications.models

No populate for all models.

## modules.models

No populate for all models.
Will be created during populating finances and prod.

## finances.models

### Sale_old (Amount, date, done, is_credit, category, wording, justification, sender, recipient, operator, payment)

### ExceptionnalMovement (Datetime, justification, operator, recipient, amount, is_credit)

```
For each Sale where category = ‘exceptionnal_movement’:
	Create new ExceptionnalMovement
		datetime —> date
		justification —> justification
		operator —> operator
		recipient —> sender (!!!)
		amount —> amount
		is_credit —> is_credit
```

### Transfert (Datetime, justification, sender, recipient, amount)

```
For each Sale where category = ‘transfer’:
	Create new Transfert
		datetime —> date
		justification —> justification
		sender —> sender
		recipient —> recipient
		amount —> amount
```

### Recharging (datetime, sender, operator, payment_solution)

### LydiaOnline (ender, recipient, amount, date_operation, id_from_lydia, banked, date_banked)

### LydiaFaceToFace (sender, recipient, amount, date_operation, id_from_lydia, banked, date_banked)

### Cash (sender, recipient, amount)

### Cheque (sender, recipient, amount, is_cashed, cheque_number, signature_date, bank_account)

### BankAccount (bank, account, owner)

```
For each Sale where category = ‘recharging’ && wording = ‘Rechargement automatique’:
	if payment.unique_payment_type == ‘lydia_auto’:
	Create new Recharging
		datetime —> date
		sender —> sender
		operator —> operator
		payment_solution = Create new LydiaOnline
				sender -> sender
				recipient -> AE ENSAM
				amount -> amount
				date_operation —> date
				id_from_lydia —> payment.lydias[0].id_from_lydia
```

```
For each Sale where category = ‘recharging’ && wording = ‘Rechargement manuel’:

if payment.unique_payment_type == ‘cash’:
	Create new Recharging
		datetime —> date
		sender —> sender
		operator —> operator
		payment_solution = Create new Cash
			sender —> sender
			recipient —> AE ENSAM
			amount —> amount

if payment.unique_payment_type == ‘lydia_face2face’:
Create new Recharging
datetime —> date
sender —> sender
operator —> operator
payment_solution = Create new LydiaFaceToFace
	sender —> sender
	recipient —> AE ENSAM
	amount —> amount
	date_operation —> date
	id_from_lydia —> payment.lydias[0].id_from_lydia

if payment.unique_payment_type == ‘cheque’:
	Create new Recharging
		datetime —> date
		sender —> sender
		operator —> operator
		payment_solution = Create new Cheque
		sender —> sender
		recipient —> AE ENSAM
		amount —> amount
		is_cashed —> False
		cheque_number —> payment.cheques[0].cheque_number
		signature_date —> payment.cheques[0].signature_date
		bank_account —> Get or Create BankAccount
			bank -> payment.cheques[0].bank_account.bank
			account -> payment.cheques[0].bank_account.account
			owner -> payment.cheques[0].bank_account.owner
```

### Sale (datetime, sender, recipient, operator, content_type, module_id, module, shop, products)

### SaleProduct (sale, product, quantity, price)

Sale_old (Amount, date, done, is_credit, category, wording, justification, sender, recipient, operator, payment)

```
For each Sale where category = 'sale':
	if sender is operator:
		module = Get or Create Module (selfsale, from_shop())
	else:
		module = Get or Create Module (operatorSale, from_shop())

	sale = Create new Sale
		datetime -> date
		sender -> sender
		recipient -> AE ENSAM
		operator -> operator
		module -> module
		shop -> from_shop()

	products = []
	For each singleproduct in list_single_products()[0]:
		product = Get or Create new Product
			name —> singleproduct.product_base.name
			is*manual = True
			if product_unit:
				If singleproduct.product_base.product_unit.unit = ‘CL’:
					manual_price = (singleproduct.product_base.get_moded_usual_price() * 100) / singleproduct.product_base.roduct*unit.usual_quantity
				Else singleproduct.product_base.product_unit.unit = ‘G’:
					manual_price = (singleproduct.product_base.get_moded_usual_price() * 1000) / singleproduct.product_base.product_unit.usual_quantity
			else:
				manual_price = singleproduct.product_base.get_moded_usual_price()
			shop —> shop
			is_active = True
			is_removed = False
			if product_unit:
				unit = singleproduct.product_base.product_unit.unit
			correcting_factor = Decimal(1)

		if Get SaleProduct(sale = sale, product = product) exists:
			saleproduct = Get SaleProduct(sale = sale, product = product)
			saleproduct.quantity = saleproduct.quantity + 1
			saleproduct.price = saleproduct.price + singleproduct.sale_price
			saleproduct.save()
		else:
			Create New SaleProduct
				sale -> sale
				product -> product
				quantity -> 1
				price -> singleproduct.sale_price

	For each singleproductfromcontainer in list_single_products_from_container()[0]:
		product = Get or Create new Product
			name —> singleproductfromcontainer.product_base.name
			is*manual = True
			if product_unit:
				If singleproductfromcontainer.product_base.product_unit.unit = ‘CL’:
					manual_price = (singleproductfromcontainer.product_base.get_moded_usual_price() * 100) / singleproductfromcontainer.product_base.roduct*unit.usual_quantity
				Else singleproductfromcontainer.product_base.product_unit.unit = ‘G’:
					manual_price = (singleproductfromcontainer.product_base.get_moded_usual_price() * 1000) / singleproductfromcontainer.product_base.product_unit.usual_quantity
			else:
				manual_price = singleproductfromcontainer.product_base.get_moded_usual_price()
			shop —> shop
			is_active = True
			is_removed = False
			if product_unit:
				unit = singleproductfromcontainer.product_base.product_unit.unit
			correcting_factor = Decimal(1)

			if Get SaleProduct(sale = sale, product = product) exists:
				saleproduct = Get SaleProduct(sale = sale, product = product)
				saleproduct.quantity = saleproduct.quantity + singleproductfromcontainer.quantity
				saleproduct.price = saleproduct.price + singleproductfromcontainer.sale_price
				saleproduct.save()
			else:
				Create New SaleProduct
					sale -> sale
					product -> product
					quantity -> singleproductfromcontainer.quantity
					price -> singleproductfromcontainer.sale_price
```

### Caution:

The identification of the module may be changed ...
