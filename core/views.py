from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
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


def signup(request):
    if request.method == "POST":
        pass
    return render(request, "signup.html")


def signin(request):
    return render(request, "signin.html")


def checkout(request):
    return render(request, "checkout.html")