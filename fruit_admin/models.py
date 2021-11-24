import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Product(models.Model):
    name = models.CharField("Название", max_length=100)
    price = models.IntegerField("Цена")


class Income(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='incomes')
    count = models.IntegerField("Кол-во")

    class TypeIncome(models.TextChoices):
        income = "Приход", _("Приход")
        expense = "Продажа", _("Продажа")

    class StatusIncome(models.TextChoices):
        success = "SUCCESS", _("SUCCESS")
        error = "ERROR", _("ERROR")

    type = models.CharField(choices=TypeIncome.choices, max_length=20)
    status = models.CharField(choices=StatusIncome.choices, max_length=30, default=StatusIncome.success)
    created = models.DateTimeField(auto_now_add=True)


class ProductCount(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Cash(models.Model):
    sum = models.FloatField()


class ChatMessage(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
