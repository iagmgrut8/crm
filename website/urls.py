from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    # path('login/', views.login_user, name='התחברות'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

]