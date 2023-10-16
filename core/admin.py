from django.contrib import admin
from .models import CustomUser, Profile, Categories, Product

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


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity")
    list_display_links = ("name", "category")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(Product, ProductAdmin)