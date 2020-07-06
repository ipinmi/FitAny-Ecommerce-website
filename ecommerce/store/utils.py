import json
from .models import *

def cookieCart(request):
     # dummy value for  first guest user 
    try:
        cart = json.loads(request.COOKIES['cart'])
    except: 
        cart = {}
        print('Cart', cart)

    items = []
    #manually create a value for unauthenticated user
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    # loop through the cart items
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            # querying the products 
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            # creating the order 
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            # dictionary representation of the guest cart items 
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]["quantity"],
                'get_total': total,
            }
            # to append this dictionary to the main "items"
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except: 
            pass

    return {'cartItems':cartItems ,'order':order, 'items':items}

# function for user authentication
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
         #get all the orderitems that have that particular order as their parent
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        #linking the return values in cookie cart to models.py
       cookieData = cookieCart(request)
       cartItems = cookieData['cartItems']
       order = cookieData['order']
       items = cookieData['items']
    return {'cartItems':cartItems ,'order':order, 'items':items}

def guestOrder(request, data):
    print('User is not logged in')
    # print out the cookies
    print('COOKIES', request.COOKIES)
    firstName = data['user-form']['firstName']
    lastName = data['user-form']['lastName']
    email = data['user-form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    # create the guest customer
    customer, created = Customer.objects.get_or_create(
        # to keep record of the customers order instead of creating a new user
        email=email, 
    )
    customer.firstName = firstName
    customer.lastName = lastName
    customer.save()

    # create order
    order = Order.objects.create(
        customer=customer,
        complete= False,
    )
    # adding to the DB 
    for item in items:
        # get the product from items dictionary in the util.py
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order