from django.contrib import admin
from foods.models import Customize_options, FoodItems, SizeChart, BaseType, Sauce, Toppings, Order, OrderItem, Cart, CustomizedCart

# Register your models here.
admin.site.register(FoodItems)
admin.site.register(Customize_options)
admin.site.register(SizeChart)
admin.site.site_header = "Foodie Admin"
admin.site.register(BaseType)
admin.site.register(Sauce)
admin.site.register(Toppings)
admin.site.register(Cart)
admin.site.register(CustomizedCart)


class OrderItemInline(admin.TabularInline):
    """Inline display of order items within Order admin"""
    model = OrderItem
    readonly_fields = ('order', 'food', 'quantity', 'price', 'is_customized', 'customization_details')
    extra = 0
    can_delete = False


class OrderAdmin(admin.ModelAdmin):
    """Admin panel for viewing and managing orders"""
    list_display = ('order_id', 'customer_name', 'total_price', 'status', 'created_at', 'item_count')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('order_id', 'customer_name')
    readonly_fields = ('order_id', 'created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'customer_name', 'status')
        }),
        ('Financial Details', {
            'fields': ('total_price',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def item_count(self, obj):
        """Display the count of items in this order"""
        return obj.items.count()
    item_count.short_description = 'Items Count'


class OrderItemAdmin(admin.ModelAdmin):
    """Admin panel for viewing order items"""
    list_display = ('get_order_id', 'food', 'quantity', 'price', 'is_customized', 'get_created_date')
    list_filter = ('order__status', 'is_customized', 'order__created_at')
    search_fields = ('order__order_id', 'food__name')
    readonly_fields = ('order', 'food', 'quantity', 'price', 'is_customized', 'customization_details')
    
    def get_order_id(self, obj):
        """Display the order ID"""
        return obj.order.order_id
    get_order_id.short_description = 'Order ID'
    
    def get_created_date(self, obj):
        """Display the order creation date"""
        return obj.order.created_at
    get_created_date.short_description = 'Order Date'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
