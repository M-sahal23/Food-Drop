# 🍕 FoodDrop - Online Food Ordering Platform

[![Django 5.2.9](https://img.shields.io/badge/Django-5.2.9-darkgreen?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat-square&logo=bootstrap)](https://getbootstrap.com/)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

A production-ready Django web application for online food ordering with integrated payment processing, user authentication, advanced food customization, and real-time order tracking.

> 🚀 **Status**: Deployment Ready ✅

## 📋 Quick Links

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Installation](#-quick-start)
- [Deployment](#-deployment)
- [Author](#-author)
- [License](#-license)
- [Documentation](#-documentation)

## 🎯 Overview

FoodDrop is a full-stack Django application that enables users to browse food items, customize their orders, manage shopping carts, and process payments securely. Built with a focus on user experience and security, it features:

- User authentication and profile management
- Advanced food customization (sizes, sauces, toppings, bases)
- Real-time cart management
- Secure payment processing (UPI, Cards, COD)
- Order tracking and history
- Wishlist functionality
- Customer reviews and ratings
- Responsive mobile-first design

## ✨ Key Features

### 👤 User Management
- User registration with email verification
- Secure login/logout with session management  
- User profile management with address details
- Dual user types: Vendor & Customer
- Auto-logout after idle time (200 seconds)

### 🍔 Food Ordering
- Comprehensive food catalog with search
- Category-based filtering (Pizza, Burgers, Fries, Desserts, etc.)
- Real-time food availability status
- Food details with high-resolution images

### 🎨 Customization Engine
- Size selection with dynamic pricing
- Multiple sauce selections with quantity controls
- Multiple toppings with individual quantities
- Live price calculation
- Real-time customization preview

### 🛒 Shopping Cart & Checkout
- Dynamic cart management with real-time updates
- Support for both regular and customized items
- Multiple payment methods (UPI, Cards, COD)
- Order confirmation with receipt

### 📦 Order Management
- Order confirmation and receipt
- Real-time order status tracking
- Order history with filtering
- Email notifications

### 🔒 Security
- Google reCAPTCHA v3 integration
- Argon2 password hashing
- CSRF token protection
- SQL injection prevention
- XSS protection

## � Screenshots

### Homepage
![Homepage](./docs/screenshots/homepage.png)
*Browse available food items with search and filter capabilities*

### Food Details Page
![Food Details](./docs/screenshots/food-details.png)
*Detailed food information with reviews and customization options*

### Customization Interface
![Customization](./docs/screenshots/customization.png)
*Intuitive food customization with real-time price calculation*

### Shopping Cart
![Shopping Cart](./docs/screenshots/cart.png)
*Manage cart items with quantity controls and price breakdown*

### Checkout & Payment
![Payment](./docs/screenshots/payment.png)
*Secure payment processing with multiple payment methods*

### Order Tracking
![Order Tracking](./docs/screenshots/order-tracking.png)
*Real-time order status tracking and history*

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
PostgreSQL 12+ (or SQLite for development)
Git
```

### Installation
```bash
# Clone repository
git clone https://github.com/M-sahal23/Food-Drop.git
cd Food-Drop

# Create virtual environment
python -m venv env1
source env1/bin/activate  # Windows: env1\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Access application
# Homepage: http://localhost:8000
# Admin: http://localhost:8000/admin
```

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | Django | 5.2.9 |
| Database | PostgreSQL | 12+ |
| Language | Python | 3.8+ |
| Frontend | HTML5/CSS3/JavaScript | ES6+ |
| UI Framework | Bootstrap | 5.x |
| Authentication | Django Auth + Argon2 | - |
| Security | Google reCAPTCHA v3 | v3 |

## 🚀 Deployment

### Environment Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/M-sahal23/Food-Drop.git
   cd Food-Drop
   ```

2. **Virtual Environment**
   ```bash
   python -m venv env1
   source env1/bin/activate  # Windows: env1\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### Production Deployment

- **Heroku**: Quick cloud deployment
- **DigitalOcean**: Full VPS control
- **AWS/EC2**: Enterprise-grade hosting
- **Render**: Modern platform as a service
- **PythonAnywhere**: Python-specific hosting

> For detailed deployment instructions, see [DEPLOYMENT.md](./docs/DEPLOYMENT.md)

---

## 📚 Documentation

For detailed information, see:

- [DATABASE_MODELS.md](./docs/DATABASE_MODELS.md) - Database schema and models
- [CONFIGURATION.md](./docs/CONFIGURATION.md) - Detailed configuration guide
- [API_ENDPOINTS.md](./docs/API_ENDPOINTS.md) - Complete API reference
- [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md) - Common issues and solutions
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guidelines

---

## 👨‍💻 Author

**Muhammed Sahal**

- B.Tech Information Technology
- Aspiring Full Stack Developer
- **Skills**: Django | Python | PostgreSQL | Bootstrap | JavaScript

**Connect**:
- GitHub: [M-sahal23](https://github.com/M-sahal23)
- Repository: [Food-Drop](https://github.com/M-sahal23/Food-Drop)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated**: June 2026  
**Django Version**: 5.2.9  
**Status**: Deployment Ready ✅
