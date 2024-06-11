from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "התחברות בוצעה בהצלחה")
            return redirect('Home')
        else:
            messages.success(request, "שגיאה בהתחברות")
            return redirect('Home')
    else:
        return render (request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "התנתקת בהצלחה")
    return redirect('Home')

def register_user(request):
    return render (request, 'register.html', {})
