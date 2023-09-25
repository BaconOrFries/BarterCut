from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import *
from .form import *
from fypcore.models import *

# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'listing/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.listed_by = request.user
            item.save()

            category = item.category
            category.item_count += 1 
            category.save()

            return redirect('listing:detail', pk=item.id)

    else:
        form = CreateListingForm()

    return render(request, 'listing/create.html', {
        'form': form,
        'title': 'Create Listing',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, listed_by=request.user)
    item.delete()

    return redirect('dashboard:index')

@login_required
def edit_listing(request, pk):
    item = get_object_or_404(Item, pk=pk, listed_by=request.user)

    if request.method == 'POST':
        form = EditListingForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('listing:detail', pk=item.id)
    else:
        form = EditListingForm(instance=item)

    return render(request, 'listing/create.html', {
        'form': form,
        'title': 'Edit Listing',
    })

def listings(request):
    query = request.GET.get('query', '')
    categories = Category.objects.all()

    # Include "Sold" items only if the user is viewing the "Completed Transactions"
    if request.path == '/completed-transactions/':  # Adjust the URL as needed
        items = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), is_sold=True)
    else:
        items = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), is_sold=False)

    category_id = request.GET.get('category', 0)

    if category_id:
        items = items.filter(category_id=category_id)

    return render(request, 'listing/listings.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })


@login_required
def barter_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    seller = item.listed_by
    buyer = request.user

    # Access the AppUser instances for the seller and buyer
    seller_app_user = AppUser.objects.get(user=seller)
    buyer_app_user = AppUser.objects.get(user=buyer)

    if buyer_app_user.point >= item.point:
        # Deduct points from the buyer
        buyer_app_user.point -= item.point
        buyer_app_user.save()

        # Add points to the seller
        seller_app_user.point += item.point
        seller_app_user.save()

        # Mark the item as sold
        item.is_sold = True
        item.transaction_status = 'Sold'
        item.received_by = buyer
        item.save()

        # Decrement the count in the respective category
        category = item.category
        category.item_count = category.item_count - 1 
        category.save()

        transaction = Transaction(user=request.user, status='completed')
        transaction.save()

        return redirect('dashboard:index')
    else:
        # Handle case where the buyer doesn't have enough points
        messages.info(request, 'You do not have enough points')
        return HttpResponseRedirect('/dashboard')