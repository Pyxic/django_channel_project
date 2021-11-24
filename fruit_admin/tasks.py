import json
import random
from datetime import date

import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User

from fruit_admin.models import Product, Cash, Income
from fruit_admin.models import ProductCount
from fruit.celery import app
from celery.schedules import crontab

channel_layer = get_channel_layer()


# @app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(6.0, buy_apples.s())
#
#     sender.add_periodic_task(9.0, buy_bananas.s())
#
#     sender.add_periodic_task(12.0, buy_pineapples.s())
#
#     sender.add_periodic_task(15.0, buy_peaches.s())
#     sender.add_periodic_task(15.0, sell_apples.s())
#
#     sender.add_periodic_task(12.0, sell_bananas.s())
#
#     sender.add_periodic_task(9.0, sell_pineapples.s())
#
#     sender.add_periodic_task(6.0, sell_peaches.s())


@app.task
def buy_apples(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 10)
    product = Product.objects.get(name='яблоки')
    cash = Cash.objects.first()
    if cash.sum > product.price*quantity:

        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='SUCCESS')
        print('create_income')
        product_count = product.productcount
        product_count.quantity += quantity
        product_count.save()
        print("buy_apple")
        cash.sum -= product.price*quantity
        cash.save()
        async_to_sync(channel_layer.group_send)(
            "products_count", {"type": "update.count", "count": product_count.quantity, 'product': product.id,
                               'cash': cash.sum}
        )
    else:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='ERROR')
        print("Not enough money")


@app.task
def buy_bananas(quantity=None):
    if quantity is None:
        quantity = random.randint(10, 20)
    product = Product.objects.get(name='бананы')
    cash = Cash.objects.first()
    if cash.sum > product.price*quantity:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='SUCCESS')
        print('create_income')
        product_count = product.productcount
        product_count.quantity += quantity
        product_count.save()
        print("buy bananas")
        cash.sum -= product.price * quantity
        cash.save()
        async_to_sync(channel_layer.group_send)(
            "products_count", {"type": "update.count", "count": product_count.quantity, 'product': product.id,
                               'cash': cash.sum}
        )
    else:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='ERROR')
        print(f"Not enough money for buy {quantity} bananas")


@app.task
def buy_pineapples(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 10)
    product = Product.objects.get(name='ананасы')
    cash = Cash.objects.first()
    if cash.sum > product.price*quantity:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='SUCCESS')
        print('create_income')
        product_count = product.productcount
        product_count.quantity += quantity
        product_count.save()
        print("buy_pineapples")
        cash.sum -= product.price * quantity
        cash.save()
        async_to_sync(channel_layer.group_send)(
            "products_count", {"type": "update.count", "count": product_count.quantity, 'product': product.id,
                               'cash': cash.sum}
        )
    else:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='ERROR')
        print(f"Not enough money for buy {quantity} pineapples")
        

@app.task
def buy_peaches(quantity=None):
    if quantity is None:
        quantity = random.randint(5, 15)
    product = Product.objects.get(name='персики')
    cash = Cash.objects.first()
    if cash.sum > product.price*quantity:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='SUCCESS')
        print('create_income')
        product_count = product.productcount
        product_count.quantity += quantity
        product_count.save()
        print("buy_peaches")
        cash.sum -= product.price * quantity
        cash.save()
        async_to_sync(channel_layer.group_send)(
            "products_count", {"type": "update.count", "count": product_count.quantity, 'product': product.id,
                               'cash': cash.sum}
        )
    else:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='ERROR')
        print(f"Not enough money for buy {quantity} peaches")


@app.task
def sell_apples(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 10)
    product = Product.objects.get(name='яблоки')
    cash = Cash.objects.first()
    if product.productcount.quantity >= quantity:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='SUCCESS')
        print('create_expense')
        product_count = product.productcount
        product_count.quantity -= quantity
        product_count.save()
        print("sell_apples")
        cash.sum += product.price * quantity
        cash.save()
        async_to_sync(channel_layer.group_send)(
            "products_count", {"type": "update.count", "count": product_count.quantity, 'product': product.id,
                               'cash': cash.sum}
        )
    else:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='ERROR')
        print(f"Not enough quantity for sell {quantity} apple")


@app.task
def sell_bananas(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 30)
    product = Product.objects.get(name='бананы')
    cash = Cash.objects.first()
    if product.productcount.quantity >= quantity:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='SUCCESS')
        print('create_expense')
        product_count = product.productcount
        product_count.quantity -= quantity
        product_count.save()
        print("sell_bananas")
        cash.sum += product.price * quantity
        cash.save()
        async_to_sync(channel_layer.group_send)(
            "products_count", {"type": "update.count", "count": product_count.quantity, 'product': product.id,
                               'cash': cash.sum}
        )
    else:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='ERROR')
        print(f"Not enough quantity for sell {quantity} bananas")


@app.task
def sell_pineapples(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 10)
    product = Product.objects.get(name='ананасы')
    cash = Cash.objects.first()
    if product.productcount.quantity >= quantity:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='SUCCESS')
        print('create_expense')
        product_count = product.productcount
        product_count.quantity -= quantity
        product_count.save()
        print("sell_pineapples")
        cash.sum += product.price * quantity
        cash.save()
        async_to_sync(channel_layer.group_send)(
            "products_count", {"type": "update.count", "count": product_count.quantity, 'product': product.id,
                               'cash': cash.sum}
        )
    else:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='ERROR')
        print(f"Not enough quantity for sell {quantity} pineapples")


@app.task
def sell_peaches(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 20)
    product = Product.objects.get(name='персики')
    cash = Cash.objects.first()
    if product.productcount.quantity >= quantity:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='SUCCESS')
        print('create_expense')
        product_count = product.productcount
        product_count.quantity -= quantity
        product_count.save()
        print("sell_peaches")
        cash.sum += product.price * quantity
        cash.save()
        async_to_sync(channel_layer.group_send)(
            "products_count", {"type": "update.count", "count": product_count.quantity, 'product': product.id,
                               'cash': cash.sum}
        )
    else:
        Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='ERROR')
        print(f"Not enough quantity for sell {quantity} peaches")


@app.task
def get_random_joke():
    res = requests.get("https://tproger.ru/wp-content/plugins/citation-widget/get-quote.php")
    print(res.text)
    joke = res.text
    async_to_sync(channel_layer.group_send)(
        "jokes", {"type": "jokes.joke", "text": joke, "user": User.objects.get(username='jocker').username}
    )
