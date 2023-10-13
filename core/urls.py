from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.SignupCreateView.as_view(), name="signup"),
    path("signin", views.signin, name="signin"),
    path("checkout", views.checkout, name="checkout")
]