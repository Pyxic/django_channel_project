import json
import random
from datetime import date

import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Func, F, Value, CharField
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from fruit_admin.models import Product, Cash, Income, ChatMessage
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
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='ERROR')
        print("Not enough money")
    async_to_sync(channel_layer.group_send)(
        "story", {"type": "update.story", "status": income.status, 'income_type': income.type,
                  "count": income.count, 'product': income.product.name, 'price': income.product.price,
                  'created': str(income.created.strftime('%d.%m.%Y %H:%M'))}
    )


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
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='ERROR')
        print(f"Not enough money for buy {quantity} bananas")
    async_to_sync(channel_layer.group_send)(
        "story", {"type": "update.story", "status": income.status, 'income_type': income.type,
                  "count": income.count, 'product': income.product.name, 'price': income.product.price,
                  'created': str(income.created.strftime('%d.%m.%Y %H:%M'))}
    )


@app.task
def buy_pineapples(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 10)
    product = Product.objects.get(name='ананасы')
    cash = Cash.objects.first()
    if cash.sum > product.price*quantity:
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='SUCCESS')
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
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='ERROR')
        print(f"Not enough money for buy {quantity} pineapples")
    async_to_sync(channel_layer.group_send)(
        "story", {"type": "update.story", "status": income.status, 'income_type': income.type,
                  "count": income.count, 'product': income.product.name, 'price': income.product.price,
                  'created': str(income.created.strftime('%d.%m.%Y %H:%M'))}
    )
        

@app.task
def buy_peaches(quantity=None):
    if quantity is None:
        quantity = random.randint(5, 15)
    product = Product.objects.get(name='персики')
    cash = Cash.objects.first()
    if cash.sum > product.price*quantity:
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='SUCCESS')
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
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.income, status='ERROR')
        print(f"Not enough money for buy {quantity} peaches")
    async_to_sync(channel_layer.group_send)(
        "story", {"type": "update.story", "status": income.status, 'income_type': income.type,
                  "count": income.count, 'product': income.product.name, 'price': income.product.price,
                  'created': str(income.created.strftime('%d.%m.%Y %H:%M'))}
    )


@app.task
def sell_apples(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 10)
    product = Product.objects.get(name='яблоки')
    cash = Cash.objects.first()
    if product.productcount.quantity >= quantity:
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense,
                                       status='SUCCESS')
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
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='ERROR')
        print(f"Not enough quantity for sell {quantity} apple")
    async_to_sync(channel_layer.group_send)(
        "story", {"type": "update.story", "status": income.status, 'income_type': income.type,
                  "count": income.count, 'product': income.product.name, 'price': income.product.price,
                  'created': str(income.created.strftime('%d.%m.%Y %H:%M'))}
    )


@app.task
def sell_bananas(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 30)
    product = Product.objects.get(name='бананы')
    cash = Cash.objects.first()
    if product.productcount.quantity >= quantity:
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense,
                                       status='SUCCESS')
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
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='ERROR')
        print(f"Not enough quantity for sell {quantity} bananas")
    async_to_sync(channel_layer.group_send)(
        "story", {"type": "update.story", "status": income.status, 'income_type': income.type,
                  "count": income.count, 'product': income.product.name, 'price': income.product.price,
                  'created': str(income.created.strftime('%d.%m.%Y %H:%M'))}
    )


@app.task
def sell_pineapples(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 10)
    product = Product.objects.get(name='ананасы')
    cash = Cash.objects.first()
    if product.productcount.quantity >= quantity:
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense,
                                       status='SUCCESS')
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
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='ERROR')
        print(f"Not enough quantity for sell {quantity} pineapples")
    async_to_sync(channel_layer.group_send)(
        "story", {"type": "update.story", "status": income.status, 'income_type': income.type,
                  "count": income.count, 'product': income.product.name, 'price': income.product.price,
                  'created': str(income.created.strftime('%d.%m.%Y %H:%M'))}
    )


@app.task
def sell_peaches(quantity=None):
    if quantity is None:
        quantity = random.randint(1, 20)
    product = Product.objects.get(name='персики')
    cash = Cash.objects.first()
    if product.productcount.quantity >= quantity:
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense,
                                       status='SUCCESS')
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
        income = Income.objects.create(product=product, count=quantity, type=Income.TypeIncome.expense, status='ERROR')
        print(f"Not enough quantity for sell {quantity} peaches")
    async_to_sync(channel_layer.group_send)(
        "story", {"type": "update.story", "status": income.status, 'income_type': income.type,
                  "count": income.count, 'product': income.product.name, 'price': income.product.price,
                  'created': str(income.created.strftime('%d.%m.%Y %H:%M'))}
    )


@app.task
def get_random_joke():
    res = requests.get("https://tproger.ru/wp-content/plugins/citation-widget/get-quote.php")
    print(res.text)
    joke = res.text
    message = ChatMessage.objects.create(text=joke, user=User.objects.get(username='jocker'))
    async_to_sync(channel_layer.group_send)(
        "jokes", {"type": "jokes.joke", "text": joke, "user": message.user.username}
    )
    PeriodicTask.objects.update_or_create(
        name='Get joke',
        defaults={
            'name': 'Get joke',
            'interval': IntervalSchedule.objects.get_or_create(
                every=float(len(joke)),
                period=IntervalSchedule.SECONDS)[0],
            'task': 'fruit_admin.tasks.get_random_joke'
        }
    )


@app.task
def update_stock():
    gen = [x for x in range(1, 10000)]
    for _ in gen:
        pass


@app.task
def get_updates():
    last_updates = Income.objects.annotate(
        formatted_date=Func(
            F('created'),
            Value('HH:mm'),
            function='to_char',
            output_field=CharField()
        )
    ).filter(status='SUCCESS').order_by('-id').values('type', 'formatted_date', 'product__name')[:4]
    data = json.dumps(list(last_updates), cls=DjangoJSONEncoder)
    async_to_sync(channel_layer.group_send)(
        "last_updates", {"type": "update.last", "last_updates": data}
    )
