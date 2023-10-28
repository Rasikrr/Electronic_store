from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from .models import CustomUser, Profile, Categories, Product, CartItem, WishListItem
from django.views.generic.edit import CreateView
from .forms import SignupForm
from random import shuffle, sample

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            unique_email = CustomUser.objects.filter(email=cleaned_data.get("email")).exists()
            unique_username = CustomUser.objects.filter(username=cleaned_data.get("username")).exists()
            policy = cleaned_data.get("policy")
            password_1 = cleaned_data.get("password")
            password_2 = cleaned_data.get("password_2")
            if password_1 != password_2:
                messages.info(request, "password_2", "Passwords are not similar")
                return redirect("signup")
            if not policy:
                messages.info(request, "policy", "Please accept policy")
                return redirect("signup")
            if unique_email:
                messages.info(request, "email", "User with this email is exists")
                return redirect("signup")
            if unique_username:
                messages.info(request, "username", "User with this username is exists")
                return redirect("signup")
            email = cleaned_data["email"]
            username = cleaned_data["username"]
            user_obj = CustomUser.objects.create_user(username=username,
                                                      email=email, password=make_password(password_1),
                                                      password_2=make_password(password_2))
            user_obj.save()
            Profile.objects.create(user=user_obj).save()
            login(request, user_obj, backend="core.backends.EmailBackend")
            return redirect("index")

    else:
        form = SignupForm()
    return render(request, "signup.html", context={"form": form})


# Function for search
def search_func(request):
    search_query = request.POST.get("search-bar")
    selected_category = request.POST.get("input-select")
    return redirect("search", product_name=search_query, selected_category=selected_category)


def index(request):
    try:
        user = CustomUser.objects.get(username=request.user.username)
        cart = CartItem.objects.filter(user=user)
    except CustomUser.DoesNotExist:
        user = ""
        cart = ""
    if request.method == "POST":
        return search_func(request)
    else:
        categories = Categories.objects.all()
        all_products = list(Product.objects.all())
        new_products = sample(all_products, 5)
        shuffle(all_products)
        top_selling_1 = all_products[:5]
        top_selling_2 = all_products[6:9]
        top_selling_3 = all_products[9:12]
        top_selling_4 = all_products[12:15]
        return render(request, "index.html", context={"user": user,
                                                      "categories": categories,
                                                      "new_products": new_products,
                                                      "top_selling_1": top_selling_1,
                                                      "top_selling_2": top_selling_2,
                                                      "top_selling_3": top_selling_3,
                                                      "top_selling_4": top_selling_4,
                                                      "cart": cart})


def search(request, product_name, selected_category):
    try:
        user = CustomUser.objects.get(username=request.user.username)
        cart = CartItem.objects.filter(user=user)
    except CustomUser.DoesNotExist:
        user = ""
        cart = ""
    product_name = product_name.capitalize()
    categories = Categories.objects.all()
    if selected_category == "0":
        products = Product.objects.filter(name__icontains=product_name)
    else:
        products = Product.objects.filter(category__name__iexact=selected_category, name__icontains=product_name)
    if request.method == "POST":
        return search_func(request)
    return render(request, "search.html", context={"products": products,
                                                   "user": user,
                                                   "search_query": product_name,
                                                   "categories": categories,
                                                   "cart": cart})


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Email or password is wrong")
            return redirect("signin")
    else:
        return render(request, "signin.html")


@login_required(login_url="signin")
def profile(request, user_id):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    cart = CartItem.objects.filter(user=user)

    if request.method == "POST":
        if not request.POST.get("input-select"):
            first_name = request.POST.get("first-name")
            last_name = request.POST.get("last-name")
            address = request.POST.get("address")
            city = request.POST.get("city")
            country = request.POST.get("country")
            zip_code = request.POST.get("zip-code")
            telephone = request.POST.get("tel")
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.address = address
            user_profile.city = city
            user_profile.country = country
            user_profile.zip_code = zip_code
            user_profile.telephone = telephone
            user_profile.save()
            messages.info(request, "Data is saved")
            return redirect("profile", user_id=user_id)
        else:
            return search_func(request)
    else:
        return render(request, "profile.html", context={"user_profile": user_profile,
                                                        "cart": cart,
                                                        })


@login_required(login_url="signin")
def checkout(request, user_id):
    user = CustomUser.objects.get(username=request.user.username)
    cart = CartItem.objects.filter(user=user)
    user_profile = Profile.objects.get(user=user)

    if request.method == "POST":
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        zip_code = request.POST.get("zip-code")
        telephone = request.POST.get("tel")
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.address = address
        user_profile.city = city
        user_profile.country = country
        user_profile.zip_code = zip_code
        user_profile.telephone = telephone
        user_profile.save()
    else:
        return render(request, "checkout.html", context={"user_profile": user_profile,
                                                         "cart": cart})


