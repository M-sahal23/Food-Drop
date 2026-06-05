from django.shortcuts import get_object_or_404, render, redirect
from foods.models import FoodItems, Cart, CustomizedCart, Order, OrderItem
from foods.forms import FoodItemForm, CustomizationForm
from foods.models import SizeChart, BaseType, Sauce, Toppings
import json
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Avg
from foods.forms import ReviewForm       
from foods.models import Review

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from foods.models import Wishlist

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.contrib.auth.models import User


# Create your views here.
def Food_Details(request, id=0):
    fooditem    = get_object_or_404(FoodItems, id=id)
    reviews     = Review.objects.filter(food=fooditem)
    avg_rating  = reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating  = round(avg_rating, 1) if avg_rating else 0
    form        = ReviewForm()

    # check if current user has wishlisted this food
    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(
            user=request.user, food=fooditem
        ).exists()

    return render(request, 'foods/fooddetails.html', {
        'fooditem':      fooditem,
        'reviews':       reviews,
        'avg_rating':    avg_rating,
        'form':          form,
        'total':         reviews.count(),
        'is_wishlisted': is_wishlisted,
    })

def add_review(request, food_id):
    food = get_object_or_404(FoodItems, id=food_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review      = form.save(commit=False)
            review.food = food
            review.save()

    # always redirect back to food detail page
    return redirect('fooddetails', id=food_id)

def AllFoods(request):
    allfood = FoodItems.objects.all()
    return render(request,'foods/allfoods.html',{'allfood':allfood})

def AddNewFood(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('addnewfood')
    else:
        form = FoodItemForm()
    return render(request,'foods/addnewfood.html', {'form': form})

# def AddToCart(request,id=0):
#     if request.method == 'POST':
#         carts = FoodItems.objects.all(id=id)
#         if carts.is_valid():
#             carts.save()
#             return redirect('cart')
#     return render(request,'foods/cart.html',{'carts':carts})

# def AddToCart(request,id):
#     carts = get_object_or_404(FoodItems, id=id)

#     # Check if food already in cart
#     cart_item, created = Cart.objects.get_or_create(
#         food=carts,
#         defaults={
#             'Name': carts.name,
#             'Rating': carts.rating,
#             'quantity': 1,
#             'total_price': carts.price
#         }
#     )

#     # If already exists → increase quantity
#     if not created:
#         cart_item.quantity += 1
#         cart_item.total_price = cart_item.quantity * carts.price
#         cart_item.save()

#     return redirect('cart',id)

def AddToCart(request, id):
    food = get_object_or_404(FoodItems, id=id)
    
    # Get quantity from request (POST or GET)
    quantity = int(request.POST.get('quantity', request.GET.get('quantity', 1)))

    cart_item, created = Cart.objects.get_or_create(
        food=food,
        defaults={
            'quantity': quantity,
            'total_price': quantity * food.price
        }
    )

    if not created:
        # If item already exists, add the new quantity
        cart_item.quantity += quantity
        cart_item.total_price = cart_item.quantity * food.price
        cart_item.save()

    return redirect('cart')

# def cart_view(request,id=0):
#     cart_items = Cart.objects.all(id=id)
#     grand_total = sum(item.total_price for item in cart_items)

#     context = {
#         'cart_items': cart_items,
#         'grand_total': grand_total
#     }
#     return render(request, 'cart.html', context)

def cart_view(request):
    """Display all cart items (both regular and customized)"""
    regular_cart_items = Cart.objects.all()
    customized_cart_items = CustomizedCart.objects.all()
    
    # Calculate totals
    regular_total = sum(item.total_price for item in regular_cart_items)
    customized_total = sum(float(item.total_price) for item in customized_cart_items)
    grand_total = regular_total + customized_total

    context = {
        'cart_items': regular_cart_items,
        'customized_items': customized_cart_items,
        'regular_total': regular_total,
        'customized_total': customized_total,
        'grand_total': grand_total
    }
    return render(request, 'foods/cart.html', context)

def delete_from_cart(request, id):
    """Delete a food item from the cart"""
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.delete()
    return redirect('cart')

def update_quantity(request, id):
    """Update the quantity of a food item in the cart"""
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item = get_object_or_404(Cart, id=id)
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        
        # Recalculate total price based on new quantity
        cart_item.total_price = cart_item.quantity * cart_item.food.price
        cart_item.save()
    
    return redirect('cart')


def delete_customized_item(request, id):
    """Delete a customized food item from cart"""
    customized_item = get_object_or_404(CustomizedCart, id=id)
    customized_item.delete()
    return redirect('cart')


def update_customized_quantity(request, id):
    """Update quantity of customized item"""
    if request.method == 'POST':
        action = request.POST.get('action')
        customized_item = get_object_or_404(CustomizedCart, id=id)
        
        if action == 'increase':
            customized_item.quantity += 1
        elif action == 'decrease' and customized_item.quantity > 1:
            customized_item.quantity -= 1
        
        # Recalculate total price
        customized_item.calculate_total_price()
        customized_item.save()
    
    return redirect('cart')




def Customize_Food(request, id=0):
    """Display customization page with options based on food category"""
    food = get_object_or_404(FoodItems, id=id)
    size_opt = SizeChart.objects.all()
    base_opt = BaseType.objects.all()
    sauce_opt = Sauce.objects.all()
    toppings_opt = Toppings.objects.all()
    
    # Define which options to show based on category
    show_size = False
    show_base = False
    show_sauce = False
    show_toppings = False
    
    if food.category == "PIZZA":
        show_size = True
        show_base = True
        show_sauce = True
        show_toppings = True
    elif food.category == "BURGER":
        show_size = False      # Burgers don't have sizes
        show_base = True
        show_sauce = True
        show_toppings = True
    elif food.category == "BIRIYANI":
        show_size = False
        show_base = False
        show_sauce = False
        show_toppings = True   # Only toppings for biryani
    elif food.category == "FRENCH FRIES":
        show_size = True
        show_base = False
        show_sauce = True
        show_toppings = True
    elif food.category == "DESSERTS":
        show_size = False
        show_base = False
        show_sauce = False
        show_toppings = True
    elif food.category == "BEVERAGES":
        show_size = True
        show_base = False
        show_sauce = False
        show_toppings = False
    
    context = {
        'food': food,
        'size_opt': size_opt if show_size else [],
        'base_opt': base_opt if show_base else [],
        'sauce_opt': sauce_opt if show_sauce else [],
        'toppings_opt': toppings_opt if show_toppings else [],
        'show_size': show_size,
        'show_base': show_base,
        'show_sauce': show_sauce,
        'show_toppings': show_toppings,
        'food_category': food.category,
    }
    return render(request, 'foods/customize.html', context)


def save_customization(request, id):
    """Save customized food item to cart"""
    if request.method == 'POST':
        food = get_object_or_404(FoodItems, id=id)
        quantity = int(request.POST.get('quantity', 1))
        size_id = request.POST.get('size')
        base_id = request.POST.get('base')
        sauce_id = request.POST.get('sauce')
        toppings_ids = request.POST.getlist('toppings')
        
        # Create customized cart item
        customized_item = CustomizedCart.objects.create(
            food=food,
            quantity=quantity,
            base_price=food.price
        )
        
        # Add selected options (empty values are ignored)
        if size_id:
            customized_item.size = SizeChart.objects.get(id=size_id)
        if base_id:
            customized_item.base = BaseType.objects.get(id=base_id)
        if sauce_id:
            customized_item.sauce = Sauce.objects.get(id=sauce_id)
        
        customized_item.save()
        
        # Add toppings
        if toppings_ids:
            for topping_id in toppings_ids:
                if topping_id:  # Skip empty values
                    try:
                        topping = Toppings.objects.get(id=topping_id)
                        customized_item.toppings.add(topping)
                    except Toppings.DoesNotExist:
                        pass
        
        # Calculate and save total price
        customized_item.calculate_total_price()
        customized_item.save()
        
        return redirect('cart')
    
    return redirect('customize', id=id) 


def buy_now(request):
    """Process order from cart items"""
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        
        if not customer_name:
            # Redirect back with error message
            return redirect('cart')
        
        try:
            # Get cart items
            regular_cart_items = list(Cart.objects.all())
            customized_cart_items = list(CustomizedCart.objects.all())
            
            # Check if cart is empty
            if not regular_cart_items and not customized_cart_items:
                return redirect('cart')
            
            # Calculate total price
            regular_total = sum(item.total_price for item in regular_cart_items)
            customized_total = sum(float(item.total_price) for item in customized_cart_items)
            grand_total = regular_total + customized_total
            
            # Create Order with auto-generated order_id
            order = Order.objects.create(
                customer_name=customer_name,
                total_price=grand_total,
                status='PENDING',
                user=request.user if request.user.is_authenticated else None,
            )
            
            # Add regular cart items to order
            for item in regular_cart_items:
                OrderItem.objects.create(
                    order=order,
                    food=item.food,
                    quantity=item.quantity,
                    price=item.total_price,
                    is_customized=False,
                    customization_details=''
                )
            
            # Add customized cart items to order
            for item in customized_cart_items:
                # Create customization details JSON
                customization = {
                    'size': item.size.size_type if item.size else None,
                    'base': item.base.base_name if item.base else None,
                    'sauce': item.sauce.sname if item.sauce else None,
                    'toppings': [t.topping_name for t in item.toppings.all()]
                }
                
                OrderItem.objects.create(
                    order=order,
                    food=item.food,
                    quantity=item.quantity,
                    price=item.total_price,
                    is_customized=True,
                    customization_details=json.dumps(customization)
                )
            if customer_email:
                order.customer_email = customer_email
                order.save()
            
            # Do NOT clear the cart yet — keep items until payment completes
            # Redirect to payment page so user can complete payment for this order
            return redirect('payment_page', order_id=order.id)
            
        except Exception as e:
            print(f"Error creating order: {str(e)}")
            return redirect('cart')
    
    return redirect('cart')



def order_confirmation(request, order_id):
    """Display order confirmation with unique order ID"""
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'foods/order_confirmation.html', context)


def cart_count(request):
    """API endpoint to get current cart count"""
    regular_count = Cart.objects.count()
    customized_count = CustomizedCart.objects.count()
    total_count = regular_count + customized_count
    
    return JsonResponse({'count': total_count})


def order_status(request, order_id):
    """View order status and details"""
    try:
        order = Order.objects.get(order_id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        
        # Calculate totals
        items_total = sum(item.price * item.quantity for item in order_items)
        
        context = {
            'order': order,
            'order_items': order_items,
            'items_total': items_total,
            'items_count': len(order_items)
        }
        return render(request, 'foods/order_status.html', context)
    except Order.DoesNotExist:
        return render(request, 'foods/order_not_found.html', {'order_id': order_id})


def payment_page(request, order_id):
    """Display payment page for the order"""
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        
        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(request, 'foods/payment.html', context)
    except Order.DoesNotExist:
        return redirect('cart')


def process_payment(request, order_id):
    """Process payment and update order status"""
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)
            
            # Get payment details from form
            payment_method = request.POST.get('payment_method', 'CARD')
            
            # Simulate payment processing
            # In production, integrate with actual payment gateway (Razorpay, Stripe, etc.)
            
            # Determine status based on method — simulate immediate success for COD
            # and assume CARD/UPI/WALLET succeed in this simulation.
            order.status = 'PROCESSING'
            order.save()

            # Clear the cart only after successful payment
            Cart.objects.all().delete()
            CustomizedCart.objects.all().delete()

            # Redirect to payment success page
            return redirect('payment_success', order_id=order.id)
            
        except Order.DoesNotExist:
            return redirect('cart')
    
    return redirect('payment_page', order_id=order_id)


def payment_success(request, order_id):
    """Display payment success page and clear cart"""
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
                # ── Send confirmation email ──────────────────────
        if order.customer_email:
            try:
                # Build items summary
                items_text = '\n'.join([
                    f"  • {item.food.name} x{item.quantity}  —  ₹{item.price}"
                    for item in order_items
                ])

                message = f"""
Hi {order.customer_name}! 👋

Your order has been placed successfully! 🎉

━━━━━━━━━━━━━━━━━━━━━━━━
  ORDER #{order.id} SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━

{items_text}

━━━━━━━━━━━━━━━━━━━━━━━━
  TOTAL :  ₹{order.total_price}
  STATUS:  {order.status}
━━━━━━━━━━━━━━━━━━━━━━━━

We are preparing your food now 🔥
Estimated delivery: 30–45 minutes.

Thank you for ordering with FoodDrop! 🍕
— The FoodDrop Team
                """.strip()

                send_mail(
                    subject=f'🍕 Order Confirmed! — Order #{order.id}',
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.customer_email],
                    fail_silently=True,   # won't crash the page if email fails
                )
            except Exception as e:
                print(f"Email failed: {e}")
        # ── End email ────────────────────────────────────
        
        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(request, 'foods/payment_success.html', context)
    except Order.DoesNotExist:
        return redirect('cart')


