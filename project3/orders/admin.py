  
from django.contrib import admin

from .models import Inventory, Topping, ItemCost, ToppingCount, Type, Size, Orderr, Completed_Order

# Register your models here.
admin.site.register(Inventory)
admin.site.register(Topping)
admin.site.register(ItemCost)
admin.site.register(ToppingCount)
admin.site.register(Type)
admin.site.register(Size)
admin.site.register(Orderr)
admin.site.register(Completed_Order)