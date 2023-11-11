from django.contrib import admin
from .models import CustomUser, Profile, Categories, Product, CartItem, WishListItem, Order

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff")
    list_display_links = ("email", "username")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "city", "country")
    list_display_links = ("user", "first_name", "last_name")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    list_display_links = list_display


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity")
    list_display_links = list_display[0:len(list_display)-1]


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity")
    list_display_links = ("name", "category")


class WishListAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    list_display_links = list_display


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "city", "country", "address", "zip_code", "order_status", "total")
    list_display_links = ("user", "first_name", "last_name", "order_status")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(WishListItem, WishListAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
