from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("checkout/<int:user_id>/", views.checkout, name="checkout"),
    path("catalog", views.catalog, name="catalog"),
    path("laptops", views.category, name="laptops"),
    path("smartphones", views.category, name="smartphones"),
    path("cameras", views.category, name="cameras"),
    path("accessories", views.category, name="accessories"),
    path("add_to_cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<int:prosuct_id>", views.remove_from_cart, name="remove_from_cart"),
    path("<str:category>/product/<int:product_id>", views.product, name="product"),
    path("check_cart", views.check_cart, name="check_cart"),
    path("logout", views.log_out, name="logout")
]

