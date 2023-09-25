from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from listing.models import *
from fypcore.models import Transaction
# Create your views here.

@login_required
def index(request):
    listed_items = Item.objects.filter(listed_by=request.user, transaction_status='Listed')
    sold_items = Item.objects.filter(listed_by=request.user, transaction_status='Sold')
    received_items = Item.objects.filter(received_by=request.user, transaction_status='Sold')

    return render(request, 'dashboard/index.html', {
        'listed_items': listed_items,
        'sold_items': sold_items,
        'received_items': received_items,
    })