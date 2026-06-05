"""
URL configuration for LEARNING project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include 
from learnapp import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from foods import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', include('learnapp.urls')),
    path('foods/', include('foods.urls')),
    # path('<int:id>',views.AllFoods), 
    path('<int:id>',views.Food_Details),
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls'))
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard/orders/<int:order_id>/', views.order_detail_view, name='order_detail_view'),
    path('dashboard/customers/',  views.customer_list_view, name='customer_list'),
    path('dashboard/customers/<int:user_id>/', views.customer_detail_view, name='customer_detail'),
    
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
