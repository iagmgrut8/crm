from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='Home'),
    # path('login/', views.login_user, name='התחברות'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.costumer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('edit/<int:pk>/', views.edit_record, name='edit_record'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('search/', views.search_records, name='search_records'),
    path('statistics/', views.statistics, name='statistics'),
    
    
    
    ]