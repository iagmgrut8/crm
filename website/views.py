import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, EditRecordForm, SearchForm
from django.db.models import Count
from .models import Record
import csv
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from facebook_scraper import get_posts
from urllib.parse import quote



def home(request):
    records = Record.objects.all()

    # Apply sorting
    sort_by = request.GET.get('sort_by', 'id')
    records = records.order_by(sort_by)

    # Apply filtering
    status_filter = request.GET.get('status', None)
    if status_filter:
        records = records.filter(status=status_filter)
        
    # Handle search form
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('q')
        if search_query:
            records = records.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(source__icontains=search_query) |
                Q(status__icontains=search_query) |
                Q(date_of_interview__icontains=search_query) |
                Q(hour_of_interview__icontains=search_query) |
                Q(notes__icontains=search_query)
            )

    # Handle AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('partials/records_table.html', {'records': records})
        return JsonResponse({'html': html})

    # Handle POST request for login
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "התחברות בוצעה בהצלחה")
            return redirect('Home')  # Redirect to the same view after login
        else:
            messages.error(request, "שגיאה בהתחברות")
            return redirect('Home')  # Redirect to the same view after failed login

    # Handle regular GET request
    else:
        return render(request, 'home.html', {'records': records, 'search_form': search_form})


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
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def costumer_record(request, pk):
    if request.user.is_authenticated:
        costumer_record = get_object_or_404(Record, id=pk)
        return render(request, 'record.html', {'costumer_record': costumer_record})
    else:
        messages.success(request, "יש לבצע התחברות")
        return redirect('Home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = get_object_or_404(Record, id=pk)
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


def edit_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    if request.method == 'POST':
        form = EditRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record', pk=record.id)
    else:
        form = EditRecordForm(instance=record)
    return render(request, 'edit_record.html', {'form': form, 'record': record})


def export_csv(request):
    # Retrieve your data (e.g., from the Record model)
    records = Record.objects.all()

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="records.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Phone', 'Source', 'Status', 'Date of Interview', 'Hour of Interview', 'Notes'])  # Add column headers

    for record in records:
        writer.writerow([record.id, record.first_name, record.last_name, record.phone, record.source, record.status, record.date_of_interview, record.hour_of_interview, record.notes])  # Add data rows

    return response

def search_records(request):
    # Retrieve all records from the database
    records = Record.objects.all()

    # Apply any additional filters based on the specified fields
    search_query = request.GET.get('q', '')  # Get the search query from the URL parameter
    if search_query:
        records = records.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(source__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(date_of_interview__icontains=search_query) |
            Q(hour_of_interview__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    # Other logic (sorting, authentication, etc.) can be added here

    return render(request, 'search_results.html', {'records': records})

def statistics(request):
    # Count records by status and source
    data = Record.objects.values('status', 'source').annotate(count=Count('id'))

    # Calculate total count of records
    total_count = Record.objects.count()

    # Prepare data for Chart.js
    labels = set()
    status_counts = {}
    for entry in data:
        status = entry['status']
        source = entry['source']
        count = entry['count']
        if status not in status_counts:
            status_counts[status] = {}
        status_counts[status][source] = count
        labels.add(source)

    labels = list(labels)
    datasets = []
    for status, counts in status_counts.items():
        counts_list = []
        for label in labels:
            counts_list.append(counts.get(label, 0))
        percentages = [(count / total_count) * 100 if total_count > 0 else 0 for count in counts_list]
        datasets.append({
            'label': status,
            'data': percentages,
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',  # Example color
            'borderColor': 'rgba(54, 162, 235, 1)',       # Example border color
            'borderWidth': 1,
        })

    context = {
        'labels': labels,
        'datasets': datasets,
        'animation_config': {
            'onComplete': 'onAnimationComplete',
            'delay': 'onAnimationDelay'
        }
    }
    return render(request, 'statistics.html', context)
