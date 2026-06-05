from django.urls import path
from learnapp import views
# from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.registration, name='register'),
    path('login/', views.user_login , name='login'),
    path('home', views.home, name='home'),
    path('logout', views.user_logout, name='logout'),
    path('profile',views.userprofile, name='profile'),
    path('update',views.userupdate, name='update'),
    # path('accounts/login/',LoginView.as_view(template_name='login.html'),name='login')
    path('test-email/', views.test_email, name='test_email'),

]