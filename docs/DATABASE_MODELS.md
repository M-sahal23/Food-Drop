# Database Models - FoodDrop

This document provides detailed information about all database models used in the FoodDrop application.

## 🗄️ Database Schema Overview

### **FoodItems** 📍
The main model for storing food item information.

```python
- id (auto)
- name: CharField(100)
- price: IntegerField
- rating: IntegerField
- description: TextField
- category: Choice field (PIZZA, BURGER, FRIES, DESSERTS, BEVERAGES, BIRYANI)
- food_img: ImageField
- created_at: DateTime (optional)
- updated_at: DateTime (optional)
```

**Use**: Stores all food items available in the catalog with their basic information and pricing.

---

### **Customize_options** 🎨
Model for storing customization templates for different food types.

```python
- id (auto)
- food_type: CharField with categories
- size: ForeignKey → SizeChart
- base: CharField (MAIDA, WHEAT)
- sauce: ForeignKey → Sauce
- toppings: ForeignKey → Toppings
- image: ImageField
```

**Use**: Defines available customization options for each food type.

---

### **SizeChart** 📏
Model for managing food sizes and their pricing.

```python
- id (auto)
- size_type: Choice (REGULAR, MEDIUM, LARGE)
- size_in_cm: CharField
- price: DecimalField(10, 2)
```

**Use**: Stores different size options and their associated prices.

---

### **Sauce** 🌶️
Model for managing sauce options.

```python
- id (auto)
- sname: CharField(100)
- simage: ImageField
- price: DecimalField(10, 2)
```

**Use**: Stores available sauces with their images and prices.

---

### **Toppings** 🍕
Model for managing topping options.

```python
- id (auto)
- topping_name: CharField(100)
- qty: IntegerField (available quantity)
- price: DecimalField(10, 2)
- topping_img: ImageField
```

**Use**: Stores available toppings with inventory and pricing.

---

### **Cart** 🛒
Model for storing regular (non-customized) cart items.

```python
- id (auto)
- food: ForeignKey → FoodItems
- quantity: IntegerField
- total_price: IntegerField
- is_customized: BooleanField
```

**Use**: Stores shopping cart items for users.

---

### **CustomizedCart** 🎯
Model for storing customized cart items.

```python
- id (auto)
- food: ForeignKey → FoodItems
- quantity: IntegerField
- size: ForeignKey → SizeChart (nullable)
- base: ForeignKey → BaseType (nullable)
- sauce: ForeignKey → Sauce (nullable)
- toppings: ManyToManyField → Toppings
- base_price: DecimalField(10, 2)
- sauce_qty: IntegerField
- total_addons_price: DecimalField(10, 2)
```

**Use**: Stores customized food items in cart with all customization details and pricing breakdown.

---

### **Order** 📦
Model for storing order information.

```python
- id: UUIDField (Primary)
- user: ForeignKey → User (nullable)
- customer_email: EmailField
- status: Choice (Pending, Confirmed, Shipped, Delivered)
- payment_method: CharField
- total_amount: DecimalField(10, 2)
- created_at: DateTimeField
- updated_at: DateTimeField
```

**Use**: Stores order records with status tracking and payment information.

---

### **OrderItem** 📋
Model for storing individual items within an order.

```python
- id (auto)
- order: ForeignKey → Order
- food: ForeignKey → FoodItems
- quantity: IntegerField
- price: DecimalField(10, 2)
- customizations: JSONField (optional)
```

**Use**: Stores details of each item in an order.

---

### **Review** ⭐
Model for storing customer reviews.

```python
- id (auto)
- food: ForeignKey → FoodItems
- user: ForeignKey → User
- rating: IntegerField (1-5)
- comment: TextField
- created_at: DateTimeField
- updated_at: DateTimeField
```

**Use**: Stores customer ratings and reviews for food items.

---

### **Wishlist** 💝
Model for storing user wishlist items.

```python
- id (auto)
- user: ForeignKey → User
- food: ForeignKey → FoodItems
- added_at: DateTimeField
```

**Use**: Stores favorite food items for each user.

---

### **UserDetails** 👤
Model for storing extended user profile information.

```python
- id (auto)
- user: OneToOneField → User
- phone: CharField(10) - Unique
- address: CharField(100)
- street: CharField(100)
- city: CharField(100)
- zipcode: CharField(10)
- profile_pic: ImageField (nullable)
- user_type: Choice (VENDOR, NORMAL_USER)
```

**Use**: Extends Django's User model with additional profile and address information.

---

## 📊 Model Relationships

```
User (Django)
  ├── UserDetails (1:1)
  ├── Review (1:Many)
  ├── Wishlist (1:Many)
  └── Order (1:Many)

FoodItems
  ├── Cart (1:Many)
  ├── CustomizedCart (1:Many)
  ├── Review (1:Many)
  ├── Wishlist (1:Many)
  └── OrderItem (1:Many)

Order
  └── OrderItem (1:Many)

SizeChart
  └── CustomizedCart (1:Many)

Sauce
  ├── Customize_options (1:Many)
  └── CustomizedCart (1:Many)

Toppings
  ├── Customize_options (1:Many)
  └── CustomizedCart (Many:Many)
```

---

## 🔄 Database Migration History

To view all migrations:
```bash
python manage.py showmigrations
```

To apply migrations:
```bash
python manage.py migrate
```

To create new migrations after model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📝 Notes

- All price fields use `DecimalField(10, 2)` for precision
- Images are stored in `MEDIA_ROOT` directory
- UUIDs are used for Order primary keys for security
- Timestamps are automatically managed for created_at and updated_at fields
- User authentication extends Django's built-in User model

