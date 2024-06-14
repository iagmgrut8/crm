from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record, status_choices, SOURCE_CHOICES
from datetime import datetime

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d/%m/%Y'
    
    def __init__(self, *args, **kwargs):
        kwargs['format'] = self.format
        super().__init__(*args, **kwargs)
    
    def format_value(self, value):
        if value is not None and isinstance(value, datetime):
            return value.strftime(self.format)
        return super().format_value(value)

class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"שם פרטי", "class":"form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"שם משפחה", "class":"form-control"}), label="")
    phone = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"טלפון", "class":"form-control"}), label="")
    date_of_interview = forms.DateField(required=True, widget=DateInput(attrs={"placeholder":"תאריך ראיון", "class":"form-control"}), label="")
    hour_of_interview = forms.TimeField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"שעת ראיון", "class":"form-control"}), label="")
    source = forms.ChoiceField(
        choices=SOURCE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            "class": "form-control",
        }), label=""
    )
    status = forms.ChoiceField(
        choices=status_choices,
        required=True,
        widget=forms.Select(attrs={
            "class": "form-control",
        }), label="סטטוס"
    )
    notes = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"הערות", "class":"form-control"}), label="")
    
    class Meta:
        model = Record
        exclude = ('user',)

class DateInput(forms.DateInput):
    input_type = 'date'
    widget = DateInput(attrs={
        "placeholder": "תאריך ראיון",
        "class": "form-control"
    })

class EditRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['first_name', 'last_name', 'phone', 'date_of_interview', 'hour_of_interview', 'source', 'status', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'שם פרטי'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'שם משפחה'}),
            'date_of_interview': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'תאריך ראיון'}),
            'hour_of_interview': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'שעת ראיון'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'הערות'}),
        }
        labels = {
            'date_of_interview': '',
            'hour_of_interview': '',
            'source': '',
            'status': '',
            'notes': '',
        }

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', required=False)

    def search_records(self):
        query = self.cleaned_data.get('search_query')
        if query:
            # Customize the filtering based on your fields
            records = Record.objects.filter(
                first_name__icontains=query,
                last_name__icontains=query,
                phone__icontains=query,
                date_of_interview__icontains=query,
                hour_of_interview__icontains=query,
                source__icontains=query,
                status__icontains=query,
                notes__icontains=query
            )
            return records
        else:
            return Record.objects.none()