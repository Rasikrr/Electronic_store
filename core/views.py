from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from .models import CustomUser, Profile
from django.views.generic.edit import CreateView
from .forms import SignupForm

# Create your views here.


class SignupCreateView(CreateView):
    template_name = "signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def index(request):
    try:
        user = CustomUser.objects.get(username=request.user.username)
    except CustomUser.DoesNotExist:
        user = ""
    return render(request, "index.html", context={"user": user})


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


def profile(request):
    user = request.user
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
        messages.info(request, "Data is saved")
        return redirect("profile")
    else:
        return render(request, "profile.html", context={"user_profile": user_profile
                                                        })


def checkout(request):
    return render(request, "checkout.html")