def order_history(request):
    """Display all past orders for user"""
    # Get all orders (in production, filter by logged-in user)
    all_orders = Order.objects.all().order_by('-created_at')
    
    context = {
        'orders': all_orders,
    }
    return render(request, 'foods/order_history.html', context)


def order_tracking(request, order_id):
    """Display detailed order tracking with live status"""
    try:
        order = Order.objects.get(order_id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        
        # Define status stages
        status_stages = {
            'PENDING': {'label': 'Order Placed', 'step': 1},
            'PROCESSING': {'label': 'Processing', 'step': 2},
            'COMPLETED': {'label': 'Delivered', 'step': 3},
            'CANCELLED': {'label': 'Cancelled', 'step': 0},
        }
        
        current_status = order.status
        current_step = status_stages.get(current_status, {}).get('step', 0)
        
        context = {
            'order': order,
            'order_items': order_items,
            'status_stages': status_stages,
            'current_step': current_step,
        }
        return render(request, 'foods/order_tracking.html', context)
    except Order.DoesNotExist:
        return render(request, 'foods/order_not_found.html', {'order_id': order_id})

# For searching.
from django.db.models import Q  # add this to your existing imports at the top

def SearchFood(request):
    query = request.GET.get('q', '').strip()
    foods = FoodItems.objects.none()

    if query:
        foods = FoodItems.objects.filter(
            Q(name__icontains=query) |          # matches food name
            Q(desc__icontains=query) |          # matches description
            Q(category__icontains=query)        # matches category (Pizza, Burger etc.)
        ).distinct()

    return render(request, 'foods/search.html', {
        'foods': foods,
        'query': query,
    })



# ---------------------------------------------------------

#   For Wishlist 
@login_required(login_url='login')
def toggle_wishlist(request, food_id):
    food = get_object_or_404(FoodItems, id=food_id)

    # get_or_create returns (object, created_bool)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        food=food
    )

    if not created:
        # already in wishlist → remove it
        wishlist_item.delete()
        added = False
        message = f'"{food.name}" removed from wishlist.'
    else:
        added = True
        message = f'"{food.name}" added to wishlist!'

    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'added': added,
            'food_name': food.name,
            'message': message,
        })
    
    messages.success(request, message)
    # go back to the page that triggered this
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', 'wishlist'))
    return redirect(next_url)


