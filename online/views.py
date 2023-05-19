from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Cart, Customer, OrderPlaced, Product, Wishlist
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required

                                                          


# Create your views here.
def home(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, "online/home.html", locals())


def about(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, "online/about.html", locals())


def contact(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, "online/contact.html", locals())


class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values("title")
        return render(request, "online/category.html", locals())


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values("title")
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, "online/category.html", locals())


class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, "online/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, "online/customerregistration.html", locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations!! Registered Successfully")
        else:
            messages.error(request, "Invalid Data")
        return render(request, "online/customerregistration.html", locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, "online/profile.html", locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            mobile = form.cleaned_data["mobile"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]

            reg = Customer(
                user=user,
                name=name,
                locality=locality,
                mobile=mobile,
                city=city,
                zipcode=zipcode,
                state=state,
            )
            reg.save()
            messages.success(request, "Congratulations!! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "online/profile.html", locals())


def addres(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, "online/address.html", locals())


class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, "online/updateaddress.html", locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data["name"]
            add.locality = form.cleaned_data["locality"]
            add.city = form.cleaned_data["city"]
            add.mobile = form.cleaned_data["mobile"]
            add.state = form.cleaned_data["state"]
            add.zipcode = form.cleaned_data["zipcode"]
            add.save()
            messages.success(request, "Congratulations!! Address Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        # The product already exists in the cart, update the quantity
        cart_item.quantity += 1
        cart_item.save()
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount * 1.05
    return render(request, "online/addtocart.html", locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    product= Wishlist.objects.filter(user=user)
    return render(request, "online/wishlist.html", locals())

class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount * 1.05
        return render(request, "online/checkout.html", locals())

@login_required
def orders(request):
    orders_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, "online/orders.html", locals())


# cart=Cart.objects.filter(user=user)
# for c in cart:
#     OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
#     c.delete()
#     return redirect("orders")

@login_required
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount * 1.05
        formatted_totalamount = "{:.2f}".format(totalamount)
        data = {"quantity": c.quantity, "amount": amount, "totalamount": formatted_totalamount}
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount * 1.05
        formatted_totalamount = "{:.2f}".format(totalamount)
        data = {"quantity": c.quantity, "amount": amount, "totalamount": formatted_totalamount}
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount * 1.05
        data = {"amount": amount, "totalamount": totalamount}
        return JsonResponse(data)

@login_required
def plus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        product = get_object_or_404(Product, id=prod_id)
        user = request.user
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
        
        if not created:
            # Wishlist item already exists
            data = {
                "message": "Product already exists in the wishlist",
            }
            return JsonResponse(data)
        
        data = {
            "message": "Product added to the wishlist successfully",
        }
        return JsonResponse(data)

@login_required
def minus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            "message": "Wishlist Remove Successfully",
        }
        return JsonResponse(data)
    
@login_required
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    products = Product.objects.filter(Q(title__icontains=query))
    return render(request, "online/search.html", locals())
