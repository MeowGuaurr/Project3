from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from decimal import Decimal
from .models import *
from .models import Completed_Order

# Create your views here.


def index(request):
    # verify if user already did login
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"error": "Invalid Username"})
    # return menu
    context = {
        'types': Type.objects.all(),
        'inventory': Inventory.objects.all(),
        'extra_allowed_count': 3,
        'size':  Size.objects.all(),
        'toppings': Topping.objects.all()
    }
    return render(request, "orders/index.html", context)

# def addItem_view(request):
#     try:
#         item_id = request.POST['item-id']
#     except:
#         item_id = None
#     try:
#         max_topping = request.POST['max_topping']
#     except:
#         None
#     try:
#         size = request.POST['size-select']
#     except:
#         size = None

#     toppings = []
#     if max_topping:
#         for i in max_topping:
#             try:
#                 top = request.POST[f'select-{i}']
#                 toppings.append(Topping.objects.get(pk=top))
#             except:
#                 pass
#     item = Inventory.objects.get(pk=item_id)

#     cart = Orderr.objects.get(user=request.user)
#     cart_item = Orderr(order_id=cart, item=item)


def add_to_cart(request):
    if request.method == 'POST':
        #getting information that user wants in their order
        size = request.POST["item"]
        topp = request.POST.getlist("toppings-selected")
        cantidad = request.POST["qty"]
        cart_item = ItemCost.objects.get(pk=size)
        item = cart_item.itemcost.get()
        price = cart_item.amount
        number_of_toppings = int(len(topp))
        #initiate order
        to_cart = Orderr.objects.create(
            qty=cantidad, status='Initiated', amount=price, user_id=request.user.id)

        # verify if customizable
        if item.customizable is True:
            for n in topp:
                topping = Topping.objects.get(pk=n)
                to_cart.item_topping.add(topping)

            # loop over toppings
            for c in ToppingCount.objects.all():
                for p in c.inventory.all():
                    if p.id == cart_item.id:
                        # check for number of selected topping
                        if number_of_toppings == int(c.count):
                            # add subs, topping price if exists
                            if str(item.item_type) == "subs":
                                price = price + c.amount
                            else:
                                # not subs then same topping price
                                price = c.amount
        #set price
        price = float(price) * int(cantidad)
        to_cart.item.add(cart_item)
        to_cart.amount = price
        
        #save cart info
        to_cart.save()
        messages.success(request, f'Item: {to_cart} added to cart!')
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "orders/index.html")

#delete in car
def delete_item(request):
    item_id = request.POST["item_id"]  
    Orderr.objects.get(pk=item_id).delete()            
    #return to prev view
    return HttpResponseRedirect('cart')
    
def cart(request):
    #check items and price
    orders =  Orderr.objects.filter(user_id=request.user.id)
    total = Decimal(0)
    #counter for non-empty car
    cart_item_count = 0 
    total_id = []
    #check previous order
    for order in orders:
        if order.status == 'Initiated':
            total_id.append(order.id)
            cart_item_count = len(total_id)
            total += Decimal(order.amount)
    #pass context with cart and orders info
    context = {
        "inventory": Inventory.objects.all(),
        "itemcost": ItemCost.objects.all(),
        "orders": orders,
        "total": total,
        "total_id": total_id,
        "cart_item_count": cart_item_count
    }
    return render(request, 'orders/cart.html', context)

#logout for user
def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message_success": "You Logged out"})

#create a new user
def register(request):
    if request.method == 'GET':
        return render(request, 'orders/register.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["email"]

    except KeyError:
        return render(request, "orders/register.html", {"error": "Invalid Entry"})
    if not username:
        return render(request, "orders/register.html", {"error": "Invalid Username"})
    if not password:
        return render(request, "orders/register.html", {"error": "Invalid Password"})

    check_user = User.objects.filter(username=username)
    if check_user:
        return render(request, "orders/register.html", {"error": "Username already exists, try something else"})
    if User.objects.filter(email=email).exists():
        return render(request, "orders/register.html", {"error": "email already exists, try something else"})
    if len(first_name) < 2:
        return render(request, "orders/register.html", {"error": "First Name must be greater than 2 char"})
    if len(last_name) < 2:
        return render(request, "orders/register.html", {"error": "Last Name must be greater than 2 char"})

    user = User.objects.create_user(
        username=username, first_name=first_name, last_name=last_name, email=email, password=password)
    user.save()
    login(request, user)

 
    messages.success(request, f" Now you're registered!")
    return HttpResponseRedirect(reverse('index'))

#login to user account
def login_view(request):
    if request.method == 'GET':
        return render(request, 'orders/login.html')
    try:
        username = request.POST['username']
        password = request.POST['password']

    except KeyError:
        return render(request, "orders/login.html", {"error": "Invalid Entry"})
    if not username:
        return render(request, "orders/login.html", {"error": "Invalid Username"})
    if not password:
        return render(request, "orders/login.html", {"error": "Invalid Password"})

    user = authenticate(request, username=username, password=password)
    if not user:
        return render(request, 'orders/login.html', {"error": 'Invalid credentials'})
    else:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

#views to see and check orders
def my_orders(request):
    gen_order = Completed_Order.objects.filter(user_id=request.user.id)
    context = {
        "orders": gen_order,
        "admin_orders": Completed_Order.objects.filter(status ="Initiated")
    }
    return render(request, 'orders/orders.html', context)
    
def check_order(request):
    if request.POST["completed"]:
        completed = request.POST["completed"]
        row = Completed_Order.objects.get(pk=completed)
        row.status = 'Completed'
        row.save()

    return HttpResponseRedirect(reverse('my_orders'))
    
#from admin view and confirm orders in list
def confirm_order(request):
    total=request.POST.get("amount")
    order =  Orderr.objects.filter(user_id=request.user.id)
    print(total)
    orderstr = str(order)
    orderstr = orderstr[9:len(orderstr)]
    
    create_order_id = Completed_Order.objects.create(user_id=request.user.id, total=total, order_detail=orderstr)
    create_order_id.save()   
    order.delete()

    messages.success(request, f'Thank you!')
    return HttpResponseRedirect(reverse('index'))