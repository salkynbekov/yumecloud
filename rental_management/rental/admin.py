from django.contrib import admin

from rental.models import OrderProduct, Order, Product

admin.site.register([Product, Order, OrderProduct])
