from django.urls import path

from . import views

app_name = 'message'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('message/<int:item_pk>', views.new_conversation, name='message'),
    path('<int:pk>/', views.details, name='details'),
]