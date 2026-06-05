from django.urls import path
from foods import views

urlpatterns =[
   path('allfoods',views.AllFoods,name='allfoods'),
   path('<int:id>',views.Food_Details,name='fooddetails'),
   # path('fooddetails/<int:id>/',views.Food_Details,name='fooddetails'),
   path('addnewfood',views.AddNewFood,name='addnewfood'),
   path('cart/<int:id>',views.AddToCart,name='addtocart'),
   path('cart',views.cart_view,name='cart'),
   path('cart/delete/<int:id>/',views.delete_from_cart,name='delete_from_cart'),
   path('cart/update-quantity/<int:id>/',views.update_quantity,name='update_quantity'),
   path('customize/<int:id>/',views.Customize_Food, name='customize'),
   path('customize/save/<int:id>/',views.save_customization,name='save_customization'),
   path('cart/delete-customized/<int:id>/',views.delete_customized_item,name='delete_customized_item'),
   path('cart/update-customized-quantity/<int:id>/',views.update_customized_quantity,name='update_customized_quantity'),
   path('buy-now/', views.buy_now, name='buy_now'),
   path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
   path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
   path('process-payment/<int:order_id>/', views.process_payment, name='process_payment'),
   path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
   path('order-status/<str:order_id>/', views.order_status, name='order_status'),
   path('order-history/', views.order_history, name='order_history'),
   path('order-tracking/<str:order_id>/', views.order_tracking, name='order_tracking'),
   path('api/cart-count/', views.cart_count, name='cart_count'),
   path('search/', views.SearchFood, name='search'),
   # path('place-order/', views.PlaceOrder, name='placeorder'),
   path('food/<int:food_id>/review/', views.add_review, name='add_review'),
   path('wishlist/',views.wishlist_view,name='wishlist'),
   path('wishlist/toggle/<int:food_id>/', views.toggle_wishlist,  name='toggle_wishlist'),
   path('wishlist/to-cart/<int:food_id>/',  views.wishlist_to_cart, name='wishlist_to_cart'),
   

]
