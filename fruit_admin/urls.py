from django.urls import path

from fruit_admin import views

urlpatterns = [
    path('', views.warehouse, name='warehouse'),
    path('sell_product/<int:product_id>', views.sell_product, name='sell_product'),
    path('buy_product/<int:product_id>', views.buy_product, name='buy_product'),
    path('add_cash', views.add_cash, name='add_cash'),
]
