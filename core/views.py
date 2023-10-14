from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from .models import CustomUser
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
    return render(request, "index.html")


def show_message_redirect(request, message, page):
    messages.info(request, message)
    return redirect(page)


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


def checkout(request):
    return render(request, "checkout.html")