from django.shortcuts import render,redirect
from learnapp.forms import User, UserDetails, UserForm
from learnapp.forms import UserProfileForm, UserUpdateForm, UserProfileUpdateForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from foods.models import FoodItems

# Create your views here.
def registration(request):
    registered = False
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = UserProfileForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            profile = form2.save(commit=False)
            profile.user = user #Committing two models to have the final data
            profile.save()
            registered = True
    else:
        form1 = UserForm()
        form2 = UserProfileForm()
    context = {
        'form1': form1, 
        'form2': form2,
        'registered': registered
    }
    return render(request, 'registration.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return render(request, "login.html", {'error_message': 'Please enter both username and password'})
        
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect("home")
            else:
                return HttpResponse("Your account is disabled.")
        else:
            # print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    return render(request, 'login.html')

@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def home(request):
    allfood = FoodItems.objects.all()
    top_rated_foods = FoodItems.objects.filter(rating__gte=4).order_by('-rating')[:6]
    popular_foods = FoodItems.objects.order_by('-rating')[:6]
    return render(request, 'home.html', {
        'allfood': allfood,
        'top_rated_foods': top_rated_foods,
        'popular_foods': popular_foods
    })

@login_required(login_url="login")
def userprofile(request):
    return render(request, 'profile.html')          

@login_required(login_url="login")
def userupdate(request):
    if request.method=='POST':
        form=UserUpdateForm(request.POST,instance=request.user)
        form1=UserProfileUpdateForm(request.POST,request.FILES,instance=request.user.userdetails)
        if form.is_valid() and form1.is_valid():
            user=form.save()
            user.save()

            profile=form1.save(commit=False)
            profile.user=user
            profile.save()                                           
        return redirect("profile")
    else:
        form=UserUpdateForm(instance=request.user)
        form1=UserProfileUpdateForm(instance=request.user.userdetails)
    context={
        'form':form,
        'form1':form1
    }
    return render(request, 'update.html',context)
    
def test_email(request):
    from django.core.mail import send_mail
    from django.conf import settings
    try:
        send_mail(
            subject='FoodApp Test Email',
            message='If you see this, email is working!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['your_gmail@gmail.com'],  # ← your own email
            fail_silently=False,
        )
        from django.http import HttpResponse
        return HttpResponse('✅ Email sent successfully! Check your inbox.')
    except Exception as e:
        from django.http import HttpResponse
        return HttpResponse(f'❌ Email failed: {str(e)}')