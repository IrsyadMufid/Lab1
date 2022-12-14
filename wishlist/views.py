from django.shortcuts import render
from wishlist.models import ItemWishlist
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_wishlist_item = ItemWishlist.objects.all()
    context = {
    'list_item': data_wishlist_item  ,
    'name': 'Irsyad Mufid',
    'last_login': request.COOKIES['last_login'],
}

    return render(request, "wishlist.html", context)

@login_required(login_url='/wishlist/login/')
def show_wishlist_ajax(request):
    data_wishlist_item = ItemWishlist.objects.all()
    context = {
    'name': 'Irsyad Mufid',
    'last_login': request.COOKIES['last_login'],
}
    return render(request, "wishlist_ajax.html",context)

@csrf_exempt
@login_required(login_url="/wishlist/login/")
def add_wishlist_ajax(request):
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        print(item_name)
        item_price = request.POST.get("item_price")
        description = request.POST.get("description")
        ItemWishlist.objects.create(
            item_name = item_name, item_price = item_price, description = description
        )
        JsonResponse({}, status=200)
    return redirect("wishlist:show_wishlist_ajax")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context) 

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)   


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    response.delete_cookie('last_login')
    return response


def show_xml(request):
    data = ItemWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = ItemWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(requst, id):
    data = ItemWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(requst, id):
    data = ItemWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