def catalog(request):
    try:
        user = CustomUser.objects.get(username=request.user.username)
        cart = CartItem.objects.filter(user=user)
        user_profile = Profile.objects.get(user=user)
    except CustomUser.DoesNotExist:
        user = ""
        cart = ""
        user_profile = ""
    if request.method == "POST":
        return search_func(request)
    products = Product.objects.all()
    top_selling = sample(list(products), 3)
    selected_categories = [category for category in request.GET if request.GET.get(category) and category in ("laptops", "smartphones", "cameras", "accessories")]
    category_filters = Q()
    for cat in selected_categories:
        category_filters |= Q(category__name=cat)
    products = products.filter(category_filters, price__range=(request.GET.get('price-min', 0), request.GET.get('price-max', 5000)))
    print("selected", selected_categories)
    if "sorting" in request.GET:
        print(products)
        sorting_option = request.GET.get("sorting", None)
        if sorting_option == "asc-price":
            products = products.order_by("price")
        elif sorting_option == "desc-price":
            products = products.order_by("-price")
    categories = Categories.objects.all()
    laptops_count = Product.objects.filter(category__name="laptops").count()
    smartphones_count = Product.objects.filter(category__name="smartphones").count()
    cameras_count = Product.objects.filter(category__name="cameras").count()
    accessories_count = Product.objects.filter(category__name="accessories").count()
    print(request.GET.get("price-min"), request.GET.get("price-max"))
    return render(request, "store.html", context={"products": products,
                                                  "top_selling": top_selling,
                                                  "categories": categories,
                                                  "cart": cart,
                                                  "user": user,
                                                  "laptops_count": laptops_count,
                                                  "smartphones_count": smartphones_count,
                                                  "cameras_count": cameras_count,
                                                  "accessories_count": accessories_count,
                                                  "laptops_selected": 1 if "laptops" in selected_categories else 0,
                                                  "cameras_selected": 1 if "cameras" in selected_categories else 0,
                                                  "smartphones_selected": 1 if "smartphones" in selected_categories else 0,
                                                  "accessories_selected": 1 if "accessories" in selected_categories else 0,
                                                  "price_min": request.GET.get("price-min"),
                                                  "price_max": request.GET.get("price-max")
                                                  })


def product(request, product_id, category):
    try:
        user = CustomUser.objects.get(username=request.user.username)
        cart = CartItem.objects.filter(user=user)
        user_profile = Profile.objects.get(user=user)
    except CustomUser.DoesNotExist:
        user = ""
        cart = ""
        user_profile = ""
    if request.method == "POST":
        return search_func(request)
    single_product = Product.objects.get(id=product_id)
    similar_products = list(Product.objects.filter(category=single_product.category))
    similar_products.remove(single_product)
    shuffle(similar_products)
    related_products = sample(similar_products, 3)
    categories = Categories.objects.all()
    return render(request, "product.html", context={"product": single_product,
                                                    "related_products": related_products,
                                                    "category": category,
                                                    "categories": categories,
                                                    "cart": cart,
                                                    "user": user
                                                    })


def category(request):
    try:
        user = CustomUser.objects.get(username=request.user.username)
        cart = CartItem.objects.filter(user=user)
        user_profile = Profile.objects.get(user=user)
    except CustomUser.DoesNotExist:
        user = ""
        cart = ""
        user_profile = ""
    if request.method == "POST":
        return search_func(request)
    categories = {"/laptops": "Laptops",
                  "/smartphones": "Smartphones",
                  "/accessories": "Accessories",
                  "/headphones": "Headphones",
                  "/cameras": "Cameras"}

    all_categories = Categories.objects.all()
    print(request.get_full_path().split("?")[0])
    main_category = Categories.objects.get(name__icontains=categories[request.get_full_path().split("?")[0]])
    products = Product.objects.filter(category=main_category, price__range=(request.GET.get("price-min", 1), request.GET.get("price-max", 5000)))
    top_selling = list(products)[:3]
    if "sorting" in request.GET:
        sorting_option = request.GET.get("sorting", None)
        if sorting_option == "asc-price":
            products = products.order_by("price")
        elif sorting_option == "desc-price":
            products = products.order_by("-price")
    return render(request, "category.html", context={"products": products,
                                                     "category": main_category.name,
                                                     "categories": all_categories,
                                                     "top_selling": top_selling,
                                                     "cart": cart,
                                                     "user": user,
                                                     })


def add_to_cart(request, product_id):
    print("-"*100)
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'You have to sign in before adding item to cart'})
    user_object = request.user
    product_object = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=user_object, product=product_object)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    product_object.quantity -= 1
    product_object.save()

    return JsonResponse({'message': 'Item added to cart.',
                         'quantity_in_stock': str(product_object.quantity),
                         'quantity': str(cart_item.quantity),
                         'image': str(cart_item.product.image.url),
                         'id': str(cart_item.product.id),
                         'price': str(cart_item.product.price),
                         'category': str(cart_item.product.category.name),
                         'name': str(cart_item.product.name)
                         })


def wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'You have to sign in before adding item to cart'})
    user_object = request.user
    product_object = Product.objects.get(id=product_id)
    wishlist_item, created = WishListItem.objects.get_or_create(user=user_object, product=product_object)





def delete_from_cart(request, product_id):
    product_obj = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(user=request.user, product=product_obj)
    product_obj.quantity = cart_item.quantity
    cart_item.delete()
    return JsonResponse({'quantity': str(cart_item.quantity),
                         'price': str(cart_item.product.price)})


def check_cart(request):
    try:
        cart = CartItem.objects.filter(user=request.user)
        cart_len = str(cart.count())
    except CartItem.DoesNotExist:
        cart_len = 0
    return JsonResponse({'cart_len': cart_len})


def check_wishlist(request):
    try:
        wishlist = WishListItem.objects.get(user=request.user)
        wishlist_len = str(wishlist.count())
    except WishListItem.DoesNotExist:
        wishlist_len = 0
    return JsonResponse({'wishlist_len': wishlist_len})


def remove_from_cart(request, product_id):
    user_object = request.user
    product_object = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(user=user_object, product=product_object)
    cart_item.quantity -= 1
    product_object.quantity += 1
    quantity = str(cart_item.quantity)
    if not cart_item.quantity:
        cart_item.delete()
    else:
        cart_item.save()
    product_object.save()
    return JsonResponse({"quantity": quantity})


@login_required(login_url="signin")
def log_out(request):
    logout(request)
    return redirect("index")


