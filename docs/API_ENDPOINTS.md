# API Endpoints Reference - FoodDrop

Complete reference of all API endpoints available in the FoodDrop application.

## 🔐 Authentication Endpoints

### User Registration
```
POST /register/
Content-Type: application/x-www-form-urlencoded

Parameters:
- username: string (required)
- email: string (required)
- password1: string (required)
- password2: string (required)
- first_name: string (optional)
- last_name: string (optional)

Response: 200 OK
{
  "message": "User registered successfully",
  "user_id": 1,
  "redirect_url": "/login/"
}
```

### User Login
```
POST /login/
Content-Type: application/x-www-form-urlencoded

Parameters:
- username: string (required)
- password: string (required)

Response: 200 OK
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "user@example.com",
    "email": "user@example.com"
  }
}
```

### User Logout
```
GET /logout/

Response: 200 OK
{
  "message": "Logged out successfully",
  "redirect_url": "/"
}
```

### User Profile
```
GET /profile/

Response: 200 OK
{
  "user": {
    "id": 1,
    "username": "user",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "details": {
    "phone": "9876543210",
    "address": "123 Main Street",
    "city": "New York",
    "zipcode": "10001",
    "user_type": "NORMAL_USER"
  }
}
```

### Password Reset Request
```
POST /password-reset/
Content-Type: application/x-www-form-urlencoded

Parameters:
- email: string (required)

Response: 200 OK
{
  "message": "Password reset email sent"
}
```

---

## 🍔 Food Endpoints

### List All Foods
```
GET /foods/allfoods/

Query Parameters:
- page: integer (optional, default: 1)
- search: string (optional)
- category: string (optional)

Response: 200 OK
{
  "foods": [
    {
      "id": 1,
      "name": "Margherita Pizza",
      "price": 250,
      "rating": 4.5,
      "description": "Classic pizza",
      "category": "PIZZA",
      "image_url": "/media/foodimg/pizza1.jpg"
    }
  ],
  "total_count": 50,
  "page": 1
}
```

### Get Food Details
```
GET /foods/<id>/

Response: 200 OK
{
  "food": {
    "id": 1,
    "name": "Margherita Pizza",
    "price": 250,
    "rating": 4.5,
    "description": "Classic pizza",
    "category": "PIZZA",
    "image_url": "/media/foodimg/pizza1.jpg",
    "reviews": [
      {
        "user": "john_doe",
        "rating": 5,
        "comment": "Excellent pizza!",
        "created_at": "2024-01-15T10:30:00Z"
      }
    ],
    "average_rating": 4.7,
    "total_reviews": 24
  }
}
```

### Search Foods
```
GET /foods/search/

Query Parameters:
- q: string (required, search term)
- category: string (optional)

Response: 200 OK
{
  "results": [
    {
      "id": 1,
      "name": "Margherita Pizza",
      "price": 250,
      "rating": 4.5,
      "image_url": "/media/foodimg/pizza1.jpg"
    }
  ],
  "count": 5
}
```

### Add New Food (Vendor Only)
```
POST /foods/addnewfood/
Content-Type: multipart/form-data

Parameters:
- name: string (required)
- price: integer (required)
- description: text (required)
- category: string (required)
- food_img: file (required)

Response: 201 Created
{
  "message": "Food item added successfully",
  "food_id": 25,
  "food_name": "Special Pizza"
}
```

---

## 🛒 Cart Endpoints

### Add to Cart
```
POST /foods/cart/<food_id>/
Content-Type: application/x-www-form-urlencoded

Parameters:
- quantity: integer (required)
- is_customized: boolean (optional, default: false)

Response: 200 OK
{
  "message": "Item added to cart",
  "cart_count": 3,
  "total_price": 750
}
```

### View Cart
```
GET /foods/cart/

Response: 200 OK
{
  "items": [
    {
      "id": 1,
      "food": "Margherita Pizza",
      "quantity": 2,
      "unit_price": 250,
      "total_price": 500,
      "is_customized": false,
      "image_url": "/media/foodimg/pizza1.jpg"
    }
  ],
  "total_items": 2,
  "subtotal": 750,
  "tax": 75,
  "total": 825
}
```

### Update Item Quantity
```
POST /foods/cart/update-quantity/<item_id>/
Content-Type: application/x-www-form-urlencoded

Parameters:
- quantity: integer (required, minimum: 1)

Response: 200 OK
{
  "message": "Quantity updated",
  "new_quantity": 3,
  "new_total": 750,
  "cart_total": 1500
}
```

### Remove from Cart
```
DELETE /foods/cart/delete/<item_id>/

Response: 200 OK
{
  "message": "Item removed from cart",
  "cart_count": 1,
  "total_price": 250
}
```

### Get Cart Count
```
GET /foods/api/cart-count/

Response: 200 OK
{
  "count": 3
}
```

---

## 🎨 Customization Endpoints

### Get Customization Options
```
GET /foods/customize/<food_id>/

Response: 200 OK
{
  "food": {
    "id": 1,
    "name": "Margherita Pizza",
    "base_price": 250
  },
  "sizes": [
    { "id": 1, "name": "Regular", "price": 0 },
    { "id": 2, "name": "Medium", "price": 50 },
    { "id": 3, "name": "Large", "price": 100 }
  ],
  "bases": [
    { "id": 1, "name": "Maida" },
    { "id": 2, "name": "Wheat" }
  ],
  "sauces": [
    { "id": 1, "name": "Tomato", "price": 20 },
    { "id": 2, "name": "Mayo", "price": 20 }
  ],
  "toppings": [
    { "id": 1, "name": "Cheese", "price": 30, "available_qty": 100 },
    { "id": 2, "name": "Pepperoni", "price": 40, "available_qty": 50 }
  ]
}
```

