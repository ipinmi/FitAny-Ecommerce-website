from django.shortcuts import render 
from django.http import JsonResponse, HttpResponse, request, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
import json
from ecommerce import settings
import datetime 
from .models import *
from users.models import *
from store.forms import SearchForm
from .utils import cookieCart, cartData, guestOrder
# Create your views here.
#rendering templates created
def homepage(request):

    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    # setting = Setting.objects.get(pk=1)
    #linking the return values in cartData to models.py
    data = cartData(request)
    cartItems = data['cartItems']
    category = Category.objects.all()

    context = {'cartItems': cartItems, 'category':category}
    return render(request, 'store/home.html', context)

def store(request):
    
    #linking the return values in cartData to models.py
    data = cartData(request)
    cartItems = data['cartItems']
    category = Category.objects.all()
    products = Product.objects.all()
    context = {'products':products, 'cartItems': cartItems, 'category':category}
    return render(request, 'store/store.html', context)

# to keep details of the last currency chosen
def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(lasturl)

# to show the full path of the catergory mptt and product details
def category_products(request, id, slug):
    #linking the return values in cartData to models.py
    data = cartData(request)
    cartItems = data['cartItems']
    category = Category.objects.all()
    catdata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)

    context = {'cartItems': cartItems, 'products':products, 'category':category, 'catdata':catdata}
    
    return render(request, 'store/category_products.html', context)

# search products from navbar
def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            context = {'products': products, 'query':query,
                       'category': category }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')

def cart(request):

    #linking the return values in cartData to models.py
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category = Category.objects.all()


    context = {'items':items, 'order':order, 'cartItems': cartItems, 'category':category}
    return render(request, 'store/cart.html', context)

def productpage(request, id, slug):
    data = cartData(request)
    cartItems = data['cartItems']
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = ProductImage.objects.filter(product_id=id)
   
    context = { 'cartItems': cartItems,  'category':category, 'product':product, 'images': images}
    return render(request, 'store/productpage.html', context)


def checkout(request):
    
    #linking the return values in cartData to models.py
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category = Category.objects.all()


    context = {'items':items, 'order':order, 'cartItems': cartItems, 'category':category}
    return render(request, 'store/checkout.html', context)

#when a user clicks "add to cart " this function confirms the addition of the data
def updateItem(request):
    #to parse the string data from the json response in the fecth function
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action'] 

    print('Action:', action)
    print('productId:', productId)

    #creating an order
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    #attach an order to a customer 
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
   
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    #remove order if quantity is below zero 
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    # creating a trans id
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    # for guest and authenicated uswer
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
        
    else:
        customer, order = guestOrder(request, data)
    
    # to get the total value from userdataform object 
    total = float(data['user-form']['total'])
    order.transaction_id = transaction_id

    # to avoid data manipulation 
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    # creating shipping address object
    if order.shipping == True:
        # for each model in models.py
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            # address2=data['shipping']['address2'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    print('Data:', request.body)
    return JsonResponse('Payment Complete', safe=False)