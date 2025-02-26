from django.contrib import admin
from .models import Products,Order,Cart,OrderItem,Reviews
# Register your models here
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Reviews)