@login_required(login_url='login')
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related('food')
    return render(request, 'foods/wishlist.html', {'items': items})


@login_required(login_url='login')
def wishlist_to_cart(request, food_id):
    food = get_object_or_404(FoodItems, id=food_id)

    # add to cart
    cart_item, created = Cart.objects.get_or_create(
        food=food,
        defaults={'quantity': 1, 'total_price': food.price}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * food.price
        cart_item.save()

    # remove from wishlist
    Wishlist.objects.filter(user=request.user, food=food).delete()

    messages.success(request, f'"{food.name}" moved to cart!')
    return redirect('wishlist')


# DashBoard view for admin to see order stats.
@staff_member_required(login_url='login')
def owner_dashboard(request):
    all_orders = Order.objects.all().order_by('-created_at')
    total_orders    = all_orders.count()
    total_revenue   = all_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_customers = User.objects.filter(is_staff=False).count()
    pending_orders  = all_orders.filter(status='PENDING').count()
    processing      = all_orders.filter(status='PROCESSING').count()
    completed       = all_orders.filter(status='COMPLETED').count()
    cancelled       = all_orders.filter(status='CANCELLED').count()
    recent_orders   = all_orders[:10]
    top_foods = (
        OrderItem.objects
        .values('food__name', 'food__category')
        .annotate(total_qty=Sum('quantity'), order_count=Count('id'))
        .order_by('-total_qty')[:5]
    )
    context = {
        'total_orders':    total_orders,
        'total_revenue':   total_revenue,
        'total_customers': total_customers,
        'pending_orders':  pending_orders,
        'processing':      processing,
        'completed':       completed,
        'cancelled':       cancelled,
        'recent_orders':   recent_orders,
        'top_foods':       top_foods,
    }
    return render(request, 'dashboard/owner_dashboard.html', context)


@staff_member_required(login_url='login')
def order_detail_view(request, order_id):
    order       = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order).select_related('food')
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['PENDING', 'PROCESSING', 'COMPLETED', 'CANCELLED']:
            order.status = new_status
            order.save()
            messages.success(request, f'Order {order.order_id} updated to {new_status}.')
        return redirect('order_detail_view', order_id=order.id)
    return render(request, 'dashboard/order_detail.html', {
        'order':       order,
        'order_items': order_items,
    })


@staff_member_required(login_url='login')
def customer_list_view(request):
    customers = (
        User.objects
        .filter(is_staff=False)
        .annotate(order_count=Count('order'))
        .order_by('-date_joined')
    )
    return render(request, 'dashboard/customer_list.html', {
        'customers': customers,
    })


@staff_member_required(login_url='login')
def customer_detail_view(request, user_id):
    customer     = get_object_or_404(User, id=user_id)
    orders       = Order.objects.filter(
        customer_name__icontains=customer.username
    ).order_by('-created_at')
    total_spent  = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = orders.count()
    return render(request, 'dashboard/customer_detail.html', {
        'customer':     customer,
        'orders':       orders,
        'total_spent':  total_spent,
        'total_orders': total_orders,
    })