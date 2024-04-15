from django.shortcuts import render

# Create your views here.

def LogIn(request):
    return render(request, 'users/log_in.html')

def registration(request):
    return render(request, 'users/registration.html')

def profile(request):
    return render(request, 'users/user_page.html')