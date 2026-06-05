from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.


categories = [
    ("PIZZA","Pizza"),
    ("BURGER","Burger"),
    ("FRENCH FRIES","French Fries"),
    ("DESSERTS","Desserts"),
    ("BEVERAGES","Beverages"),
    ("BIRIYANI","Biryani"),
]

size_chart = [
    ("REGULAR","Regular"),
    ("MEDIUM","Medium"),
    ("LARGE","Large"),  
]
base = [
    ("MAIDA","Maida"),
    ("WHEAT","Wheat"),
]
class FoodItems(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    rating = models.IntegerField()
    desc = models.TextField()
    food_img = models.ImageField(upload_to='foodimg/',null=True, blank=True)
    category = models.CharField(max_length=100,choices=categories)


    def __str__(self):
        return self.name


class Customize_options(models.Model):
    food_type = models.CharField(max_length=100,choices=categories)
    size = models.ForeignKey('SizeChart',related_name= "sizes", on_delete=models.CASCADE)
    base = models.CharField(max_length=100,choices=base)
    sauce = models.ForeignKey('Sauce',related_name= "sauces", on_delete=models.CASCADE)
    toppings = models.ForeignKey('Toppings',related_name= "toppings", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='customizeimg/',null=True, blank=True)
    def __str__(self):
        return self.food_type

class SizeChart(models.Model):
    size_type = models.CharField(max_length=100,choices=size_chart)
    size_in_cm = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.size_type


class BaseType(models.Model):
    base_name = models.CharField(max_length=100)
    base_img = models.ImageField(upload_to='baseimg/',null=True, blank=True)

    def __str__(self):
        return self.base_name
    
class Toppings(models.Model):
    topping_name = models.CharField(max_length=100)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    topping_img = models.ImageField(upload_to='toppings/')

    def __str__(self):
        return self.topping_name
    
class Sauce(models.Model):
    sname = models.CharField(max_length=100)
    simage = models.ImageField(upload_to='sauces/')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.sname
    
class Cart(models.Model):
    food = models.ForeignKey("FoodItems",related_name= "fooditems", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()
    is_customized = models.BooleanField(default=False)

    def __str__(self):
        return self.food.name


class CustomizedCart(models.Model):
    """Stores customized food items with selections"""
    food = models.ForeignKey("FoodItems", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.ForeignKey('SizeChart', null=True, blank=True, on_delete=models.SET_NULL)
    base = models.ForeignKey('BaseType', null=True, blank=True, on_delete=models.SET_NULL)
    sauce = models.ForeignKey('Sauce', null=True, blank=True, on_delete=models.SET_NULL)
    toppings = models.ManyToManyField('Toppings', blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # food price
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # all prices combined
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        """Calculate total price: base + size + sauce + toppings"""
        total = float(self.base_price)
        
        if self.size:
            total += float(self.size.price)
        if self.sauce:
            total += float(self.sauce.price)
        
        # Add all selected toppings
        for topping in self.toppings.all():
            total += float(topping.price)
        
        # Multiply by quantity
        self.total_price = total * self.quantity
        return self.total_price

    def __str__(self):
        return f"{self.food.name} (Customized) x{self.quantity}"


class Order(models.Model):
    """Stores completed orders with unique ID, customer info, and items"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    order_id = models.CharField(max_length=100, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Generate unique order ID if not already set"""
        if not self.order_id:
            # Generate order ID: ORDER_TIMESTAMP_UUID
            self.order_id = f"ORD_{self.created_at.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8].upper()}" if self.created_at else f"ORD_{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"


class OrderItem(models.Model):
    """Stores individual food items in an order"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food = models.ForeignKey('FoodItems', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    is_customized = models.BooleanField(default=False)
    customization_details = models.TextField(blank=True)  # JSON or text details
    
    def __str__(self):
        return f"{self.food.name} x{self.quantity} in {self.order.order_id}"



class Review(models.Model):
    food        = models.ForeignKey(FoodItems, on_delete=models.CASCADE, related_name='reviews')
    reviewer    = models.CharField(max_length=100)          # name of reviewer
    rating      = models.IntegerField(
                    validators=[MinValueValidator(1), MaxValueValidator(5)]
                  )
    comment     = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']                          # newest first

    def __str__(self):
        return f"{self.reviewer} → {self.food.name} ({self.rating}★)"


from django.contrib.auth.models import User

class Wishlist(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    food       = models.ForeignKey(FoodItems, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'food')   # ← prevents duplicate entries at DB level
        ordering        = ['-added_at']

    def __str__(self):
        return f"{self.user.username} → {self.food.name}"
