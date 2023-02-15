from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
from datetime import datetime


# Create your views here.
def store(request):
	products = Product.objects.all()
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# It will get all the orderItems which will have "order" as parent
		items = order.orderitem_set.all()
		cart_items = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total': 0,
				 'get_cart_items': 0,
				 "shipping": "False"
				 }
		cart_items = order['get_cart_items']

	context = {'products': products, 'cart_items': cart_items, 'order': order}
	return render(request, 'store/store.html', context=context)


def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# It will get all the orderItems which will have "order" as parent
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_total': 0,
				 'get_cart_items': 0,
				 "shipping": "False"
				 }

	context = {'items': items, 'order': order}
	return render(request, 'store/cart.html', context=context)


def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		# Create Empty cart for now for none-logged in users
		order = {'get_cart_total': 0, "get_cart_items": 0, "shipping": "False"}
		items = []

	context = {"items": items, "order": order}
	return render(request, "store/checkout.html", context)


def updateItem(request):
	data = json.loads(request.body)
	product_id = data['productId']
	action = data['action']
	print("product:", product_id)
	print("action:", action)

	customer = request.user.customer
	product = Product.objects.get(id=product_id)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		order_item.quantity += 1
	elif action == 'remove':
		order_item.quantity -= 1
	order_item.save()

	if order_item.quantity <= 0:
		order_item.delete()

	return JsonResponse("Item added successfully", safe=False)


def processOrder(request):
	transaction_id = datetime.now().timestamp()
	data = json.load(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping:
			ShippingAddress.object.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode = data['shipping']['zipcode'],
			)

	else:
		print("User not logged in .!")

	return JsonResponse("Payment successfully", safe=False)

