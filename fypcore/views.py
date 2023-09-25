from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from listing.models import *
from .models import *
from .form import *

# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.filter(item_count__gt=0).order_by('-item_count')[:3]
    return render(request, 'fypcore/index.html', {'categories': categories, 'items':items,})

def contact(request):
    return render(request, 'fypcore/contact.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                user = form.save()
                app_user = AppUser(user=user)
                app_user.save()

                return redirect('/login/')

    return render(request,'fypcore/register.html', {
        'form': form
    })

def terms(request):
    return render(request, 'fypcore/terms.html')

def policy(request):
    return render(request, 'fypcore/policy.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/login/')