from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .form import LoginForm

app_name = 'fypcore'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='fypcore/login.html',authentication_form=LoginForm), name='login'),
    path('terms/', views.terms, name='terms'),
    path('policy/', views.policy, name='policy'),
    path('logout/', views.user_logout, name='logout'),
]