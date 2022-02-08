from django.shortcuts import render,HttpResponse, redirect
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
from django.contrib import messages 
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'Your-Merchant-Key-Here'

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)
def shop(request): 
    return render(request, "shop/basic.html")

def searchMatch(query, item):
    if query in item.product_name or query in item.subcategory or query in item.desc or query in item.category:
        return True
    else:
        return False

def basic(request):
    return(render,"shop/basic.html")


def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
       

    return render(request, 'shop/checkout.html')




def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST.get('username')
        email=request.POST.get('email')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

         # check for errorneous input
        

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return render(request,'shop/about.html')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return render(request,'shop/about.html')

        # check for errorneous input
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return render(request,'shop/about.html')

    else:
        return HttpResponse("404 - Not found")
    
    



def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST.get('loginusername')
        loginpassword=request.POST.get('loginpassword')

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return render(request,'shop/about.html')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return render(request,'shop/about.html')

    return HttpResponse("404- Not found")
    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return render(request,'shop/about.html')

def payment(request):
    return render(request,"shop/paytm.html")