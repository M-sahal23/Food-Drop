from django.contrib import admin
from foods.models import Customize_options, FoodItems, SizeChart, BaseType, Sauce, Toppings

# Register your models here.
admin.site.register(FoodItems)
admin.site.register(Customize_options)
admin.site.register(SizeChart)
admin.site.site_header = "Foodie Admin"
admin.site.register(BaseType)
admin.site.register(Sauce)
admin.site.register(Toppings)