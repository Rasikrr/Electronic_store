from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.SignupCreateView.as_view(), name="signup"),
    path("signin", views.signin, name="signin"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("checkout/<int:user_id>/", views.checkout, name="checkout"),
    path("catalog", views.catalog, name="catalog"),
    path("laptops", views.category, name="laptops"),
    path("smartphones", views.category, name="smartphones"),
    path("cameras", views.category, name="cameras"),
    path("accessories", views.category, name="accessories"),
    path("<str:category>/product/<int:product_id>", views.product, name="product"),

    path("logout", views.log_out, name="logout")
]

