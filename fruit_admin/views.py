from http.client import HTTPResponse

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from fruit_admin.models import Product, Cash, Income, ChatMessage
from fruit_admin.tasks import buy_bananas, buy_apples, buy_pineapples, buy_peaches, sell_peaches, sell_pineapples, \
    sell_apples, sell_bananas


def warehouse(request):
    products = Product.objects.all()
    cash = Cash.objects.first()
    logs = Income.objects.all().order_by('-created').select_related()[:20]
    chat_messages = ChatMessage.objects.all()[:40]
    return render(request, 'fruit_admin/warehouse/index.html', {
        "products": products,
        "cash": cash, "logs": logs,
        "chat_messages": chat_messages
    })


def sell_product(request, product_id):
    products_buy_functions = {
        'бананы': sell_bananas, 'яблоки': sell_apples, 'ананасы': sell_pineapples, 'персики': sell_peaches
    }
    product = Product.objects.get(id=product_id)
    count = request.POST.get('count')
    products_buy_functions[product.name].delay(quantity=int(count))
    return JsonResponse({'pk': product.id})


def buy_product(request, product_id):
    print('buy product')
    products_buy_functions = {
        'бананы': buy_bananas, 'яблоки': buy_apples, 'ананасы': buy_pineapples, 'персики': buy_peaches
    }
    product = Product.objects.get(id=product_id)
    count = request.POST.get('count')
    print(request.POST)
    products_buy_functions[product.name].delay(quantity=int(count))
    return JsonResponse({'pk': product.id})


def add_cash(request):
    amount = request.POST.get('amount')
    cash = Cash.objects.first()
    cash.sum = cash.sum + float(amount)
    cash.save()
    print(cash.sum)
    return JsonResponse({"cash": cash.sum}, safe=False)
