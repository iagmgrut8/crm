from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()
    
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
        return render (request, 'home.html', {'records':records})

def logout_user(request):
    logout(request)
    messages.success(request, "התנתקת בהצלחה")
    return redirect('Home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "התחברת בהצלחה")
            return redirect('Home')
    else:
        form = SignUpForm()
        return render (request, 'register.html', {'form':form})

    return render (request, 'register.html', {'form':form})

def costumer_record(request, pk):
    if request.user.is_authenticated:
        costumer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'costumer_record':costumer_record})
    else:
        messages.success(request, "יש לבצע התחברות")
        return redirect('Home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "נמחק בהצלחה")
        return redirect('Home')
    
    else:
        messages.success(request, "נא להתחבר")
        return redirect('Home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "נוסף בהצלחה")
                return redirect('Home')
        # Pass the form instance to the template context
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "עליך להתחבר")
        return redirect('Home')

    