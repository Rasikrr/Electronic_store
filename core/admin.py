from django.contrib import admin
from .models import CustomUser, Profile

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff")
    list_display_links = ("email", "username")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "city", "country")
    list_display_links = ("user", "first_name", "last_name")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)