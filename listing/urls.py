from django.urls import path

from . import views

app_name = 'listing'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit', views.edit_listing, name='edit_listing'),
    path('create/', views.create_listing, name='create_listing'),
    path('barter/<int:pk>/', views.barter_item, name='barter_item'),
    path('', views.listings, name='listings')
]