### Save Customized Item
```
POST /foods/customize/save/<food_id>/
Content-Type: application/json

Parameters:
{
  "quantity": 1,
  "size_id": 2,
  "base_id": 1,
  "sauce_id": 1,
  "toppings": [1, 2],
  "sauce_qty": 2
}

Response: 201 Created
{
  "message": "Customized item added to cart",
  "customized_item_id": 5,
  "total_price": 480
}
```

### Update Customized Item Quantity
```
POST /foods/cart/update-customized-quantity/<item_id>/
Content-Type: application/x-www-form-urlencoded

Parameters:
- quantity: integer (required)

Response: 200 OK
{
  "message": "Customized item quantity updated",
  "new_total_price": 960
}
```

---

## 💳 Order & Payment Endpoints

### Buy Now
```
GET /foods/buy-now/

Response: 200 OK
{
  "cart_items": [...],
  "total_amount": 825
}
```

### Order Confirmation
```
POST /foods/order-confirmation/<cart_id>/
Content-Type: application/x-www-form-urlencoded

Parameters:
- delivery_address: string (required)
- phone: string (required)
- notes: string (optional)

Response: 201 Created
{
  "message": "Order confirmed",
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_amount": 825
}
```

### Payment Page
```
GET /foods/payment/<order_id>/

Response: 200 OK
{
  "order": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "total_amount": 825,
    "status": "Pending"
  },
  "payment_methods": [
    "UPI",
    "CARD",
    "COD"
  ]
}
```

### Process Payment
```
POST /foods/process-payment/<order_id>/
Content-Type: application/json

Parameters:
{
  "payment_method": "UPI",
  "payment_id": "UPI123456789",
  "upi_id": "user@upi"
}

Response: 200 OK
{
  "message": "Payment processed",
  "status": "SUCCESS",
  "transaction_id": "TXN123456789"
}
```

### Payment Success
```
GET /foods/payment-success/<order_id>/

Response: 200 OK
{
  "message": "Payment successful",
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "order_items": [...],
  "total_amount": 825
}
```

### Get Order Status
```
GET /foods/order-status/<order_id>/

Response: 200 OK
{
  "order": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "Confirmed",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z",
    "items": [...]
  }
}
```

### Order History
```
GET /foods/order-history/

Query Parameters:
- page: integer (optional)
- status: string (optional)

Response: 200 OK
{
  "orders": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "total_amount": 825,
      "status": "Delivered",
      "created_at": "2024-01-15T10:30:00Z",
      "item_count": 2
    }
  ],
  "total_count": 15,
  "page": 1
}
```

### Order Tracking
```
GET /foods/order-tracking/<order_id>/

Response: 200 OK
{
  "order": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "Out for Delivery",
    "current_location": "Downtown",
    "estimated_delivery": "2024-01-15T14:30:00Z",
    "timeline": [
      { "status": "Order Placed", "timestamp": "2024-01-15T10:30:00Z" },
      { "status": "Confirmed", "timestamp": "2024-01-15T10:35:00Z" },
      { "status": "Preparing", "timestamp": "2024-01-15T10:45:00Z" },
      { "status": "Out for Delivery", "timestamp": "2024-01-15T12:00:00Z" }
    ]
  }
}
```

---

## ⭐ Review & Rating Endpoints

### Add Review
```
POST /foods/food/<food_id>/review/
Content-Type: application/json

Parameters:
{
  "rating": 5,
  "comment": "Great pizza! Highly recommended."
}

Response: 201 Created
{
  "message": "Review added successfully",
  "review_id": 1,
  "average_rating": 4.7
}
```

### Get Food Reviews
```
GET /foods/food/<food_id>/reviews/

Query Parameters:
- page: integer (optional)

Response: 200 OK
{
  "reviews": [
    {
      "id": 1,
      "user": "john_doe",
      "rating": 5,
      "comment": "Excellent pizza!",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "average_rating": 4.7,
  "total_reviews": 24
}
```

---

## 💝 Wishlist Endpoints

### View Wishlist
```
GET /foods/wishlist/

Response: 200 OK
{
  "items": [
    {
      "id": 1,
      "food": "Margherita Pizza",
      "price": 250,
      "added_at": "2024-01-10T15:20:00Z",
      "image_url": "/media/foodimg/pizza1.jpg"
    }
  ],
  "total_items": 5
}
```

### Toggle Wishlist Item
```
POST /foods/wishlist/toggle/<food_id>/

Response: 200 OK
{
  "message": "Item added to wishlist",
  "in_wishlist": true
}
```

### Move from Wishlist to Cart
```
POST /foods/wishlist/to-cart/<food_id>/
Content-Type: application/x-www-form-urlencoded

Parameters:
- quantity: integer (required)

Response: 200 OK
{
  "message": "Item moved to cart",
  "cart_count": 3
}
```

---

## 📝 Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Successful delete |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Not authenticated |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## 🔒 Authentication

All protected endpoints require authentication. Include session cookies or authentication tokens in requests:

```
Cookie: sessionid=<session_id>
```

---

## 📚 Additional Documentation

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [HTTP Status Codes](https://httpwg.org/specs/rfc7231.html#status.codes)

